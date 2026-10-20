import argparse
from pathlib import Path
from prefect import flow, task, get_run_logger
import subprocess
import sys

PYTHON_BIN = sys.executable
BASE_DIR = Path(__file__).resolve().parent
MAIN_PY = BASE_DIR / "main.py"


def _run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def _run_report_only(cmd: list[str]) -> int:
    """Exécute la commande sans faire planter le flow, retourne le code de sortie."""
    result = subprocess.run(cmd)
    return result.returncode

@task(name="clone-or-pull-repo")
def fetch_repo() -> None:
    logger = get_run_logger()
    if not Path(".git").exists():
        _run(["git", "clone", "https://github.com/ahmed200346/DevOps-Test", "."])
    else:
        _run(["git", "pull"])
    logger.info("Repository up to date.")
@task(name="install-dependencies")
def install_dependencies() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), "-m", "pip", "install", "-r", "requirements.txt"])
    logger.info("Dependencies installed.")


@task(name="prepare-data")
def prepare_data() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), str(MAIN_PY), "--prepare"])
    logger.info("Data preparation complete.")


@task(name="train-model")
def train_model() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), str(MAIN_PY), "--train"])
    logger.info("Training complete.")


@task(name="save-model")
def save_model() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), str(MAIN_PY), "--save"])
    logger.info("Model saved.")


@task(name="load-model")
def load_model() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), str(MAIN_PY), "--load"])
    logger.info("Model loaded.")


@task(name="evaluate-model")
def evaluate_model() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), str(MAIN_PY), "--evaluate"])
    logger.info("Evaluation complete.")


@task(name="format-code")
def format_code() -> None:
    logger = get_run_logger()
    _run(
        [
            str(PYTHON_BIN),
            "-m",
            "black",
            str(BASE_DIR / "model_pipeline.py"),
            str(BASE_DIR / "main.py"),
            str(BASE_DIR / "pipeline_prefect.py"),
        ]
    )
    logger.info("Code formatted.")


@task(name="lint-code")
def lint_code() -> None:
    logger = get_run_logger()
    code = _run_report_only(
        [
            str(PYTHON_BIN),
            "-m",
            "pylint",
            str(BASE_DIR / "model_pipeline.py"),
            str(BASE_DIR / "main.py"),
            str(BASE_DIR / "pipeline_prefect.py"),
        ]
    )
    logger.info(f"Lint check complete (exit code {code}).")


@task(name="security-check")
def security_check() -> None:
    logger = get_run_logger()
    code = _run_report_only(
        [
            str(PYTHON_BIN),
            "-m",
            "bandit",
            str(BASE_DIR / "model_pipeline.py"),
            str(BASE_DIR / "main.py"),
            str(BASE_DIR / "pipeline_prefect.py"),
        ]
    )
    logger.info(f"Security check complete (exit code {code}).")


@task(name="unit-tests")
def unit_tests() -> None:
    logger = get_run_logger()
    _run([str(PYTHON_BIN), "-m", "pytest", str(BASE_DIR / "test_main.py")])
    logger.info("Unit tests passed.")

@task(name="run-api")
def run_api() -> None:
    logger = get_run_logger()
    subprocess.Popen([
        str(PYTHON_BIN), "-m", "uvicorn",
        "app:app", "--host", "0.0.0.0", "--port", "8000"
    ])
    logger.info("API FastAPI lancée en arrière-plan.")

@task(name="run-streamlit")
def run_streamlit() -> None:
    logger = get_run_logger()
    subprocess.Popen([
        str(PYTHON_BIN), "-m", "streamlit", "run",
        str(BASE_DIR / "streamlit_app.py"),
        "--server.port", "8501",
        "--server.address", "0.0.0.0"
    ])
    logger.info("Frontend Streamlit lancé.")

@flow(name="full-app", log_prints=True)
def flow_full_app() -> None:
    run_api()
    run_streamlit()

@flow(name="frontend", log_prints=True)
def flow_frontend() -> None:
    run_streamlit()

@flow(name="train", log_prints=True)
def flow_train() -> None:
    prepare_data()
    train_model()
    save_model()


@flow(name="evaluate", log_prints=True)
def flow_evaluate() -> None:
    load_model()
    evaluate_model()


@flow(name="code", log_prints=True)
def flow_code() -> None:
    format_code()
    lint_code()
    security_check()
    unit_tests()


@flow(name="all", log_prints=True)
def flow_all() -> None:
    install_dependencies()
    flow_code()
    prepare_data()
    train_model()
    save_model()
    evaluate_model()
@flow(name="api", log_prints=True)
def flow_api() -> None:
    run_api()

FLOWS = {
    "all": flow_all,
    "train": flow_train,
    "evaluate": flow_evaluate,
    "code": flow_code,
    "api": flow_api,
    "frontend": flow_frontend,
    "full-app": flow_full_app,
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--flow", required=True, choices=FLOWS.keys())
    args = parser.parse_args()
    FLOWS[args.flow]()
