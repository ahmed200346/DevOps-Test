"""Déploiement planifié des flows du pipeline MLOps."""
from prefect import serve
from prefect.client.schemas.schedules import CronSchedule

from pipeline_prefect import flow_all, flow_train, flow_evaluate

if __name__ == "__main__":
    deployment_all = flow_all.to_deployment(
        name="ml-pipeline-all",
        schedules=[CronSchedule(cron="0 2 * * *", timezone="Africa/Tunis")],
        tags=["mlops", "full-pipeline"],
    )
    deployment_train = flow_train.to_deployment(
        name="ml-pipeline-train",
        tags=["mlops", "train"],
    )
    deployment_evaluate = flow_evaluate.to_deployment(
        name="ml-pipeline-evaluate",
        tags=["mlops", "evaluate"],
    )

    serve(deployment_all, deployment_train, deployment_evaluate)
