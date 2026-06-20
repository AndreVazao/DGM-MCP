import subprocess
import json
import time
import sys

def run_test(name, messages, expected_checks=None):
    print(f"\n--- Running Test: {name} ---")

    process = subprocess.Popen(
        [sys.executable, "-m", "dgm_mcp.main", "run-stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    responses = []

    try:
        for msg in messages:
            if isinstance(msg, str):
                msg_str = msg
            else:
                msg_str = json.dumps(msg)

            print(f"SEND: {msg_str}")
            process.stdin.write(msg_str + "\n")
            process.stdin.flush()

            # If it has an 'id' or it's a raw string (invalid json), we expect a response line
            if (isinstance(msg, dict) and "id" in msg) or isinstance(msg, str):
                line = process.stdout.readline()
                if line:
                    try:
                        resp = json.loads(line)
                        responses.append(resp)
                        print(f"RECV: {json.dumps(resp)}")
                    except json.JSONDecodeError:
                        print(f"RECV (raw): {line.strip()}")
                        responses.append(line.strip())
                else:
                    print("RECV: (no response)")
                    responses.append(None)
            else:
                # Notification
                print("SEND: (notification, no response expected)")
                # We don't append anything to responses for notifications to keep indices aligned with requests
                time.sleep(0.1)

    finally:
        process.terminate()

    if expected_checks:
        for check in expected_checks:
            if not check(responses):
                print(f"❌ FAILED check in {name}")
                return False

    print(f"✅ PASSED: {name}")
    return True

def check_handshake(resps):
    if not resps[0] or "result" not in resps[0]: return False
    return True

def check_tools_list(resps):
    # resps[0]: initialize
    # resps[1]: tools/list
    if len(resps) < 2 or not resps[1] or "result" not in resps[1]: return False
    return "tools" in resps[1]["result"]

def check_uninitialized_error(resps):
    if not resps[0] or "error" not in resps[0]: return False
    return resps[0]["error"]["code"] == -32000

def main():
    success = True

    # 1. Standard Handshake + Tools List
    success &= run_test("Full Handshake & Discovery", [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    ], [check_handshake, check_tools_list])

    # 2. Lifecycle Gating (Error -32000)
    success &= run_test("Lifecycle Gating", [
        {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}
    ], [check_uninitialized_error])

    # 3. Tool Call
    success &= run_test("Tool Call Execution", [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}},
        {"jsonrpc": "2.0", "method": "initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "shell", "arguments": {"command": "echo hello"}}}
    ], [
        lambda resps: resps[1] and "result" in resps[1] and "content" in resps[1]["result"]
    ])

    # 4. Invalid JSON
    success &= run_test("Invalid JSON Payload", [
        '{"jsonrpc": "2.0", "id": 1, "method": "initialize", ' # Incomplete JSON
    ], [
        lambda resps: resps[0] and "error" in resps[0] and resps[0]["error"]["code"] == -32700
    ])

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
