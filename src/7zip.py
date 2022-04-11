import os
import traceback
from pathlib import Path

import py7zr
from loguru import logger as log


def compress_7zip(src: str, dst_dir: str = None,
                  target_file: str = None, password: str = None):
    """对指定目录的文件或文件夹进行 7z 形式的压缩

    Args:
        src: 指定的文件夹或者文件目录
        dst_dir: 压缩后的文件所在的目录
        target_file: 压缩后的文件名称
        password: 密码

    Returns:
        压缩成功或失败
    """
    try:
        dst_dir = src if not dst_dir else dst_dir
        src_path = Path(src)
        dst_path = Path(dst_dir)
        if not target_file:
            target_file = os.path.join(dst_path.parent, f'{src_path.name}.7z')
        if not target_file.endswith('7z'):
            target_file = f'{target_file}.7z'
        with py7zr.SevenZipFile(file=target_file, mode='w', password=password) as archive:
            archive.writeall(path=dst_dir, arcname=src_path.name)
        log.success(f'Compress "{src}" OK, compressed file: "{target_file}"!')
        return True
    except Exception as e:
        log.error(f'Compress "{src}" Failed, detail: {e}')
        log.error(traceback.format_exc())
        return False


def uncompress_7zip(target_file: str, dst_dir: str = None, password: str = None):
    """解压指定的 7z 压缩文件

    Args:
        target_file: 指定的 7z 压缩文件
        dst_dir: 解压后的位置
        password: 解压密码

    Returns:
        解压成功或失败
    """
    if not target_file.endswith('7z'):
        return False
    try:
        src_path = Path(target_file)
        dst_dir = src_path.parent if not dst_dir else dst_dir
        with py7zr.SevenZipFile(file=target_file, mode='r', password=password) as unarchive:
            unarchive.extractall(path=dst_dir)
        dst_path = os.path.join(dst_dir, src_path.name)
        log.success(f'Uncompress "{target_file}" OK, uncompressed path: "{dst_path}"')
        return True
    except Exception as e:
        log.error(f'Uncompress "{target_file}" Failed, detail: {e}')
        log.error(traceback.format_exc())
        return False
