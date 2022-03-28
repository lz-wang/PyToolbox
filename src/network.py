import socket

import requests
from loguru import logger as log


def get_internal_ip():
    ip = ''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        log.success(f'Get internal IP SUCCESS, IP={ip}')
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
        log.success(f'Get external IP SUCCESS, IP={ip}')
    except Exception as e:
        log.error(f'Get external IP FAILED, detail: {e}')
    finally:
        return ip


if __name__ == "__main__":
    get_internal_ip()
    get_external_ip()
