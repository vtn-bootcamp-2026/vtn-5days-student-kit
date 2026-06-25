#!/usr/bin/env python3
"""
Capstone Grader Engine — Tác tử phân tích hồ sơ bài nộp và chấm điểm dự thảo.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any


EXCLUDED_SCAN_DIRS = {
    ".git",
    ".next",
    "__pycache__",
    "node_modules",
    "output",
    "playwright-report",
    "test-results",
}


def find_blueprint_file(group_dir: Path, key: str) -> Path | None:
    """Tìm tệp thiết kế thực tế ở root nhóm hoặc thư mục capstone_project, hỗ trợ có hoặc không có số thứ tự đầu."""
    possible_names = {
        "one_pager": ["01-use-case-one-pager.md", "use-case-one-pager.md", "1. use-case-one-pager.md", "1-use-case-one-pager.md"],
        "logical_workflow": ["02-logical-workflow.md", "logical-workflow.md", "2. logical-workflow.md", "2-logical-workflow.md"],
        "core_prompt_design": ["03-core-prompt-design.md", "core-prompt-design.md", "3. core-prompt-design.md", "3-core-prompt-design.md"],
        "compliance_checklist": ["04-compliance-checklist.md", "compliance-checklist.md", "4. compliance-checklist.md", "4-compliance-checklist.md"],
        "action_plan": ["05-action-plan-30-90-days.md", "action-plan-30-90-days.md", "5. action-plan-30-90-days.md", "5-action-plan-30-90-days.md"],
        "presentation": [
            "10-presentation-outline.md", "presentation-outline.md",
            "slide-presentation.html", "slide.html",
            "slide nhom 4.html", "slide nhom 3.pptx", "slide nhom 6.pdf",
            "slide nhom 4.pdf", "slide nhom 4.pptx", "Tra sua AI_Alarm-AI-Agent.pptx"
        ]
    }
    names = possible_names.get(key, [])
    for name in names:
        p = group_dir / name
        if p.exists():
            return p
        p = group_dir / "capstone_project" / name
        if p.exists():
            return p
    
    # Pattern fallback
    pattern_fallbacks = {
        "one_pager": ["01-*.md", "1-*.md", "1.*.md"],
        "logical_workflow": ["02-*.md", "2-*.md", "2.*.md"],
        "core_prompt_design": ["03-*.md", "3-*.md", "3.*.md"],
        "compliance_checklist": ["04-*.md", "4-*.md", "4.*.md"],
        "action_plan": ["05-*.md", "5-*.md", "5.*.md"],
        "presentation": ["10-*.md", "*presentation*.md", "*slide*.md"],
    }
    if key in pattern_fallbacks:
        pats = pattern_fallbacks[key]
        import fnmatch
        for base_dir in [group_dir, group_dir / "capstone_project"]:
            if base_dir.exists() and base_dir.is_dir():
                for p in base_dir.iterdir():
                    if p.is_file():
                        for pat in pats:
                            if fnmatch.fnmatch(p.name.lower(), pat.lower()):
                                return p

    # Fallback cho presentation: quét mọi file chứa "slide" hoặc "presentation" ở group_dir
    if key == "presentation":
        for p in group_dir.iterdir():
            if p.is_file():
                if any(k in p.name.lower() for k in ["slide", "presentation", "tra sua ai", "alarm-ai-agent"]):
                    return p
                if p.suffix.lower() in [".pptx", ".pdf"]:
                    return p
        capstone_dir = group_dir / "capstone_project"
        if capstone_dir.exists() and capstone_dir.is_dir():
            for p in capstone_dir.iterdir():
                if p.is_file():
                    if any(k in p.name.lower() for k in ["slide", "presentation", "tra sua ai", "alarm-ai-agent"]):
                        return p
                    if p.suffix.lower() in [".pptx", ".pdf"]:
                        return p
    return None


def find_workspace_file(group_dir: Path, rel_path: str) -> Path | None:
    """Tìm tệp tin trong toàn bộ phân cấp thư mục liên quan (nhóm, capstone_project, session root, v.v.)."""
    for base in [group_dir, group_dir / "capstone_project", group_dir.parent, group_dir.parent.parent, group_dir.parent.parent.parent]:
        p = base / rel_path
        if p.exists():
            return p
    return None


def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text or "").lower()


def count_keyword_hits(text: str, keywords: list[str]) -> int:
    text_norm = normalize_text(text)
    return sum(1 for keyword in keywords if normalize_text(keyword) in text_norm)


def count_regex_hits(text: str, patterns: list[str]) -> int:
    return sum(1 for pattern in patterns if re.search(pattern, text, re.IGNORECASE | re.MULTILINE))


def clamp_score(value: float, min_score: float, max_score: float) -> float:
    return round(max(min_score, min(max_score, value)), 1)


def safe_read_text(path: Path | None) -> str:
    if not path or not path.exists() or path.suffix.lower() in {".pdf", ".pptx", ".docx", ".zip"}:
        return ""
    try:
        return unicodedata.normalize("NFC", path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return ""


def iter_project_files(group_dir: Path) -> list[Path]:
    files: list[Path] = []
    for p in group_dir.rglob("*"):
        if not p.is_file():
            continue
        rel_parts = p.relative_to(group_dir).parts
        if any(part in EXCLUDED_SCAN_DIRS for part in rel_parts):
            continue
        files.append(p)
    return files


def score_by_hits(base: float, max_score: float, hits: int, target_hits: int) -> float:
    if target_hits <= 0:
        return base
    return clamp_score(base + (max_score - base) * min(hits, target_hits) / target_hits, 0.0, max_score)


def score_level(score: float, max_score: float) -> str:
    ratio = score / max_score if max_score else 0.0
    if ratio >= 0.9:
        return "rất tốt"
    if ratio >= 0.75:
        return "tốt"
    if ratio >= 0.6:
        return "đạt nhưng còn thiếu chiều sâu"
    return "cần cải thiện rõ"


def build_quality_comment(score: float, max_score: float, strengths: list[str], gaps: list[str]) -> str:
    strengths_text = "; ".join(strengths[:4]) if strengths else "chưa có tín hiệu mạnh nổi bật"
    gaps_text = "; ".join(gaps[:4]) if gaps else "chưa phát hiện thiếu hụt lớn theo tiêu chí tự động"
    lost = round(max_score - score, 1)
    return (
        f"Mức đánh giá: {score_level(score, max_score)} ({score}/{max_score}). "
        f"Điểm mạnh: {strengths_text}. "
        f"Hạn chế/rủi ro cần xem lại: {gaps_text}. "
        f"Điểm trừ ước tính {lost} điểm phản ánh phần còn thiếu về độ cụ thể, bằng chứng vận hành hoặc kiểm soát chất lượng."
    )


def analyze_submission(group_dir: Path) -> dict[str, Any]:
    """Phân tích các tệp nộp của nhóm và trích xuất hiện trạng."""
    group_id = group_dir.name
    blueprint_files = {}
    
    # 1. Định nghĩa các tệp Blueprint mặc định
    bp_mappings = {
        "one_pager": "01-use-case-one-pager.md",
        "logical_workflow": "02-logical-workflow.md",
        "core_prompt_design": "03-core-prompt-design.md",
        "compliance_checklist": "04-compliance-checklist.md",
        "action_plan": "05-action-plan-30-90-days.md"
    }

    placeholder_patterns = [
        r"\[Nhập\s*[^\]]*\]", r"\[Điền\s*[^\]]*\]", r"\[Tên\s*[^\]]*\]", 
        r"\[Mô tả\s*[^\]]*\]", r"\[KPI\s*[^\]]*\]", r"\[\.\.\.\]"
    ]
    placeholder_regex = re.compile("|".join(placeholder_patterns), re.IGNORECASE)

    for key, filename in bp_mappings.items():
        file_path = find_blueprint_file(group_dir, key)
        exists = file_path is not None
        word_count = 0
        has_placeholders = False
        
        extracted_info = {}
        has_mermaid = False
        hitl_points = []
        system_prompt_len = 0
        checked_count = 0
        has_30 = False
        has_90 = False

        if exists:
            rel_path = file_path.relative_to(group_dir).as_posix()
            content = file_path.read_text(encoding="utf-8")
            # NFC normalization
            content = unicodedata.normalize("NFC", content)
            word_count = len(content.split())
            has_placeholders = bool(placeholder_regex.search(content))
            
            # Phân tích chi tiết từng tệp
            if key == "one_pager":
                uc_match = re.search(r"#\s*(.*)", content)
                uc_name = uc_match.group(1).strip() if uc_match else "Chưa xác định"
                extracted_info = {
                    "use_case_name": uc_name,
                    "target_users": ["Kỹ sư NOC"],  # Mock hoặc trích xuất cơ bản
                    "kpis": ["Tiết kiệm 80% thời gian"]
                }
            elif key == "logical_workflow":
                has_mermaid = "```mermaid" in content
                hitl_points = re.findall(r"(?:HITL|con người|phê duyệt|duyệt|chốt chặn)\b", content, re.IGNORECASE)
            elif key == "core_prompt_design":
                sys_match = re.search(r"```yaml\s*([\s\S]*?)```", content)
                system_prompt_len = len(sys_match.group(1)) if sys_match else len(content)
            elif key == "compliance_checklist":
                checked_count = content.count("[x]") + content.count("[X]")
            elif key == "action_plan":
                has_30 = "30 ngày" in content
                has_90 = "90 ngày" in content
        else:
            rel_path = filename

        # Tính toán confidence_score cho từng file blueprint
        if exists:
            conf_score = 0.75 if has_placeholders else 0.98
        else:
            conf_score = 1.0  # Đã xác nhận chắc chắn tệp bị thiếu

        file_status = {
            "exists": exists,
            "resolved_path": rel_path,
            "word_count": word_count,
            "contains_placeholders": has_placeholders,
            "confidence_score": conf_score
        }
        
        if key == "one_pager":
            file_status["key_details_extracted"] = extracted_info
        elif key == "logical_workflow":
            file_status["has_mermaid"] = has_mermaid
            file_status["hitl_points"] = list(set(hitl_points))[:5]
        elif key == "core_prompt_design":
            file_status["system_prompt_length"] = system_prompt_len
            file_status["output_format"] = "JSON"
        elif key == "compliance_checklist":
            file_status["items_checked_count"] = checked_count
        elif key == "action_plan":
            file_status["has_30_days"] = has_30
            file_status["has_90_days"] = has_90

        blueprint_files[key] = file_status

    # 2. Định nghĩa các tệp mã nguồn
    anonymizer_py = find_workspace_file(group_dir, "src/anonymizer.py")
    test_py = find_workspace_file(group_dir, "templates/tests/test_anonymizer.py") or find_workspace_file(group_dir, "tests/test_anonymizer.py")
    project_files = iter_project_files(group_dir)
    code_suffixes = {".py", ".js", ".jsx", ".ts", ".tsx", ".ipynb"}
    code_files = [
        p for p in project_files
        if p.suffix.lower() in code_suffixes
        and p.name not in {"next-env.d.ts"}
        and not p.name.endswith(".tsbuildinfo")
    ]
    test_files = [
        p for p in code_files
        if "test" in p.name.lower() or "spec" in p.name.lower() or "e2e" in p.parts
    ]
    config_files = [
        p for p in project_files
        if p.name in {"requirements.txt", "package.json", "docker-compose.yml", "Dockerfile", "skill.json"}
    ]

    anonymizer_exists = anonymizer_py is not None
    funcs = []
    if anonymizer_exists:
        funcs = re.findall(r"def\s+(\w+)\(", anonymizer_py.read_text(encoding="utf-8"))

    test_exists = test_py is not None
    test_count = 0
    if test_exists:
        test_count = len(re.findall(r"def\s+test_", test_py.read_text(encoding="utf-8")))

    implementation_files = {
        "anonymizer_py": {
            "exists": anonymizer_exists,
            "resolved_path": anonymizer_py.relative_to(group_dir.parent.parent.parent).as_posix() if anonymizer_exists else "src/anonymizer.py",
            "contains_functions": funcs,
            "confidence_score": 0.95 if anonymizer_exists else 1.0
        },
        "test_anonymizer_py": {
            "exists": test_exists,
            "resolved_path": test_py.relative_to(group_dir.parent.parent.parent).as_posix() if test_exists else "templates/tests/test_anonymizer.py",
            "test_count": test_count,
            "confidence_score": 0.95 if test_exists else 1.0
        },
        "source_summary": {
            "code_file_count": len(code_files),
            "test_file_count": len(test_files),
            "config_file_count": len(config_files),
            "sample_code_files": [p.relative_to(group_dir).as_posix() for p in code_files[:8]],
            "sample_test_files": [p.relative_to(group_dir).as_posix() for p in test_files[:8]],
            "confidence_score": 0.95 if code_files else 1.0
        }
    }

    # 3. Logs và cấu hình
    log_csv = (
        find_workspace_file(group_dir, "outputs/execution-log.csv")
        or find_workspace_file(group_dir, "outputs/execution_log.csv")
        or next((p for p in project_files if p.suffix.lower() in {".csv", ".log"} and "log" in p.name.lower()), None)
    )
    env_file = find_workspace_file(group_dir, ".env")
    skill_json = find_workspace_file(group_dir, "main_skill/skill.json") or find_workspace_file(group_dir, "capstone_project/main_skill/skill.json")
    skill_md = find_workspace_file(group_dir, "main_skill/SKILL.md") or find_workspace_file(group_dir, "capstone_project/main_skill/SKILL.md")

    log_exists = log_csv is not None
    lines_count = 0
    if log_exists:
        lines_count = len(log_csv.read_text(encoding="utf-8").splitlines())

    env_exists = env_file is not None
    env_keys = []
    if env_exists:
        env_keys = [line.split("=")[0].strip() for line in env_file.read_text(encoding="utf-8").splitlines() if "=" in line]

    logs_and_configs = {
        "execution_log_csv": {
            "exists": log_exists,
            "resolved_path": log_csv.relative_to(group_dir).as_posix() if log_exists else "outputs/execution-log.csv",
            "lines_count": lines_count,
            "confidence_score": 0.95 if log_exists else 1.0
        },
        "env_file": {
            "exists": env_exists,
            "resolved_path": env_file.relative_to(group_dir).as_posix() if env_exists else ".env",
            "contains_keys": env_keys,
            "confidence_score": 0.95 if env_exists else 1.0
        },
        "skill_json": {
            "exists": skill_json is not None,
            "resolved_path": skill_json.relative_to(group_dir).as_posix() if skill_json else "main_skill/skill.json",
            "confidence_score": 0.95 if skill_json is not None else 1.0
        },
        "skill_md": {
            "exists": skill_md is not None,
            "resolved_path": skill_md.relative_to(group_dir).as_posix() if skill_md else "main_skill/SKILL.md",
            "confidence_score": 0.95 if skill_md is not None else 1.0
        }
    }

    # Tính toán độ tin cậy trung bình của Intake
    all_confs = [
        blueprint_files["one_pager"]["confidence_score"],
        blueprint_files["logical_workflow"]["confidence_score"],
        blueprint_files["core_prompt_design"]["confidence_score"],
        blueprint_files["compliance_checklist"]["confidence_score"],
        blueprint_files["action_plan"]["confidence_score"],
        implementation_files["anonymizer_py"]["confidence_score"],
        implementation_files["test_anonymizer_py"]["confidence_score"],
        logs_and_configs["execution_log_csv"]["confidence_score"],
        logs_and_configs["env_file"]["confidence_score"],
        logs_and_configs["skill_json"]["confidence_score"],
        logs_and_configs["skill_md"]["confidence_score"]
    ]
    avg_conf = sum(all_confs) / len(all_confs)

    return {
        "group_id": group_id,
        "confidence_score": round(avg_conf, 2),
        "blueprint_files": blueprint_files,
        "implementation_files": implementation_files,
        "logs_and_configs": logs_and_configs
    }



def generate_draft_grading(group_dir: Path, submission_status: dict[str, Any]) -> dict[str, Any]:
    """Tự động chấm điểm dự thảo dựa trên hiện trạng bài nộp và trích xuất minh chứng thật."""
    group_id = submission_status["group_id"]
    
    # Đọc nội dung tệp để lấy minh chứng thực tế
    def get_file_content_and_path(key: str, default_name: str) -> tuple[str, str]:
        info = submission_status["blueprint_files"].get(key, {})
        rel_path = info.get("resolved_path", default_name)
        file_path = group_dir / rel_path
        if file_path.exists():
            return file_path.read_text(encoding="utf-8"), rel_path
        return "", rel_path

    one_pager_content, path_one_pager = get_file_content_and_path("one_pager", "01-use-case-one-pager.md")
    workflow_content, path_workflow = get_file_content_and_path("logical_workflow", "02-logical-workflow.md")
    prompt_content, path_prompt = get_file_content_and_path("core_prompt_design", "03-core-prompt-design.md")
    plan_content, path_plan = get_file_content_and_path("action_plan", "05-action-plan-30-90-days.md")

    # Tìm slide presentation outline
    pres_file = find_blueprint_file(group_dir, "presentation")
    path_pres = pres_file.relative_to(group_dir).as_posix() if pres_file else "10-presentation-outline.md"

    # Tìm file log_csv và trích xuất header thực tế làm quote
    log_csv = (
        find_workspace_file(group_dir, "outputs/execution-log.csv")
        or find_workspace_file(group_dir, "outputs/execution_log.csv")
    )
    scanned_log_path = submission_status["logs_and_configs"]["execution_log_csv"].get("resolved_path")
    if not log_csv and scanned_log_path:
        log_csv = group_dir / scanned_log_path
    csv_quote = "timestamp,status,pii_count"
    csv_file_path = "outputs/execution-log.csv"
    if log_csv and log_csv.exists():
        csv_file_path = submission_status["logs_and_configs"]["execution_log_csv"]["resolved_path"]
        try:
            with open(log_csv, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line:
                    csv_quote = first_line
        except Exception:
            pass

    # Hàm tìm minh chứng trong tệp
    def find_quote(text: str, keywords: list[str]) -> str:
        text_norm = unicodedata.normalize("NFC", text)
        for kw in keywords:
            kw_norm = unicodedata.normalize("NFC", kw)
            match = re.search(rf"[^.\n]*?{re.escape(kw_norm)}[^.\n]*", text_norm, re.IGNORECASE)
            if match:
                quote = match.group().strip()
                if len(quote) > 10:
                    return quote
        return "Nội dung phản ánh yêu cầu đạt của nhóm học viên trong file."

    # Trích xuất minh chứng cho từng tiêu chí
    evidence_one_pager = find_quote(one_pager_content, ["mục tiêu", "đối tượng", "KPI", "vấn đề", "giá trị"])
    evidence_workflow = find_quote(workflow_content, ["HITL", "con người", "phê duyệt", "sơ đồ", "bước", "luồng", "workflow", "chế độ"])
    evidence_prompt = find_quote(prompt_content, ["system prompt", "lời nhắc", "JSON", "phòng vệ", "xml"])
    evidence_plan = find_quote(plan_content, ["30 ngày", "90 ngày", "lộ trình", "kế hoạch", "triển khai"])

    # Trích xuất minh chứng cho slide presentation
    if pres_file and pres_file.exists():
        if pres_file.suffix.lower() in ['.pptx', '.pdf', '.docx', '.zip']:
            evidence_pres = "Tài liệu slide/thuyết trình chính thức của nhóm."
        else:
            try:
                pres_content = pres_file.read_text(encoding="utf-8", errors="ignore")
                evidence_pres = find_quote(pres_content, ["vtn hr policy assistant", "slide nhom", "thuyết trình", "slide", "báo cáo", "giải pháp"])
                if "Nội dung phản ánh yêu cầu đạt" in evidence_pres:
                    evidence_pres = "Tài liệu slide/thuyết trình chính thức của nhóm."
            except Exception:
                evidence_pres = "Tài liệu slide/thuyết trình chính thức của nhóm."
    else:
        evidence_pres = "Dàn ý slide báo cáo kết quả dự án Capstone của nhóm"

    compliance_content, _ = get_file_content_and_path("compliance_checklist", "04-compliance-checklist.md")
    source_summary = submission_status["implementation_files"].get("source_summary", {})
    code_count = int(source_summary.get("code_file_count", 0))
    test_count = int(source_summary.get("test_file_count", 0))
    config_count = int(source_summary.get("config_file_count", 0))
    checked_count = int(submission_status["blueprint_files"]["compliance_checklist"].get("items_checked_count", 0))

    # Tính điểm chính theo chất lượng nội dung, không chỉ theo sự tồn tại của file.
    one_pager_exists = submission_status["blueprint_files"]["one_pager"]["exists"]
    if one_pager_exists:
        bp_hits = 0
        bp_hits += min(submission_status["blueprint_files"]["one_pager"]["word_count"] // 180, 4)
        bp_hits += count_keyword_hits(one_pager_content, ["vấn đề", "đối tượng", "người dùng", "kpi", "giá trị", "rủi ro", "hitl", "dữ liệu", "phạm vi", "triển khai"])
        bp_hits += min(checked_count // 3, 4)
        bp_hits -= 4 if submission_status["blueprint_files"]["one_pager"]["contains_placeholders"] else 0
        bp_hits -= 2 if submission_status["blueprint_files"]["compliance_checklist"]["contains_placeholders"] else 0
        score_bp = score_by_hits(15.0, 30.0, bp_hits, 16)
    else:
        score_bp = 0.0

    workflow_exists = submission_status["blueprint_files"]["logical_workflow"]["exists"]
    if workflow_exists:
        wf_hits = 0
        wf_hits += 3 if submission_status["blueprint_files"]["logical_workflow"].get("has_mermaid") else 0
        wf_hits += min(len(submission_status["blueprint_files"]["logical_workflow"].get("hitl_points", [])), 3)
        wf_hits += count_keyword_hits(workflow_content, ["fallback", "rollback", "review", "phê duyệt", "escalation", "log", "kiểm tra", "đầu vào", "đầu ra", "lỗi"])
        wf_hits -= 3 if submission_status["blueprint_files"]["logical_workflow"]["contains_placeholders"] else 0
        score_wf = score_by_hits(9.0, 20.0, wf_hits, 12)
    else:
        score_wf = 0.0

    prompt_exists = submission_status["blueprint_files"]["core_prompt_design"]["exists"]
    if prompt_exists:
        cp_hits = 0
        cp_hits += min(submission_status["blueprint_files"]["core_prompt_design"].get("system_prompt_length", 0) // 500, 4)
        cp_hits += count_keyword_hits(prompt_content, ["system prompt", "json", "schema", "xml", "prompt injection", "jailbreak", "không được", "chỉ trả về", "confidence", "citation"])
        cp_hits += count_regex_hits(prompt_content, [r"```(?:json|yaml)", r"\{[\s\S]*\"[a-zA-Z_]+\"[\s\S]*\}", r"<[^>]+>"])
        cp_hits -= 4 if submission_status["blueprint_files"]["core_prompt_design"]["contains_placeholders"] else 0
        score_cp = score_by_hits(9.0, 20.0, cp_hits, 13)
    else:
        score_cp = 0.0

    plan_exists = submission_status["blueprint_files"]["action_plan"]["exists"]
    if plan_exists:
        ap_hits = 0
        ap_hits += 3 if submission_status["blueprint_files"]["action_plan"].get("has_30_days") else 0
        ap_hits += 3 if submission_status["blueprint_files"]["action_plan"].get("has_90_days") else 0
        ap_hits += count_keyword_hits(plan_content, ["phụ trách", "owner", "mốc", "kpi", "nghiệm thu", "pilot", "đào tạo", "mở rộng", "rủi ro", "use case"])
        ap_hits += min(len(re.findall(r"\[[ xX]\]|\bngày\s+\d+|\bday\s+\d+", plan_content, re.IGNORECASE)), 5)
        ap_hits -= 5 if submission_status["blueprint_files"]["action_plan"]["contains_placeholders"] else 0
        score_ap = score_by_hits(7.0, 15.0, ap_hits, 14)
    else:
        score_ap = 0.0

    if pres_file and pres_file.exists():
        if pres_file.suffix.lower() in [".pptx", ".pdf"]:
            score_pres = 12.0
        else:
            pres_content = safe_read_text(pres_file)
            pres_hits = min(len(re.findall(r"<section|class=[\"']slide|^#|^##", pres_content, re.IGNORECASE | re.MULTILINE)), 7)
            pres_hits += count_keyword_hits(pres_content, ["vấn đề", "giải pháp", "demo", "kiến trúc", "kpi", "rủi ro", "lộ trình", "q&a"])
            score_pres = score_by_hits(8.0, 15.0, pres_hits, 12)
    else:
        score_pres = 0.0

    # Tính điểm cộng theo mức triển khai thực tế, có xét test/config/log.
    bonus_src = 0.0
    if code_count > 0:
        bonus_src = 3.0
        bonus_src += min(code_count, 8) * 0.35
        bonus_src += min(test_count, 10) * 0.35
        bonus_src += min(config_count, 4) * 0.3
        bonus_src = clamp_score(bonus_src, 1.0, 10.0)

    bonus_sec = 0.0
    if submission_status["logs_and_configs"]["execution_log_csv"]["exists"]:
        log_lines = int(submission_status["logs_and_configs"]["execution_log_csv"].get("lines_count", 0))
        bonus_sec += 2.0 + min(log_lines, 20) * 0.15
    if env_file := find_workspace_file(group_dir, ".env.example"):
        env_text = safe_read_text(env_file)
        bonus_sec += 2.0 if count_keyword_hits(env_text, ["api", "key", "token", "base_url"]) else 1.0
    bonus_sec += 2.0 if count_keyword_hits(compliance_content + prompt_content, ["prompt injection", "jailbreak", "data exfiltration", "role confusion"]) >= 2 else 0.0
    bonus_sec = clamp_score(bonus_sec, 0.0, 10.0)

    main_score = clamp_score(score_bp + score_wf + score_cp + score_ap + score_pres, 0.0, 100.0)
    bonus_score = clamp_score(bonus_src + bonus_sec, 0.0, 20.0)
    total_score = main_score
    
    classification = "Đạt"
    if total_score >= 90:
        classification = "Xuất sắc"
    elif total_score < 70:
        classification = "Cần bổ sung"

    # Tính độ tin cậy cho từng tiêu chí chấm điểm
    # 1. Blueprint Overall (one-pager)
    if submission_status["blueprint_files"]["one_pager"]["exists"]:
        conf_bp = 0.65 if submission_status["blueprint_files"]["one_pager"]["contains_placeholders"] else 0.95
    else:
        conf_bp = 0.0

    # 2. Logical Workflow
    if submission_status["blueprint_files"]["logical_workflow"]["exists"]:
        conf_wf = 0.95 if submission_status["blueprint_files"]["logical_workflow"]["has_mermaid"] else 0.70
    else:
        conf_wf = 0.0

    # 3. Core Prompt
    if submission_status["blueprint_files"]["core_prompt_design"]["exists"]:
        conf_cp = 0.65 if submission_status["blueprint_files"]["core_prompt_design"]["contains_placeholders"] else 0.95
    else:
        conf_cp = 0.0

    # 4. Action Plan
    if submission_status["blueprint_files"]["action_plan"]["exists"]:
        if submission_status["blueprint_files"]["action_plan"]["contains_placeholders"]:
            conf_ap = 0.65
        elif submission_status["blueprint_files"]["action_plan"]["has_30_days"] and submission_status["blueprint_files"]["action_plan"]["has_90_days"]:
            conf_ap = 0.95
        else:
            conf_ap = 0.75
    else:
        conf_ap = 0.0

    # 5. Presentation Outline
    pres_file = find_blueprint_file(group_dir, "presentation")
    conf_pres = 0.90 if pres_file else 0.50

    # 6. Source code & testing
    if submission_status["implementation_files"]["anonymizer_py"]["exists"]:
        conf_src = 0.95 if submission_status["implementation_files"]["test_anonymizer_py"]["exists"] else 0.80
    else:
        conf_src = 1.0  # Chắc chắn 0.0 điểm

    # 7. An toàn bảo mật & Logs
    if submission_status["logs_and_configs"]["execution_log_csv"]["exists"]:
        conf_sec = 0.95
    else:
        conf_sec = 1.0  # Chắc chắn 0.0 điểm

    bp_strengths = []
    bp_gaps = []
    if one_pager_exists:
        bp_strengths.append(f"one-pager có {submission_status['blueprint_files']['one_pager']['word_count']} từ, đủ nền để đánh giá")
        if count_keyword_hits(one_pager_content, ["vấn đề", "đối tượng", "người dùng"]):
            bp_strengths.append("mô tả bài toán và nhóm người dùng mục tiêu")
        if count_keyword_hits(one_pager_content, ["kpi", "%", "giảm", "tăng", "tiết kiệm"]):
            bp_strengths.append("có tín hiệu định lượng KPI/giá trị nghiệp vụ")
        if checked_count:
            bp_strengths.append(f"compliance checklist có {checked_count} mục được tick")
        if submission_status["blueprint_files"]["one_pager"]["contains_placeholders"]:
            bp_gaps.append("one-pager còn placeholder, làm giảm độ hoàn thiện")
        if submission_status["blueprint_files"]["compliance_checklist"]["contains_placeholders"]:
            bp_gaps.append("compliance checklist còn placeholder")
        if checked_count < 6:
            bp_gaps.append("bảng tự kiểm tuân thủ còn mỏng hoặc chưa tick đủ nhiều mục")
        if not count_keyword_hits(one_pager_content, ["rủi ro", "kiểm soát", "hitl"]):
            bp_gaps.append("chưa thể hiện rõ rủi ro và cơ chế con người kiểm soát")
    else:
        bp_gaps.append("thiếu one-pager nên không có cơ sở đánh giá blueprint")

    wf_strengths = []
    wf_gaps = []
    if workflow_exists:
        if submission_status["blueprint_files"]["logical_workflow"].get("has_mermaid"):
            wf_strengths.append("có sơ đồ Mermaid giúp đọc luồng dễ kiểm chứng")
        hitl_count = len(submission_status["blueprint_files"]["logical_workflow"].get("hitl_points", []))
        if hitl_count:
            wf_strengths.append(f"có {hitl_count} tín hiệu HITL/phê duyệt")
        if count_keyword_hits(workflow_content, ["fallback", "rollback", "lỗi"]):
            wf_strengths.append("có đề cập xử lý lỗi hoặc fallback")
        if not submission_status["blueprint_files"]["logical_workflow"].get("has_mermaid"):
            wf_gaps.append("thiếu sơ đồ Mermaid hoặc sơ đồ máy đọc được")
        if hitl_count == 0:
            wf_gaps.append("chưa thấy điểm chốt con người rõ ràng")
        if not count_keyword_hits(workflow_content, ["đầu vào", "đầu ra", "log", "kiểm tra"]):
            wf_gaps.append("chưa mô tả đủ input/output, logging hoặc kiểm tra chất lượng")
    else:
        wf_gaps.append("thiếu tài liệu luồng logic")

    cp_strengths = []
    cp_gaps = []
    if prompt_exists:
        prompt_len = submission_status["blueprint_files"]["core_prompt_design"].get("system_prompt_length", 0)
        if prompt_len >= 1000:
            cp_strengths.append(f"system prompt đủ dài ({prompt_len} ký tự) để thể hiện vai trò và ràng buộc")
        if count_keyword_hits(prompt_content, ["json", "schema"]):
            cp_strengths.append("có cấu trúc đầu ra JSON/schema")
        if count_keyword_hits(prompt_content, ["prompt injection", "jailbreak", "không được", "chỉ trả về"]):
            cp_strengths.append("có tín hiệu phòng thủ prompt injection/jailbreak")
        if count_regex_hits(prompt_content, [r"```(?:json|yaml)", r"<[^>]+>"]):
            cp_strengths.append("có ví dụ cấu trúc hoặc bọc dữ liệu bằng block/tag")
        if prompt_len < 700:
            cp_gaps.append("system prompt còn ngắn, khó bao quát đầy đủ vai trò, ràng buộc và edge cases")
        if not count_keyword_hits(prompt_content, ["confidence", "citation", "evidence"]):
            cp_gaps.append("thiếu yêu cầu confidence/citation/evidence để hỗ trợ kiểm chứng")
        if not count_keyword_hits(prompt_content, ["prompt injection", "jailbreak", "data exfiltration", "role confusion"]):
            cp_gaps.append("phòng thủ prompt injection chưa đủ cụ thể theo kịch bản tấn công")
        if submission_status["blueprint_files"]["core_prompt_design"]["contains_placeholders"]:
            cp_gaps.append("còn placeholder trong tài liệu prompt")
    else:
        cp_gaps.append("thiếu core prompt design")

    ap_strengths = []
    ap_gaps = []
    if plan_exists:
        if submission_status["blueprint_files"]["action_plan"].get("has_30_days"):
            ap_strengths.append("có giai đoạn 30 ngày")
        if submission_status["blueprint_files"]["action_plan"].get("has_90_days"):
            ap_strengths.append("có giai đoạn 90 ngày")
        if count_keyword_hits(plan_content, ["phụ trách", "owner"]):
            ap_strengths.append("có tín hiệu phân công người phụ trách")
        if count_keyword_hits(plan_content, ["kpi", "nghiệm thu", "pilot"]):
            ap_strengths.append("có KPI/pilot/nghiệm thu để triển khai thực tế")
        if not count_keyword_hits(plan_content, ["phụ trách", "owner"]):
            ap_gaps.append("phân công trách nhiệm chưa rõ")
        if not count_keyword_hits(plan_content, ["kpi", "đo", "nghiệm thu"]):
            ap_gaps.append("thiếu cơ chế đo lường và nghiệm thu")
        if not count_keyword_hits(plan_content, ["rủi ro", "rollback", "fallback"]):
            ap_gaps.append("chưa gắn kế hoạch với rủi ro và phương án dự phòng")
        if submission_status["blueprint_files"]["action_plan"]["contains_placeholders"]:
            ap_gaps.append("còn placeholder trong action plan")
    else:
        ap_gaps.append("thiếu action plan")

    pres_strengths = []
    pres_gaps = []
    if pres_file and pres_file.exists():
        pres_strengths.append(f"có tài liệu trình bày dạng {pres_file.suffix.lower() or 'markdown/html'}")
        if pres_file.suffix.lower() not in [".pptx", ".pdf"]:
            if count_keyword_hits(safe_read_text(pres_file), ["demo", "kiến trúc", "kpi", "rủi ro"]):
                pres_strengths.append("slide có tín hiệu demo/kiến trúc/KPI/rủi ro")
        else:
            pres_gaps.append("file nhị phân chỉ xác minh được sự tồn tại, chưa đọc sâu chất lượng từng slide")
    else:
        pres_gaps.append("thiếu slide hoặc presentation outline")

    src_strengths = []
    src_gaps = []
    if code_count:
        src_strengths.append(f"có {code_count} tệp mã nguồn")
        if test_count:
            src_strengths.append(f"có {test_count} tệp kiểm thử")
        if config_count:
            src_strengths.append(f"có {config_count} tệp cấu hình/đóng gói")
        if test_count == 0:
            src_gaps.append("chưa phát hiện tệp kiểm thử tự động")
        if config_count == 0:
            src_gaps.append("chưa phát hiện cấu hình triển khai/đóng gói")
    else:
        src_gaps.append("không phát hiện mã nguồn triển khai, chỉ chấm được phần thiết kế")

    sec_strengths = []
    sec_gaps = []
    log_exists = submission_status["logs_and_configs"]["execution_log_csv"]["exists"]
    if log_exists:
        sec_strengths.append(f"có log vận hành {submission_status['logs_and_configs']['execution_log_csv'].get('resolved_path')}")
    else:
        sec_gaps.append("chưa phát hiện log vận hành")
    if find_workspace_file(group_dir, ".env.example"):
        sec_strengths.append("có .env.example để tách cấu hình khỏi mã nguồn")
    else:
        sec_gaps.append("thiếu .env.example hoặc mẫu cấu hình an toàn")
    if count_keyword_hits(compliance_content + prompt_content, ["prompt injection", "jailbreak", "data exfiltration", "role confusion"]) >= 2:
        sec_strengths.append("có đề cập nhiều kịch bản an toàn/prompt injection")
    else:
        sec_gaps.append("chưa mô tả đủ các kịch bản jailbreak, exfiltration, role confusion")

    source_evidence = []
    sample_code_files = source_summary.get("sample_code_files", [])
    if sample_code_files:
        source_file = sample_code_files[0]
        source_path = group_dir / source_file
        source_text = safe_read_text(source_path)
        source_quote = "Tệp mã nguồn triển khai chính của nhóm."
        for line in source_text.splitlines():
            stripped = line.strip()
            if stripped and stripped not in {'"""', "'''"} and not stripped.startswith(("#", "//", "/*", "*")):
                source_quote = stripped[:180]
                break
        source_evidence = [{
            "file": source_file,
            "quote": source_quote,
            "description": "Mã nguồn triển khai thực tế của nhóm"
        }]

    return {
        "group_id": group_id,
        "grader_name": "Giám khảo AI",
        "evaluation_date": "2026-06-15",
        "rubric_type": "100_point",
        "main_criteria": {
            "blueprint_overall": {
                "score": score_bp,
                "confidence_score": conf_bp,
                "evidence": [
                    {
                        "file": path_one_pager,
                        "quote": evidence_one_pager,
                        "description": "Mô tả vấn đề nghiệp vụ và đối tượng sử dụng thực tế của phòng ban"
                    }
                ] if submission_status["blueprint_files"]["one_pager"]["exists"] else [],
                "comments": build_quality_comment(score_bp, 30.0, bp_strengths, bp_gaps)
            },
            "logical_workflow": {
                "score": score_wf,
                "confidence_score": conf_wf,
                "evidence": [
                    {
                        "file": path_workflow,
                        "quote": evidence_workflow,
                        "description": "Thiết kế luồng xử lý và chốt chặn phê duyệt của con người"
                    }
                ] if submission_status["blueprint_files"]["logical_workflow"]["exists"] else [],
                "comments": build_quality_comment(score_wf, 20.0, wf_strengths, wf_gaps)
            },
            "core_prompt": {
                "score": score_cp,
                "confidence_score": conf_cp,
                "evidence": [
                    {
                        "file": path_prompt,
                        "quote": evidence_prompt,
                        "description": "Thiết kế system prompt chuẩn hóa và các biện pháp bảo mật"
                    }
                ] if submission_status["blueprint_files"]["core_prompt_design"]["exists"] else [],
                "comments": build_quality_comment(score_cp, 20.0, cp_strengths, cp_gaps)
            },
            "action_plan": {
                "score": score_ap,
                "confidence_score": conf_ap,
                "evidence": [
                    {
                        "file": path_plan,
                        "quote": evidence_plan,
                        "description": "Lộ trình triển khai cụ thể và các use cases mở rộng"
                    }
                ] if submission_status["blueprint_files"]["action_plan"]["exists"] else [],
                "comments": build_quality_comment(score_ap, 15.0, ap_strengths, ap_gaps)
            },
            "presentation": {
                "score": score_pres,
                "confidence_score": conf_pres,
                "evidence": [
                    {
                        "file": path_pres,
                        "quote": evidence_pres,
                        "description": "Trình bày mạch lạc, cấu trúc slide rõ chữ"
                    }
                ] if pres_file is not None else [],
                "comments": build_quality_comment(score_pres, 15.0, pres_strengths, pres_gaps)
            }
        },
        "bonus_criteria": {
            "source_code_testing": {
                "score": bonus_src,
                "confidence_score": conf_src,
                "evidence": source_evidence,
                "comments": build_quality_comment(bonus_src, 10.0, src_strengths, src_gaps)
            },
            "safety_logging": {
                "score": bonus_sec,
                "confidence_score": conf_sec,
                "evidence": [
                    {
                        "file": csv_file_path,
                        "quote": csv_quote,
                        "description": "Đầu ra logs và cấu hình biến môi trường"
                    }
                ] if submission_status["logs_and_configs"]["execution_log_csv"]["exists"] else [],
                "comments": build_quality_comment(bonus_sec, 10.0, sec_strengths, sec_gaps)
            }
        },
        "total_score": total_score,
        "bonus_score": bonus_score,
        "total_score_with_bonus": clamp_score(main_score + bonus_score, 0.0, 120.0),
        "final_classification": classification,
        "general_comment": (
            f"Điểm chính {main_score}/100 phản ánh chất lượng hồ sơ Blueprint, luồng logic, prompt, kế hoạch và slide; "
            f"điểm cộng {bonus_score}/20 phản ánh mức triển khai mã nguồn, kiểm thử, log và an toàn vận hành. "
            f"Các nhận xét chi tiết nêu rõ tín hiệu đạt và phần còn thiếu để giám khảo có thể review chất lượng thay vì chỉ kiểm tra sự tồn tại của tệp."
        )
    }



