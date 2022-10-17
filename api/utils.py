from typing import List


def format_output(stdout: str) -> List[str]:
    subtitles = stdout.split("\n")
    return [s for s in subtitles if s.strip()]
