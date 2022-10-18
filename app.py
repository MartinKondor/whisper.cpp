from typing import Dict

from fastapi import FastAPI

from api.response import PrettyJSONResponse
from api.terminal import run_whisper, run_process


app = FastAPI()


@app.get("/")
def root_route(
    f: str="",
    return_stderr: int=0
) -> Dict:
    return run_whisper(f, return_stderr)


@app.get("/pretty", response_class=PrettyJSONResponse)
def root_pretty_route(
    f: str="",
    return_stderr: int=0
) -> Dict:
    return run_whisper(f, return_stderr)


@app.get("/ls", response_class=PrettyJSONResponse)
def ls_route(
    lib: str=""
) -> Dict:
    ls = run_process(f"ls {lib}")
    return {
        "status": "ok",
        "stdout": ls.stdout.read().decode("utf-8"),
        "stderr": ls.stderr.read().decode("utf-8")
    }