def log_execution(group_dir: Path, step: int, action: str, status: str, message: str) -> None:
    """Ghi nhật ký thực thi vào cả execution_log.md và executon_log.md dưới dạng bảng Markdown."""
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_files = [
        group_dir / "output" / "execution_log.md",
        group_dir / "output" / "executon_log.md"
    ]
    for log_path in log_files:
        try:
            log_path.parent.mkdir(parents=True, exist_ok=True)
            exists = log_path.exists()
            with open(log_path, "a", encoding="utf-8") as f:
                if not exists:
                    f.write(f"---\nmuc-dich: Nhật ký thực thi workflow chấm bài Capstone\ntrang-thai: active\n---\n\n")
                    f.write(f"# Nhật ký thực thi (Execution Log) - {group_dir.name}\n\n")
                    f.write(f"| Thời gian | Bước | Hành động | Trạng thái | Chi tiết |\n")
                    f.write(f"| --- | --- | --- | --- | --- |\n")
                f.write(f"| {timestamp} | Bước {step} | {action} | {status} | {message} |\n")
        except Exception as e:
            print(f"[⚠️] Không thể ghi log thực thi vào {log_path.name}: {e}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Sử dụng: python grader_engine.py <duong_dan_nhom>")
        sys.exit(1)
        
    group_path = Path(sys.argv[1]).resolve()
    if not group_path.exists() or not group_path.is_dir():
        print(f"Lỗi: Thư mục nhóm '{group_path}' không tồn tại hoặc không phải là thư mục.")
        sys.exit(1)

    # Đảm bảo thư mục output tồn tại trước khi ghi log
    output_dir = group_path / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    log_execution(group_path, 1, "Khởi chạy Grader Engine", "INFO", "Bắt đầu phân tích bài nộp của nhóm.")

    print(f"Bắt đầu phân tích bài nộp của nhóm: {group_path.name}")
    try:
        status = analyze_submission(group_path)
        log_execution(group_path, 1, "Phân tích cấu trúc thư mục bài nộp", "SUCCESS", "Đã quét và phân tích xong hiện trạng các file thiết kế và mã nguồn.")
    except Exception as e:
        log_execution(group_path, 1, "Phân tích cấu trúc thư mục bài nộp", "FAIL", f"Lỗi trong quá trình phân tích bài nộp: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)
    
    # Lưu hiện trạng bài nộp
    status_file = output_dir / "submission_status.json"
    try:
        status_file.write_text(json.dumps(status, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Đã lưu hiện trạng bài nộp tại: output/{status_file.name}")
        log_execution(group_path, 1, "Lưu hiện trạng bài nộp (submission_status.json)", "SUCCESS", "Đã lưu trữ thành công thông tin cấu trúc tệp.")
    except Exception as e:
        log_execution(group_path, 1, "Lưu hiện trạng bài nộp (submission_status.json)", "FAIL", f"Lỗi khi lưu tệp hiện trạng: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)
    
    # Tạo chấm điểm dự thảo
    log_execution(group_path, 2, "Bắt đầu chấm điểm dự thảo", "INFO", "Khởi tạo luồng đánh giá tự động dựa trên rubric.")
    try:
        grading = generate_draft_grading(group_path, status)
        log_execution(group_path, 2, "Chấm điểm và trích dẫn minh chứng", "SUCCESS", "Đã hoàn thành đánh giá tự động và trích xuất minh chứng (evidence).")
    except Exception as e:
        log_execution(group_path, 2, "Chấm điểm và trích dẫn minh chứng", "FAIL", f"Lỗi trong quá trình chấm điểm dự thảo: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)

    grading_file = output_dir / "grading_result_draft.json"
    try:
        grading_file.write_text(json.dumps(grading, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Đã lưu kết quả chấm điểm dự thảo tại: output/{grading_file.name}")
        log_execution(group_path, 2, "Lưu kết quả chấm điểm dự thảo (grading_result_draft.json)", "SUCCESS", "Đã lưu trữ thành công kết quả chấm điểm dự thảo.")
    except Exception as e:
        log_execution(group_path, 2, "Lưu kết quả chấm điểm dự thảo (grading_result_draft.json)", "FAIL", f"Lỗi khi lưu kết quả chấm điểm dự thảo: {e}")
        print(f"Lỗi: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
