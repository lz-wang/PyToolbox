import hashlib
import os.path
import pathlib
from functools import partial
from pathlib import Path
from typing import List

import chardet
from loguru import logger as log


def get_file_md5sum(file_path: str) -> str:
    """获取文件的md5哈希值"""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f'cannot found file: {file_path}')
    with open(file_path, 'rb') as f:
        md5hash = hashlib.md5()
        for buffer in iter(partial(f.read, 128), b''):
            md5hash.update(buffer)
        return md5hash.hexdigest()


def touch_empty_file(file_name: str = '.tmp', file_dir: str = '') -> str:
    """在指定目录创建空文件"""
    if not os.path.exists(file_dir):
        file_dir = os.environ['HOME']
    file_path = os.path.join(file_dir, file_name)
    pathlib.Path(file_path).touch(exist_ok=True)
    return file_path


def is_image_file(file: str, ignore_hidden_file: bool = True) -> bool:
    """根据文件名后缀判断是否是图片文件"""
    try:
        file_name = file.split('/')[-1]
        if file_name.startswith('.') and ignore_hidden_file:
            return False
        file_suffix = file.split('.')[-1]
        image_types = ['png', 'jpg', 'gif', 'bmp', 'tif', 'svg', 'webp']
        if file_suffix in image_types:
            return True
        else:
            return False
    except Exception as e:
        log.warning(e)
        return False


def get_encoding(file: str) -> str:
    """获取文件的正确编码格式"""
    detector = chardet.UniversalDetector()
    detector.reset()
    for line in open(file, 'rb'):
        detector.feed(line)
        if detector.done:
            break
    detector.close()
    log.info(f'file: {file}, {detector.result}')

    return detector.result.get('encoding')


def find_files(target_path: str,
               ignore_hidden_file: bool = False,
               ignore_hidden_dir: bool = True) -> List[str]:
    """获取指定目录及其子目录下的所有文件列表

    Args:
        target_path: 指定的目录
        ignore_hidden_file: 是否忽略隐藏文件
        ignore_hidden_dir: 是否忽略隐藏文件夹

    Returns:
        指定目录及其子目录下的文件列表
    """
    if not os.path.exists(target_path):
        return []

    if os.path.isdir(target_path):
        file_list = []
        for root, dirs, files in os.walk(target_path):
            rp = Path(root)
            if ignore_hidden_dir and rp.name.startswith('.'):
                continue
            for file in files:
                if ignore_hidden_file:
                    if not file.startswith('.'):
                        file_list.append(os.path.join(root, file))
                else:
                    file_list.append(os.path.join(root, file))

        return file_list

    if os.path.isfile(target_path):
        return [target_path]


def list_dirs(target_path: str) -> List[str]:
    """列出定目录下所有文件夹（非递归）

    Args:
        target_path: 目标文件夹

    Returns:
        指定目录下的所有文件夹（全路径）
    """
    if not os.path.exists(target_path):
        return []
    if not os.path.isdir(target_path):
        return []
    all_paths = [os.path.join(target_path, p) for p in os.listdir(target_path)]
    return [d for d in all_paths if os.path.isdir(d)]


def list_files(target_path: str, ignore_hidden_file: bool = False) -> List[str]:
    """列出定目录下所有文件（非递归）

    Args:
        target_path: 目标文件夹
        ignore_hidden_file: 是否忽略隐藏文件

    Returns:
        指定目录下的所有文件（全路径）
    """
    if not os.path.exists(target_path):
        return []
    if not os.path.isdir(target_path):
        return []
    all_paths = [os.path.join(target_path, p) for p in os.listdir(target_path)]
    if ignore_hidden_file:
        return [d for d in all_paths if os.path.isfile(d) and not d.startswith('.')]
    else:
        return [d for d in all_paths if os.path.isfile(d)]
