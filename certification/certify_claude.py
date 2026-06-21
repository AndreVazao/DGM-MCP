import json
import subprocess
import sys

def call_mcp(stdin_data):
    process = subprocess.Popen(
        [sys.executable, "-m", "dgm_mcp.main", "run-stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=stdin_data)
    return stdout, stderr

def parse_resps(stdout):
    resps = []
    for line in stdout.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        try:
            resps.append(json.loads(line))
        except Exception:
            continue
    return resps

def main():
    print("# CLAUDE DESKTOP CERTIFICATION LOG")
    results = []

    # Handshake
    init_payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": "claude-desktop", "version": "1.0.0"}}}

    # Test 1: Initialize
    stdout, _ = call_mcp(json.dumps(init_payload) + "\n")
    resps = parse_resps(stdout)
    resp_1 = next((r for r in resps if r.get("id") == 1), None)
    if resp_1:
        print("Test 1 (Initialize): PASS")
        results.append({"test": "initialize", "status": "PASS", "payload": init_payload, "response": resp_1})
    else:
        print("Test 1 (Initialize): FAIL")
        results.append({"test": "initialize", "status": "FAIL", "payload": init_payload, "response": stdout})
        return

    handshake = json.dumps(init_payload) + "\n" + json.dumps({"jsonrpc": "2.0", "method": "initialized"}) + "\n"

    # Test 2: Tools List
    list_tools = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_tools) + "\n")
    resps = parse_resps(stdout)
    resp_2 = next((r for r in resps if r.get("id") == 2), None)
    if resp_2 and 'tools' in resp_2.get('result', {}):
        print("Test 2 (Tools List): PASS")
        results.append({"test": "tools/list", "status": "PASS", "payload": list_tools, "response": resp_2})
    else:
        print("Test 2 (Tools List): FAIL")
        results.append({"test": "tools/list", "status": "FAIL", "payload": list_tools, "response": stdout})

    # Test 3: Tool Call (shell)
    call_shell = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "shell", "arguments": {"command": "echo certified"}}}
    stdout, _ = call_mcp(handshake + json.dumps(call_shell) + "\n")
    resps = parse_resps(stdout)
    resp_3 = next((r for r in resps if r.get("id") == 3), None)
    if resp_3 and not resp_3.get('result', {}).get('isError'):
        print("Test 3 (Tool Call): PASS")
        results.append({"test": "tools/call", "status": "PASS", "payload": call_shell, "response": resp_3})
    else:
        print("Test 3 (Tool Call): FAIL")
        results.append({"test": "tools/call", "status": "FAIL", "payload": call_shell, "response": stdout})

    # Test 4: Resources List
    list_res = {"jsonrpc": "2.0", "id": 4, "method": "resources/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_res) + "\n")
    resps = parse_resps(stdout)
    resp_4 = next((r for r in resps if r.get("id") == 4), None)
    if resp_4 and 'resources' in resp_4.get('result', {}):
        print("Test 4 (Resources List): PASS")
        results.append({"test": "resources/list", "status": "PASS", "payload": list_res, "response": resp_4})
    else:
        print("Test 4 (Resources List): FAIL")
        results.append({"test": "resources/list", "status": "FAIL", "payload": list_res, "response": stdout})

    # Test 5: Read Resource (dgm://runtime)
    read_res = {"jsonrpc": "2.0", "id": 5, "method": "resources/read", "params": {"uri": "dgm://runtime"}}
    stdout, _ = call_mcp(handshake + json.dumps(read_res) + "\n")
    resps = parse_resps(stdout)
    resp_5 = next((r for r in resps if r.get("id") == 5), None)
    if resp_5 and 'contents' in resp_5.get('result', {}):
        print("Test 5 (Read Resource): PASS")
        results.append({"test": "resources/read", "status": "PASS", "payload": read_res, "response": resp_5})
    else:
        print("Test 5 (Read Resource): FAIL")
        results.append({"test": "resources/read", "status": "FAIL", "payload": read_res, "response": stdout})

    # Test 6: Prompts List
    list_prompts = {"jsonrpc": "2.0", "id": 6, "method": "prompts/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_prompts) + "\n")
    resps = parse_resps(stdout)
    resp_6 = next((r for r in resps if r.get("id") == 6), None)
    if resp_6 and 'prompts' in resp_6.get('result', {}):
        print("Test 6 (Prompts List): PASS")
        results.append({"test": "prompts/list", "status": "PASS", "payload": list_prompts, "response": resp_6})
    else:
        print("Test 6 (Prompts List): FAIL")
        results.append({"test": "prompts/list", "status": "FAIL", "payload": list_prompts, "response": stdout})

    # Test 7: Get Prompt
    get_prompt = {"jsonrpc": "2.0", "id": 7, "method": "prompts/get", "params": {"name": "task_analysis", "arguments": {"task_description": "certification test"}}}
    stdout, _ = call_mcp(handshake + json.dumps(get_prompt) + "\n")
    resps = parse_resps(stdout)
    resp_7 = next((r for r in resps if r.get("id") == 7), None)
    if resp_7 and 'messages' in resp_7.get('result', {}):
        print("Test 7 (Get Prompt): PASS")
        results.append({"test": "prompts/get", "status": "PASS", "payload": get_prompt, "response": resp_7})
    else:
        print("Test 7 (Get Prompt): FAIL")
        results.append({"test": "prompts/get", "status": "FAIL", "payload": get_prompt, "response": stdout})

    # Test 8: Shutdown
    shutdown = {"jsonrpc": "2.0", "id": 8, "method": "shutdown"}
    stdout, _ = call_mcp(handshake + json.dumps(shutdown) + "\n")
    resps = parse_resps(stdout)
    resp_8 = next((r for r in resps if r.get("id") == 8), None)
    if resp_8 and resp_8.get('result', {}).get('ok'):
        print("Test 8 (Shutdown): PASS")
        results.append({"test": "shutdown", "status": "PASS", "payload": shutdown, "response": resp_8})
    else:
        print("Test 8 (Shutdown): FAIL")
        results.append({"test": "shutdown", "status": "FAIL", "payload": shutdown, "response": stdout})

    # Save to MD
    with open("VALIDATIONS/CLAUDE_DESKTOP.md", "w") as f:
        f.write("# CLAUDE DESKTOP CERTIFICATION REPORT\n\n")
        for res in results:
            f.write(f"## Test: {res['test']}\n")
            f.write(f"**Status**: {res['status']}\n\n")
            f.write("### Payload:\n```json\n")
            f.write(json.dumps(res['payload'], indent=2) + "\n")
            f.write("```\n\n")
            f.write("### Response:\n```json\n")
            if isinstance(res['response'], dict):
                f.write(json.dumps(res['response'], indent=2) + "\n")
            else:
                f.write(str(res['response']) + "\n")
            f.write("```\n\n")

if __name__ == "__main__":
    main()
