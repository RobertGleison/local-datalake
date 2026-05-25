import os
import logging
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Safe logger resolution that works both inside Dagster worker pods
# and in standalone local execution environments (unit tests, manual scripts)
try:
    from dagster import get_dagster_logger
    logger = get_dagster_logger()
except Exception:
    logger = logging.getLogger("dagster")

class DLTSettings(BaseSettings):
    """
    Settings to configure execution parameters, logical CPU threads,
    and concurrent worker resources for dlt extract, normalize, and load phases.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    available_threads: int = Field(
        default_factory=lambda: os.cpu_count() or 1,
        description="Number of available logical CPUs",
    )

    extract_workers: int = Field(
        default=1,
        description="Number of workers for dlt extraction",
    )

    normalize_workers: int = Field(
        default=1,
        description="Number of workers for dlt normalization.",
    )

    load_workers: int = Field(
        default=1,
        description="Number of workers for load dlt process",
    )

    @model_validator(mode="after")
    def check_dlt_data_dir(self) -> "DLTSettings":
        if not os.environ.get("DLT_DATA_DIR"):
            logger.debug("DLT_DATA_DIR should be set on tenants that are using DLT")
        return self

    @model_validator(mode="after")
    def set_extract_workers(self) -> "DLTSettings":
        if not os.environ.get("EXTRACT__WORKERS"):
            self.extract_workers = max(1, self.available_threads - 1)
            os.environ["EXTRACT__WORKERS"] = str(self.extract_workers)
        else:
            self.extract_workers = int(os.environ["EXTRACT__WORKERS"])
        return self

    @model_validator(mode="after")
    def set_normalize_workers(self) -> "DLTSettings":
        if not os.environ.get("NORMALIZE__WORKERS"):
            self.normalize_workers = max(1, self.available_threads - 2)
            os.environ["NORMALIZE__WORKERS"] = str(self.normalize_workers)
        else:
            self.normalize_workers = int(os.environ["NORMALIZE__WORKERS"])
        return self

    @model_validator(mode="after")
    def set_load_workers(self) -> "DLTSettings":
        if not os.environ.get("LOAD__WORKERS"):
            self.load_workers = max(1, self.available_threads - 1)
            os.environ["LOAD__WORKERS"] = str(self.load_workers)
        else:
            self.load_workers = int(os.environ["LOAD__WORKERS"])
        return self
