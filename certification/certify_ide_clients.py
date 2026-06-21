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

def certify(client_name):
    print(f"Certifying {client_name}...")
    results = []

    # Discovery
    init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "clientInfo": {"name": client_name}}})
    handshake = init + "\n" + json.dumps({"jsonrpc": "2.0", "method": "initialized"}) + "\n"

    stdout, _ = call_mcp(handshake + json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"}) + "\n")
    resps = parse_resps(stdout)
    discovery = "PASS" if any(r.get("id") == 2 and "tools" in r.get("result", {}) for r in resps) else "FAIL"
    results.append(f"- Discovery: {discovery}")

    # Tool Call
    stdout, _ = call_mcp(handshake + json.dumps({"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "shell", "arguments": {"command": "echo " + client_name}}}) + "\n")
    resps = parse_resps(stdout)
    call = "PASS" if any(r.get("id") == 3 and not r.get("result", {}).get("isError") for r in resps) else "FAIL"
    results.append(f"- Tool Call: {call}")

    # Resources
    stdout, _ = call_mcp(handshake + json.dumps({"jsonrpc": "2.0", "id": 4, "method": "resources/list"}) + "\n")
    resps = parse_resps(stdout)
    res = "PASS" if any(r.get("id") == 4 and "resources" in r.get("result", {}) for r in resps) else "FAIL"
    results.append(f"- Resources: {res}")

    with open(f"VALIDATIONS/{client_name.upper()}.md", "w") as f:
        f.write(f"# {client_name.upper()} CERTIFICATION\n\n")
        f.write("\n".join(results) + "\n")

def main():
    certify("Cursor")
    certify("Windsurf")

if __name__ == "__main__":
    main()
