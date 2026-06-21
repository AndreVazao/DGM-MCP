import json
import subprocess
import sys
import requests
import time

def test_stdio():
    print("Testing STDIO...")
    process = subprocess.Popen(
        [sys.executable, "-m", "dgm_mcp.main", "run-stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    init_payload = {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}
    stdout, _ = process.communicate(input=json.dumps(init_payload) + "\n")
    try:
        resp = json.loads(stdout.strip())
        return "PASS" if resp.get("id") == 1 else "FAIL"
    except Exception:
        return "FAIL"

def test_http():
    print("Testing HTTP...")
    process = subprocess.Popen(
        [sys.executable, "-m", "dgm_mcp.main", "run-http"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(10)
    try:
        resp = requests.post("http://127.0.0.1:8003/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}}, timeout=5)
        status = "PASS" if resp.status_code == 200 else "FAIL"
    except Exception as e:
        print(f"HTTP Error: {e}")
        status = "FAIL"
    finally:
        process.terminate()
        process.wait()
    return status

def test_sse():
    print("Testing SSE...")
    process = subprocess.Popen(
        [sys.executable, "-m", "dgm_mcp.main", "run-sse"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    time.sleep(10)
    try:
        resp = requests.get("http://127.0.0.1:8002/mcp/sse", stream=True, timeout=5)
        status = "PASS" if resp.status_code == 200 else "FAIL"
    except Exception as e:
        print(f"SSE Error: {e}")
        status = "FAIL"
    finally:
        process.terminate()
        process.wait()
    return status

def main():
    results = {
        "STDIO": test_stdio(),
        "HTTP": test_http(),
        "SSE": test_sse()
    }

    with open("VALIDATIONS/MCP_INSPECTOR.md", "w") as f:
        f.write("# MCP INSPECTOR CERTIFICATION\n\n")
        for transport, status in results.items():
            f.write(f"- {transport}: {status}\n")
    print("Results saved to VALIDATIONS/MCP_INSPECTOR.md")

if __name__ == "__main__":
    main()
