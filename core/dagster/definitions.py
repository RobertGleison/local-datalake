from dagster import Definitions
from core.dagster.assets import bronze_summoner_data
from core.dagster.jobs import bronze_ingestion_job
from core.dagster.schedules import bronze_ingestion_daily
from core.dagster.resources import LakeResource, DLTResource, MinioResource

defs = Definitions(
    assets=[bronze_summoner_data],
    jobs=[bronze_ingestion_job],
    schedules=[bronze_ingestion_daily],
    resources={
        "lake": LakeResource(),
        "dlt": DLTResource(),
        "minio": MinioResource(),
    },
)
