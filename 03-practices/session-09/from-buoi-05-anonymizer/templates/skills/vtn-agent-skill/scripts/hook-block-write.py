#!/usr/bin/env python3
"""
Hook kiểm soát an toàn cho VTN Agent (pre_tool_call).
Chặn các công cụ ghi file và thực thi lệnh shell.
Dùng với Hermes Agent: hermes --accept-hooks -p <profile> chat
"""
import json
import sys

# Nhận payload JSON từ stdin do Hermes CLI truyền qua
payload = json.load(sys.stdin)
tool_name = payload.get("tool_name") or ""
tool_input = payload.get("tool_input") or {}

# Danh sách các công cụ nguy hại bị cấm hoàn toàn với trợ lý chỉ đọc
blocked_tools = {
    "write_file",
    "patch",
    "terminal",
    "process",
    "execute_code"
}

if tool_name in blocked_tools:
    # Trả về quyết định chặn dưới dạng JSON chuẩn của Hermes
    print(json.dumps({
        "action": "block",
        "message": f"Lab hook active: blocked tool {tool_name}. Agent is read-only per VTN security policy."
    }))
else:
    # Cho phép các công cụ khác đi qua (như read_file)
    print("{}")
