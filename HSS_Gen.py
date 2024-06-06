import numpy as np
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# 生成 PRF 密鑰
def generate_prf_key(lambda_security):
    return os.urandom(lambda_security)

# 公鑰加密密鑰生成函數
def PKE_Gen(lambda_security):
    # 生成 RSA 公私鑰對
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,  # 安全參數對應的密鑰大小
    )
    public_key = private_key.public_key()

    # 序列化公鑰以便存儲或傳輸
    pk = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # 序列化私鑰以便存儲或傳輸
    sk = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )

    return pk, sk

# HSS 密鑰生成函數
def HSS_Gen(lambda_security):
    # 生成公鑰和秘密密鑰對 (pk, s)
    pk, sk = PKE_Gen(lambda_security)

    # 生成 PRF 密鑰 K
    K = generate_prf_key(lambda_security)

    # 參數設置
    d = 10  # 密鑰向量的維度
    q = 2**15  # 模數

    # 從 Z_q^d 中均勻採樣 s0
    s0 = np.random.randint(0, q, size=d)

    # 生成秘密密鑰 s
    s = np.random.randint(0, q, size=d)

    # 定義 s1 = s - s0 mod q
    s1 = (s - s0) % q

    # 定義 ek0 和 ek1
    ek0 = (K, s0)
    ek1 = (K, s1)

    return pk, ek0, ek1, sk

if __name__ == "__main__":
    # 安全參數 λ
    lambda_security = 16  # 示例安全參數（16 byte）

    # 生成密鑰
    pk, ek0, ek1, sk = HSS_Gen(lambda_security)
    
    print(f'公鑰 (pk): {pk}')
    print(f'加密密鑰 ek0: {ek0}')
    print(f'加密密鑰 ek1: {ek1}')
