#!/usr/bin/env python3
import json
import re
import subprocess
from pathlib import Path

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

def get_base_data(data, service):
    # Try to find URL and Key from service section or common
    url = None
    key = None
    for section in [service, "_common"]:
        if section in data:
            if not url: url = data[section].get("url") or data[section].get("base_url")
            if not key: key = data[section].get("key") or data[section].get("api_key")
    # Also check groups
    if not url or not key:
        for section, values in data.items():
            if section.startswith(f"{service}."):
                if not url: url = values.get("url") or values.get("base_url")
                if not key: key = values.get("key") or values.get("api_key")
    return url, key

def test_endpoint(url, key, path, protocol):
    full_url = url.rstrip("/") + path
    if protocol == "claude":
        cmd = [
            "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
            "-X", "POST", full_url,
            "-H", f"x-api-key: {key}",
            "-H", "anthropic-version: 2023-06-01",
            "-H", "content-type: application/json",
            "-d", '{"model": "claude-3-haiku-20240307", "max_tokens": 1, "messages": [{"role": "user", "content": "Hi"}]}'
        ]
    else: # codex
        cmd = [
            "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
            "-X", "POST", full_url,
            "-H", f"Authorization: Bearer {key}",
            "-H", "content-type: application/json",
            "-d", '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "Hi"}]}'
        ]
    try:
        res = subprocess.check_output(cmd, timeout=5).decode().strip()
        return res
    except: return "ERR"

def main():
    paths = {
        "claude": ["/v1/messages", "/messages"],
        "codex": ["/v1/chat/completions", "/chat/completions"]
    }

    print(f"{'Provider':<15} {'Service':<8} {'Path':<25} {'Status'}")
    print("-" * 60)

    for p in sorted(CONFIG_DIR.glob("*.toml")):
        data = parse_toml(p)
        for service in ["claude", "codex"]:
            url, key = get_base_data(data, service)
            if not url or not key: continue
            
            # Remove any trailing /v1 or /v1/ from the base url for discovery
            base_url = re.sub(r'/v1/?$', '', url.rstrip("/"))
            
            for path in paths[service]:
                status = test_endpoint(base_url, key, path, service)
                print(f"{p.stem:<15} {service:<8} {path:<25} {status}")

if __name__ == "__main__":
    main()
