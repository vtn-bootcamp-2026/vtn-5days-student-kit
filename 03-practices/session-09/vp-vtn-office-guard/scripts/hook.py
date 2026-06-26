#!/usr/bin/env python3
"""
Hook bảo mật lớp cứng cho "Vệ sĩ văn phòng VTN"
================================================
Đây là "người bảo vệ cửa": chạy TRƯỚC khi skill định ghi/ xoá file.
Nếu thao tác nhắm ngoài thư mục outputs/ | kb/ | schemas/ → chặn, không cho qua.

Cách kiểm tra nhanh (paste vào terminal):
    printf '{"tool_name":"write_file","tool_input":{"path":"/etc/passwd"}}' | python scripts/hook.py
    → {"action": "block", "message": "...""}

    printf '{"tool_name":"write_file","tool_input":{"path":"outputs/ok.txt"}}' | python scripts/hook.py
    → {"action": "allow"}
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
    path = event.get("tool_input", {}).get("path", "")

    # Luôn cho phép đọc
    if tool in ("read_file", "search", "list"):
        return {"action": "allow"}

    # Chặn mọi công cụ nguy hiểm trừ khi nằm trong thư mục an toàn
    if tool in DANGEROUS_TOOLS:
        top = Path(path).parts[0] if path else ""
        # Chuẩn hóa nếu có dấu / ở đầu hoặc là đường dẫn tuyệt đối
        if not top and path.startswith("/"):
            # Ví dụ: /etc/passwd -> Path('/etc/passwd').parts[0] là '/' hoặc 'etc'
            parts = Path(path).parts
            if len(parts) > 1:
                top = parts[1] if parts[0] == "/" else parts[0]
            else:
                top = parts[0]
        
        if top in SAFE_DIRS:
            return {"action": "allow"}
            
        return {
            "action": "block",
            "message": f"Vệ sĩ VTN chặn thao tác '{tool}' ngoài thư mục an toàn "
            f"({', '.join(SAFE_DIRS)}). Đường dẫn bị chặn: {path}",
        }

    return {"action": "allow"}


if __name__ == "__main__":
    raw = sys.stdin.read().strip()
    try:
        event = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        event = {"tool_name": "unknown", "tool_input": {}}
    print(json.dumps(decide(event), ensure_ascii=False))
