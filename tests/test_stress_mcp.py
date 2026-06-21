import time
import concurrent.futures
from dgm_mcp.core.runtime import MCPRuntime
from dgm_mcp.config.config_manager import ConfigManager
from dgm_mcp.mcp.stdio import StdioMCPServer

def test_stress_mcp():
    config = ConfigManager().load()
    runtime = MCPRuntime(config, quiet=True)
    runtime.start()

    server = StdioMCPServer(runtime)

    # Handshake
    server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18"}})
    server.handle({"jsonrpc": "2.0", "method": "initialized"})

    def single_call(i):
        start = time.time()
        resp = server.handle({
            "jsonrpc": "2.0", "id": i + 100, "method": "tools/call",
            "params": {"name": "shell", "arguments": {"command": f"echo {i}"}}
        }, session_id=f"session-{i % 10}") # Parallel sessions
        return time.time() - start, resp is not None

    num_requests = 100 # Reduced for CI environment but still valid
    latencies = []
    success_count = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(single_call, i) for i in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            latency, success = future.result()
            latencies.append(latency)
            if success:
                success_count += 1

    latencies.sort()
    p50 = latencies[int(len(latencies) * 0.5)]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]
    error_rate = (num_requests - success_count) / num_requests

    report = f"""# PERFORMANCE REPORT
- Requests: {num_requests}
- Success: {success_count}
- Error Rate: {error_rate:.2%}
- Latency P50: {p50:.4f}s
- Latency P95: {p95:.4f}s
- Latency P99: {p99:.4f}s
"""
    with open("PERFORMANCE_REPORT.md", "w") as f:
        f.write(report)
    print(report)

    assert error_rate < 0.01

if __name__ == "__main__":
    test_stress_mcp()
