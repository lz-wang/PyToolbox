import socket

import requests
from loguru import logger as log


def get_internal_ip():
    ip = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception as e:
        log.error(f'Get internal IP FAILED, detail: {e}')
    finally:
        s.close()
        return ip


def get_external_ip():
    ip = ''
    try:
        response = requests.get('https://ifconfig.me/ip', timeout=3)
        ip = response.text.strip()
    except Exception as e:
        log.error(f'Get external IP FAILED, detail: {e}')
    finally:
        return ip


if __name__ == "__main__":
    print(f'External IP: {get_external_ip()}')
    print(f'Internal IP: {get_internal_ip()}')
