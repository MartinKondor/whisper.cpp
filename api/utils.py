from typing import List


def format_output(stdout: str) -> List[str]:
    lines = stdout.splitlines()
    return [line for line in lines if line.strip()]
