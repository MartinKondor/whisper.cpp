from subprocess import PIPE, Popen
from typing import Dict 
import time
import os

from api.utils import format_output


WHISPER_BIN = "./main --model models/ggml-base.en.bin "

"""
Examples:
>>> run_process("ls")
>>> run_process("ls -la")

:cmd: Command to run
"""
def run_process(cmd: str):
    return Popen([str(cmd)], stdout=PIPE, stderr=PIPE, shell=True)


"""
Downloads the inputed file from a web source with curl
"""
def download_file(
    input_file_name: str,
    output_file_name: str="download.wav",
    verbose: bool=False
) -> str:
    if verbose:
        print("[*] download_file ...")

    output = run_process(f"curl -o {output_file_name} {input_file_name}")
    output.communicate()
    return output_file_name


"""
Converts a file to the desired 16 bitrate
which is supported by whisper
"""
def convert_to_16bit(
    input_file_name: str,
    output_file_name: str="output.wav",
    verbose: bool=False
) -> str:
    if verbose:
        print("[*] convert_to_16bit ...")

    output = run_process(f"ffmpeg -y -i {input_file_name} -ar 16000 -ac 1 {output_file_name}")
    output.communicate()
    return output_file_name


"""
:input_file_name:
:return_stderr:
:remove_files_after_use:
:verbose: Send log to the console or not
:returns: dict
... The return will always contain a key "status",
... if the status is 1 then the command run down
... smoothly, otherwise if it is 0 then then there
... was an error and the error message is in under
... the "msg" key.
"""
def run_whisper(
    input_file_name: str,
    return_stderr: int=0,
    verbose: bool=True
) -> Dict:
    start_time = time.time()

    # Check input file
    if not input_file_name:
        return {
            "status": 0,
            "msg": "No input file provided"
        }
    
    if not os.path.exists(input_file_name):
        return {
            "status": 0,
            "msg": f"Input file not found {input_file_name}"
        }

    # Remove previous output
    if os.path.exists("output.wav"):
        os.remove("output.wav")

    if "://" in input_file_name:
        input_file_name = download_file(input_file_name)
        if not os.path.exists("download.wav"):
            return {
                "status": 0,
                "msg": "curl error"
            }

    input_file_name = convert_to_16bit(input_file_name)
    if not os.path.exists(input_file_name):
        return {
            "status": 0,
            "msg": "ffmpeg error"
        }

    # Startup whisper
    if verbose:
        print("[*] whisper ...")

    output = run_process(WHISPER_BIN + input_file_name)
    stdout = output.stdout.read().decode("utf-8")
    stderr = output.stderr.read().decode("utf-8")
    output.communicate()
    response = {
        "status": 1,
        "output": format_output(stdout),
        "runtime": time.time() - start_time
    }

    if return_stderr == 1:
        response["stderr"] = stderr
    return response
