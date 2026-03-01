import pytest

from src.decorators import log


def test_log_console_success(capsys):
    @log()
    def add(a, b):
        return a + b

    result = add(2, 3)
    assert result == 5
    captured = capsys.readouterr()
    out = captured.out
    assert "CALL: add" in out
    assert "RETURN: add" in out
    assert "5" in out


def test_log_console_exception(capsys):
    @log()
    def fail(x):
        raise ValueError("bad")

    with pytest.raises(ValueError):
        fail(10)

    captured = capsys.readouterr()
    out = captured.out
    assert "CALL: fail" in out
    assert "ERROR: fail" in out
    assert "ValueError" in out
    assert "10" in out


def test_log_file_success(tmp_path):
    logfile = tmp_path / "log.txt"

    @log(filename=str(logfile))
    def mul(a, b):
        return a * b

    assert mul(4, 5) == 20
    content = logfile.read_text(encoding="utf-8")
    assert "CALL: mul" in content
    assert "RETURN: mul" in content
    assert "20" in content


def test_log_file_exception(tmp_path):
    logfile = tmp_path / "log2.txt"

    @log(filename=str(logfile))
    def fail2(a):
        raise RuntimeError("oops")

    with pytest.raises(RuntimeError):
        fail2("x")

    content = logfile.read_text(encoding="utf-8")
    assert "CALL: fail2" in content
    assert "ERROR: fail2" in content
    assert "RuntimeError" in content
    assert "x" in content
