from typing import Union
from subprocess import PIPE, Popen
from typing import Dict
import os

from fastapi import FastAPI

from api_src.pretty_json_response import PrettyJSONResponse


app = FastAPI()
WHISPER_BIN = "./main --model models/ggml-base.en.bin "


def download_file(
    input_file_name: str,
    output_file_name: str="download.wav",
    verbose: bool=True
) -> str:
    if verbose:
        print("[*] curl ...")

    output = Popen(
        [f"curl -o {output_file_name} {input_file_name}"],
        stdout=PIPE,
        stderr=PIPE,
        shell=True)
    stdout = output.stdout.read().decode("utf-8")
    stderr = output.stderr.read().decode("utf-8")
    output.communicate()
    
    if verbose:
        print(stdout)
        print(stderr)
        print("[*] curl ... done")
    return output_file_name


def convert_to_16bit(
    input_file_name: str,
    output_file_name: str="output.wav",
    verbose: bool=True
) -> str:
    if verbose:
        print("[*] ffmpeg ...")

    output = Popen(
        # [f"ffmpeg -y -i {input_file_name} -ar 16000 -ac 1 -c:ax pcm_s16le {output_file_name}"],
        [f"ffmpeg -y -i {input_file_name} -ar 16000 -ac 1 {output_file_name}"],
        stdout=PIPE,
        stderr=PIPE,
        shell=True)
    stdout = output.stdout.read().decode("utf-8")
    stderr = output.stderr.read().decode("utf-8")
    output.communicate()

    if verbose:
        print(stdout)
        print(stderr)
        print("[*] ffmpeg ... done")
    return output_file_name


def remove_temp_files() -> None:
    if os.path.exists("download.wav"):
        os.remove("download.wav")
    if os.path.exists("output.wav"):
        os.remove("output.wav")


def exec_command(
    input_file_name: str,
    return_stderr: int=0,
    remove_files_after_use: bool=False,
    verbose: bool=True
) -> Dict:

    # Sample inputs:
    # "bin/samples/jfk.wav"
    # "bin/samples/talkin.wav"
    # "bin/samples/longtalkin.wav"

    if os.path.exists("output.wav"):
        os.remove("output.wav")

    if verbose:
        print("[*] input_file_name =", input_file_name)

    if not input_file_name:
        return {"status": "No input file provided"}

    if "://" in input_file_name:
        input_file_name = download_file(input_file_name)
        if not os.path.exists("download.wav"):
            return {"status": "curl error",}

    if not os.path.exists(input_file_name):
        return {"status": f"Input file not found {input_file_name}"}

    input_file_name = convert_to_16bit(input_file_name)
    if not os.path.exists(input_file_name):
        return {"status": "ffmpeg error"}

    # Whisper
    if verbose:
        print("[*] whisper ...")
    output = Popen(
        [WHISPER_BIN + input_file_name],
        stdout=PIPE,
        stderr=PIPE,
        shell=True)
    stdout = output.stdout.read().decode("utf-8")
    stderr = output.stderr.read().decode("utf-8")
    output.communicate()

    if verbose:
        print("[*] whisper done...")

    if remove_files_after_use:
        remove_temp_files()

    if return_stderr == 1:
        return {
            "status": "ok",
            "stdout": stdout,
            "stderr": stderr
        }
    return {
        "status": "ok",
        "stdout": stdout,
    }


@app.get("/")
def root_route(
    f: str="",
    return_stderr: int=0
) -> Dict:
    return exec_command(f, return_stderr)


@app.get("/ls", response_class=PrettyJSONResponse)
def ls_route(
    lib: str=""
) -> Dict:
    ls = Popen([f"ls {lib}"], stdout=PIPE, stderr=PIPE, shell=True)
    return {
        "status": "ok",
        "stdout": ls.stdout.read().decode("utf-8"),
        "stderr": ls.stderr.read().decode("utf-8")
    }


@app.get("/pretty", response_class=PrettyJSONResponse)
def root_pretty_route(
    f: str="",
    return_stderr: int=0
) -> Dict:
    return exec_command(f, return_stderr)
