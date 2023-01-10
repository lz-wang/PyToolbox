import os
import hashlib
import pathlib
import datetime

import chardet


class File(object):
    BUF_SIZE = 65536  # read stuff in 64kb chunks

    def __init__(self, filepath: str):
        self.path = filepath
        self._exists = os.path.isfile(filepath)
        self._stat = pathlib.Path(filepath).stat() if self._exists else None

    @property
    def dir(self):
        return os.path.dirname(self.path)

    @property
    def name(self):
        return os.path.basename(self.path)

    def _hash(self, algorithm: str):
        match algorithm:
            case 'md5':
                hash_func = hashlib.md5()
            case 'sha1':
                hash_func = hashlib.sha1()
            case 'sha224':
                hash_func = hashlib.sha224()
            case 'sha256':
                hash_func = hashlib.sha256()
            case 'sha384':
                hash_func = hashlib.sha384()
            case 'sha512':
                hash_func = hashlib.sha512()
            case _:
                raise
        with open(self.path, 'rb') as f:
            while True:
                data = f.read(self.BUF_SIZE)
                if not data:
                    break
                hash_func.update(data)
        return hash_func.hexdigest()

    @property
    def md5(self):
        return self._hash('md5') if self._exists else None

    @property
    def sha1(self):
        return self._hash('sha1') if self._exists else None

    @property
    def sha224(self):
        return self._hash('sha224') if self._exists else None

    @property
    def sha256(self):
        return self._hash('sha256') if self._exists else None

    @property
    def sha384(self):
        return self._hash('sha384') if self._exists else None

    @property
    def sha512(self):
        return self._hash('sha512') if self._exists else None

    @property
    def creation_time(self):
        return datetime.datetime.fromtimestamp(self._stat.st_birthtime) if self._exists else None

    @property
    def last_modified(self):
        return datetime.datetime.fromtimestamp(self._stat.st_mtime) if self._exists else None

    def is_binary(self) -> bool:
        """判断文件是否是二进制文件"""
        chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
        file_slices = open(self.path, 'rb').read(1024)
        return bool(file_slices.translate(None, chars))

    def get_encoding(self) -> str:
        """获取文件的编码格式"""
        if self.is_binary():
            raise TypeError(f'"{self.path}" is a binary file, cannot get its encoding')
        detector = chardet.UniversalDetector()
        detector.reset()
        for line in open(self.path, 'rb'):
            detector.feed(line)
            if detector.done:
                break
        detector.close()

        return detector.result.get('encoding')
