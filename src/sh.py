import subprocess
from loguru import logger as log


def run_cmd(cmd: list, show_cmd: bool = True, show_results: bool = True):
    """Example: cmd=['echo', 'hello world']"""
    if show_cmd:
        log.info(f"[run shell cmd] {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    out = stdout.decode("utf-8").strip()
    err = stderr.decode("utf-8").strip()
    if show_results:
        if err:
            log.warning(f'[run shell cmd] STD_ERR: \n{err}')
        if out:
            log.success(f'[run shell cmd] STD_OUT, output: \n{out}')
    return out, err
