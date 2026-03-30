#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path
import subprocess

CONFIG_DIR = Path.home() / ".ai-provider-switch"

def parse_toml(path):
    content = path.read_text()
    data = {"_common": {}}
    current_section = "_common"
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"): continue
        section_match = re.match(r'\[(.*?)\]', line)
        if section_match:
            current_section = section_match.group(1)
            if current_section not in data: data[current_section] = {}
        else:
            kv_match = re.match(r'([\w-]+)\s*=\s*"(.*?)"', line)
            if kv_match: data[current_section][kv_match.group(1)] = kv_match.group(2)
    return data

def get_val(data, service, keys):
    for section, values in data.items():
        if section.startswith(f"{service}."):
            for k in keys:
                if k in values: return values[k]
    for section in [service, "_common"]:
        if section in data:
            for k in keys:
                if k in data[section]: return data[section][k]
    return None

def test_claude(url, key, model):
    if not url or not key: return "N/A"
    test_url = url.rstrip("/")
    # Smart path: Only add /messages if no standard path is present
    if not any(test_url.endswith(s) for s in ["/messages", "/v1/messages"]):
        test_url = f"{test_url}/messages"
    
    payload = {"max_tokens": 1, "messages": [{"role": "user", "content": "Hi"}]}
    if model: payload["model"] = model
    else: payload["model"] = "claude-3-haiku-20240307"

    cmd = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "POST", test_url,
        "-H", f"x-api-key: {key}",
        "-H", "anthropic-version: 2023-06-01",
        "-H", "content-type: application/json",
        "-d", json.dumps(payload)
    ]
    try:
        res = subprocess.check_output(cmd, timeout=10).decode().strip()
        return f"PASS ({res})" if res == "200" else f"FAIL ({res})"
    except: return "ERROR"

def test_codex(url, key, model):
    if not url or not key: return "N/A"
    test_url = url.rstrip("/")
    # Smart path: Only add /chat/completions if no standard path is present
    if not any(test_url.endswith(s) for s in ["/chat/completions", "/v1/chat/completions"]):
        test_url = f"{test_url}/chat/completions"

    payload = {"messages": [{"role": "user", "content": "Hi"}]}
    if model: payload["model"] = model
    else: payload["model"] = "gpt-3.5-turbo"

    cmd = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-X", "POST", test_url,
        "-H", f"Authorization: Bearer {key}",
        "-H", "content-type: application/json",
        "-d", json.dumps(payload)
    ]
    try:
        res = subprocess.check_output(cmd, timeout=10).decode().strip()
        return f"PASS ({res})" if res == "200" else f"FAIL ({res})"
    except: return "ERROR"

def main():
    print(f"{'Provider':<15} {'Claude (Anthropic)':<20} {'Codex (OpenAI)'}")
    print("-" * 65)
    for p in sorted(CONFIG_DIR.glob("*.toml")):
        data = parse_toml(p)
        c_url = get_val(data, "claude", ["url", "base_url"])
        c_key = get_val(data, "claude", ["key", "api_key"])
        c_mod = get_val(data, "claude", ["model"])
        x_url = get_val(data, "codex", ["url", "base_url"])
        x_key = get_val(data, "codex", ["key", "api_key"])
        x_mod = get_val(data, "codex", ["model"])
        print(f"{p.stem:<15} {test_claude(c_url, c_key, c_mod):<20} {test_codex(x_url, x_key, x_mod)}")

if __name__ == "__main__":
    main()

