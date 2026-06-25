import argparse
import hashlib
import json
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_text(path: Path) -> str | None:
    if not path.exists():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()


@contextmanager
def manifest_lock(jobs_path: Path, timeout_seconds: float = 30.0):
    lock_path = jobs_path.with_suffix(jobs_path.suffix + ".lock")
    started = time.time()
    fd = None
    while True:
        try:
            fd = os.open(str(lock_path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.write(fd, f"{os.getpid()}\n".encode("utf-8"))
            break
        except FileExistsError:
            if time.time() - started > timeout_seconds:
                raise SystemExit(f"jobs manifest is locked by another recorder: {lock_path}")
            time.sleep(0.25)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def write_json_atomic(path: Path, data: dict):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        temp_name = handle.name
    Path(temp_name).replace(path)


def main():
    parser = argparse.ArgumentParser(description="Record a selected Codex image_gen output into the UDDS slide output folder.")
    parser.add_argument("--jobs", required=True, help="Path to image_tool_jobs.json")
    parser.add_argument("--job-id", required=True, help="Job id, for example slide1")
    parser.add_argument("--source", required=True, help="Selected Codex image_gen output file")
    parser.add_argument(
        "--allow-stale-source",
        action="store_true",
        help="Allow recording a source file older than prompt/output timestamps (not recommended).",
    )
    parser.add_argument(
        "--allow-source-reuse",
        action="store_true",
        help="Allow the same generated source image to be recorded for more than one job (not recommended).",
    )
    parser.add_argument(
        "--allow-overwrite-complete",
        action="store_true",
        help="Allow overwriting a job that is already marked complete (not recommended).",
    )
    args = parser.parse_args()

    jobs_path = Path(args.jobs).resolve()
    source = Path(args.source).resolve()
    if not source.exists():
        raise SystemExit(f"source image not found: {source}")

    with manifest_lock(jobs_path):
        data = json.loads(jobs_path.read_text(encoding="utf-8"))
        jobs = data.get("jobs", [])
        match = None
        for job in jobs:
            if job.get("id") == args.job_id:
                match = job
                break

        if not match:
            raise SystemExit(f"job id not found: {args.job_id}")

        if match.get("status") == "complete" and not args.allow_overwrite_complete:
            raise SystemExit(
                f"refusing to overwrite complete job: {args.job_id}. "
                "Use a fresh job id/output folder, or pass --allow-overwrite-complete only for an intentional replacement."
            )

        output_path = Path(match["output_path"]).resolve()
        prompt_path = Path(match.get("prompt_path", "")).resolve()
        source_mtime = source.stat().st_mtime

        if source == output_path:
            raise SystemExit("source and output are the same file; pass the generated Codex output, not the workspace target")

        source_hash = sha256_file(source)
        if not args.allow_source_reuse:
            for job in jobs:
                if job.get("id") == args.job_id:
                    continue
                if job.get("source_sha256") == source_hash or Path(job.get("source_image_tool_output", "")).resolve() == source:
                    raise SystemExit(
                        "refusing source reuse: this generated image is already recorded "
                        f"for job {job.get('id')}. Pass the correct per-job source or use --allow-source-reuse."
                    )

        if not args.allow_stale_source:
            if prompt_path.exists():
                prompt_mtime = prompt_path.stat().st_mtime
                if source_mtime < prompt_mtime:
                    raise SystemExit(
                        "refusing stale source: source image is older than prompt file. "
                        "Generate again and pass the new source path, or use --allow-stale-source to override."
                    )
            if output_path.exists():
                output_mtime = output_path.stat().st_mtime
                if source_mtime <= output_mtime:
                    raise SystemExit(
                        "refusing stale source: source image is not newer than existing output. "
                        "Delete output/regenerate or use --allow-stale-source to override."
                    )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, output_path)

        recorded_at = datetime.now(timezone.utc).isoformat()
        prompt_hash = sha256_text(prompt_path)
        output_hash = sha256_file(output_path)

        match["status"] = "complete"
        match["recorded_at"] = recorded_at
        match["source_image_tool_output"] = str(source)
        match["source_sha256"] = source_hash
        match["output_sha256"] = output_hash
        match["prompt_sha256"] = prompt_hash
        match["recorder"] = "record_image_tool_result.py"

        sidecar = output_path.with_suffix(output_path.suffix + ".record.json")
        sidecar.write_text(
            json.dumps(
                {
                    "job_id": args.job_id,
                    "recorded_at": recorded_at,
                    "jobs_path": str(jobs_path),
                    "prompt_path": str(prompt_path) if prompt_path.exists() else None,
                    "prompt_sha256": prompt_hash,
                    "source_image_tool_output": str(source),
                    "source_sha256": source_hash,
                    "output_path": str(output_path),
                    "output_sha256": output_hash,
                },
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )

        write_json_atomic(jobs_path, data)

    print(f"[OK] Recorded {args.job_id}")
    print(f"[OK] Output: {output_path}")
    print(f"[OK] Source sha256: {source_hash}")


if __name__ == "__main__":
    main()
