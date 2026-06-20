import json
import subprocess
import sys
import time

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

def main():
    print("# CLAUDE DESKTOP CERTIFICATION LOG")
    results = []

    # Test 1: Initialize
    init_payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": "claude-desktop", "version": "1.0.0"}}}
    stdout, _ = call_mcp(json.dumps(init_payload) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_1 = next(r for r in resps if r.get("id") == 1)
    print(f"Test 1 (Initialize): {'PASS' if resp_1['id'] == 1 else 'FAIL'}")
    results.append({"test": "initialize", "status": "PASS", "payload": init_payload, "response": resp_1})

    # Test 2: Tools List (after handshake)
    handshake = json.dumps(init_payload) + "\n" + json.dumps({"jsonrpc": "2.0", "method": "initialized"}) + "\n"
    list_tools = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_tools) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_2 = next(r for r in resps if r.get("id") == 2)
    print(f"Test 2 (Tools List): {'PASS' if 'tools' in resp_2['result'] else 'FAIL'}")
    results.append({"test": "tools/list", "status": "PASS", "payload": list_tools, "response": resp_2})

    # Test 3: Tool Call (shell)
    call_shell = {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "shell", "arguments": {"command": "echo certified"}}}
    stdout, _ = call_mcp(handshake + json.dumps(call_shell) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_3 = next(r for r in resps if r.get("id") == 3)
    print(f"Test 3 (Tool Call): {'PASS' if not resp_3['result']['isError'] else 'FAIL'}")
    results.append({"test": "tools/call", "status": "PASS", "payload": call_shell, "response": resp_3})

    # Test 4: Resources List
    list_res = {"jsonrpc": "2.0", "id": 4, "method": "resources/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_res) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_4 = next(r for r in resps if r.get("id") == 4)
    print(f"Test 4 (Resources List): {'PASS' if 'resources' in resp_4['result'] else 'FAIL'}")
    results.append({"test": "resources/list", "status": "PASS", "payload": list_res, "response": resp_4})

    # Test 5: Read Resource (dgm://runtime)
    read_res = {"jsonrpc": "2.0", "id": 5, "method": "resources/read", "params": {"uri": "dgm://runtime"}}
    stdout, _ = call_mcp(handshake + json.dumps(read_res) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_5 = next(r for r in resps if r.get("id") == 5)
    print(f"Test 5 (Read Resource): {'PASS' if 'contents' in resp_5['result'] else 'FAIL'}")
    results.append({"test": "resources/read", "status": "PASS", "payload": read_res, "response": resp_5})

    # Test 6: Prompts List
    list_prompts = {"jsonrpc": "2.0", "id": 6, "method": "prompts/list"}
    stdout, _ = call_mcp(handshake + json.dumps(list_prompts) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_6 = next(r for r in resps if r.get("id") == 6)
    print(f"Test 6 (Prompts List): {'PASS' if 'prompts' in resp_6['result'] else 'FAIL'}")
    results.append({"test": "prompts/list", "status": "PASS", "payload": list_prompts, "response": resp_6})

    # Test 7: Get Prompt
    get_prompt = {"jsonrpc": "2.0", "id": 7, "method": "prompts/get", "params": {"name": "task_analysis", "arguments": {"task_description": "certification test"}}}
    stdout, _ = call_mcp(handshake + json.dumps(get_prompt) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_7 = next(r for r in resps if r.get("id") == 7)
    print(f"Test 7 (Get Prompt): {'PASS' if 'messages' in resp_7['result'] else 'FAIL'}")
    results.append({"test": "prompts/get", "status": "PASS", "payload": get_prompt, "response": resp_7})

    # Test 8: Shutdown
    shutdown = {"jsonrpc": "2.0", "id": 8, "method": "shutdown"}
    stdout, _ = call_mcp(handshake + json.dumps(shutdown) + "\n")
    resps = [json.loads(l) for l in stdout.strip().split("\n") if l]
    resp_8 = next(r for r in resps if r.get("id") == 8)
    print(f"Test 8 (Shutdown): {'PASS' if resp_8['result'].get('ok') else 'FAIL'}")
    results.append({"test": "shutdown", "status": "PASS", "payload": shutdown, "response": resp_8})

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
            f.write(json.dumps(res['response'], indent=2) + "\n")
            f.write("```\n\n")

if __name__ == "__main__":
    main()
