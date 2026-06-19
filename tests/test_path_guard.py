import pytest
from pathlib import Path
from dgm_mcp.security.path_guard import PathGuard

def test_path_guard_allowed():
    allowed = [str(Path("./src").resolve())]
    pg = PathGuard(allowed)

    # Test safe path
    safe_path = Path("./src/dgm_mcp/main.py").resolve()
    assert pg.validate_path(safe_path) == safe_path
    assert pg.is_safe(safe_path) is True

def test_path_guard_disallowed():
    allowed = [str(Path("./src").resolve())]
    pg = PathGuard(allowed)

    # Test path traversal
    unsafe_path = Path("./tests/test_basic.py").resolve()
    with pytest.raises(PermissionError):
        pg.validate_path(unsafe_path)
    assert pg.is_safe(unsafe_path) is False

def test_path_guard_expanduser():
    # This might be tricky in CI, but let's test expansion
    # We use a path that we know where it will resolve
    pg = PathGuard(["~/allowed"])
    expected = Path("~/allowed").expanduser().resolve(strict=False)
    assert expected in pg.allowed_paths

def test_path_guard_relative_to():
    # Test that startswith bypass is prevented
    pg = PathGuard(["/tmp/safe"])

    with pytest.raises(PermissionError):
        pg.validate_path("/tmp/safe-secret")

    # Note: in real env /tmp/safe might not exist, but resolve(strict=False) handles it
    assert pg.validate_path("/tmp/safe/file.txt") == Path("/tmp/safe/file.txt").resolve(strict=False)
