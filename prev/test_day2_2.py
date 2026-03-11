import pytest
import json
from day2_2 import load_config, validate_config


def test_load_config_reads_file(tmp_path):
    config_file = tmp_path / "config.json"

    data = {
        "host": "localhost",
        "port": 8000,
        "debug": False
    }

    config_file.write_text(json.dumps(data))

    result = load_config(config_file)

    assert result["host"] == "localhost"
    assert result["port"] == 8000
    assert result["debug"] is False


def test_env_overrides(tmp_path, monkeypatch):
    config_file = tmp_path / "config.json"

    data = {
        "host": "localhost",
        "port": 8000,
        "debug": False
    }

    config_file.write_text(json.dumps(data))

    monkeypatch.setenv("APP_PORT", "9000")
    monkeypatch.setenv("APP_DEBUG", "true")

    result = load_config(config_file)

    assert result["port"] == 9000
    assert result["debug"] is True


@pytest.mark.parametrize("config, expected_errors", [
    ({"host": "localhost", "port": 8000, "debug": True}, []),
    ({"host": "localhost", "port": 70000, "debug": True}, ["invalid port"]),
    ({"port": 8000, "debug": True}, ["missing host"]),
    ({"host": "localhost", "port": 8000, "debug": "yes"}, ["debug must be bool"]),
])
def test_validate_config(config, expected_errors):
    assert validate_config(config) == expected_errors