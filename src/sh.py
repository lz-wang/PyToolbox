import subprocess
from loguru import logger as log


def run_cmd(cmd: list):
    """Example: cmd=['echo', 'hello world']"""
    log.info(f"[run shell cmd] {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    out = stdout.decode("utf-8")
    err = stderr.decode("utf-8")
    if err:
        log.error(f'[run shell cmd] Failed, detail: \n{err}')
    if out:
        log.success(f'[run shell cmd] OK, output: \n{out}')
    return out, err
