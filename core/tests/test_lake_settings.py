import os
from core.settings.lake_settings import LakeSettings


def test_lake_settings_defaults():
    """Verify built-in connection url string builders in LakeSettings."""
    settings = LakeSettings()

    assert settings.clickhouse_host == "clickhouse"
    assert settings.clickhouse_http_port == 8123
    assert settings.clickhouse_native_port == 9000
    assert settings.clickhouse_user == "default"
    assert settings.clickhouse_password.get_secret_value() == ""
    assert settings.clickhouse_database == "default"
    assert settings.clickhouse_http_url == "http://default@clickhouse:8123/default"
    assert settings.clickhouse_native_url == "clickhouse://clickhouse:9000/default"
    assert settings.cloudbeaver_host == "cloudbeaver"
    assert settings.cloudbeaver_port == 8978
    assert settings.cloudbeaver_url == "http://cloudbeaver:8978"


def test_lake_settings_env_overrides():
    """Verify custom env overrides change urls and properties."""
    os.environ["CLICKHOUSE_HOST"] = "192.168.1.50"
    os.environ["CLICKHOUSE_HTTP_PORT"] = "9080"
    os.environ["CLICKHOUSE_NATIVE_PORT"] = "9443"
    os.environ["CLICKHOUSE_USER"] = "admin"
    os.environ["CLICKHOUSE_PASSWORD"] = "my-secret-password-123"
    os.environ["CLICKHOUSE_DATABASE"] = "bronze_db"
    os.environ["CLOUDBEAVER_HOST"] = "editor.local"
    os.environ["CLOUDBEAVER_PORT"] = "8080"

    settings = LakeSettings()

    assert settings.clickhouse_host == "192.168.1.50"
    assert settings.clickhouse_http_port == 9080
    assert settings.clickhouse_native_port == 9443
    assert settings.clickhouse_user == "admin"
    assert settings.clickhouse_password.get_secret_value() == "my-secret-password-123"
    assert settings.clickhouse_database == "bronze_db"
    assert settings.clickhouse_http_url == "http://admin:my-secret-password-123@192.168.1.50:9080/bronze_db"
    assert settings.clickhouse_native_url == "clickhouse://192.168.1.50:9443/bronze_db"
    assert settings.cloudbeaver_host == "editor.local"
    assert settings.cloudbeaver_port == 8080
    assert settings.cloudbeaver_url == "http://editor.local:8080"
