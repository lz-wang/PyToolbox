from Crypto.Random import get_random_bytes

from src.aes import aes_cbc_encrypt, aes_cbc_decrypt

TEST_KEY = "abcdefghijklmnop".encode("utf-8")
TEST_PT = "hello world"
TEST_CT = '1dGGFwB4VKhqD6jGCIwT7Q=='


def test_aes_cbc_encrypt():
    assert aes_cbc_encrypt(TEST_PT, TEST_KEY) == TEST_CT


def test_aes_cbc_decrypt():
    assert aes_cbc_decrypt(TEST_CT, TEST_KEY) == TEST_PT


def test_aes_cbc_all():
    test_key = get_random_bytes(16)
    test_str = "python is good"
    ct = aes_cbc_encrypt(test_str, test_key)
    pt = aes_cbc_decrypt(ct, test_key)
    assert pt == test_str
