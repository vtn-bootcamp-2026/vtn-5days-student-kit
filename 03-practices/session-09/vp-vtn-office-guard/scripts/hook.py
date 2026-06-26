#!/usr/bin/env python3
"""
Hook bảo mật lớp cứng cho "Vệ sĩ văn phòng VTN"
================================================
Đây là "người bảo vệ cửa": chạy TRƯỚC khi skill định ghi/ xoá file.
Nếu thao tác nhắm ngoài thư mục outputs/ | kb/ | schemas/ → chặn, không cho qua.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

# Chỉ cho phép ghi trong các thư mục an toàn
SAFE_DIRS = ("outputs", "kb", "schemas")

# Các công cụ nguy hiểm cần hạn chế
DANGEROUS_TOOLS = ("write_file", "patch", "terminal", "process", "execute_code", "delete_file")


def decide(event: dict) -> dict:
    tool = event.get("tool_name", "")
    path_str = event.get("tool_input", {}).get("path", "")

    # Luôn cho phép đọc
    if tool in ("read_file", "search", "list"):
        return {"action": "allow"}

    # Chặn mọi công cụ nguy hiểm trừ khi nằm trong thư mục an toàn
    if tool in DANGEROUS_TOOLS:
        if not path_str:
            return {
                "action": "block",
                "message": f"Vệ sĩ VTN chặn thao tác '{tool}' vì đường dẫn trống."
            }
        
        try:
            p = Path(path_str)
            # Kiểm tra xem có bất kỳ phần nào của đường dẫn khớp vớiSAFE_DIRS không
            # Để giải quyết cả các đường dẫn tương đối (như outputs/ok.txt, ./outputs/ok.txt)
            # và tuyệt đối (như /path/to/outputs/ok.txt)
            is_safe = False
            for part in p.parts:
                if part in SAFE_DIRS:
                    is_safe = True
                    break
            if is_safe:
                return {"action": "allow"}
        except Exception:
            pass

        return {
            "action": "block",
            "message": f"Vệ sĩ VTN chặn thao tác '{tool}' ngoài thư mục an toàn "
            f"({', '.join(SAFE_DIRS)}). Đường dẫn bị chặn: {path_str}",
        }

    return {"action": "allow"}


if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    try:
        event = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        event = {"tool_name": "unknown", "tool_input": {}}
    print(json.dumps(decide(event), ensure_ascii=False))
