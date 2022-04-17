"""
References: https://pycryptodome.readthedocs.io/en/latest/index.html
"""
from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_cbc_encrypt(public_text: str, key: bytes, iv: bytes = None) -> str:
    """

    Args:
        public_text: 需要加密的字符串
        key: 加密用的key
        iv: CBC偏移量，默认使用key的后16位

    Returns:
        加密后的字符串
    """
    iv = key[:AES.block_size] if not iv else iv
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    ct_bytes = cipher.encrypt(pad(public_text.encode("utf-8"), AES.block_size))

    return b64encode(ct_bytes).decode('utf-8')


def aes_cbc_decrypt(cipher_text: str, key: bytes, iv: bytes = None) -> str:
    """

    Args:
        cipher_text: 需要解密的字符串
        key: 解密的key（与加密的key必须相同）
        iv: CBC偏移量，默认使用key的后16位

    Returns:
        加密后的字符串
    """
    iv = key[:AES.block_size] if not iv else iv
    ct = b64decode(cipher_text)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)

    return pt.decode('utf-8')
