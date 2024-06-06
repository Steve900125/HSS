import numpy as np
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import os
from HSS_Gen import HSS_Gen

# PRF 函數
def PRF(K, id_i):
    seed = (int.from_bytes(K, 'big') + id_i[0] + id_i[1]) % (2**32)
    np.random.seed(seed)
    return np.random.randint(0, 2**15)

# PKE.OKDM 函數
def PKE_OKDM(pk, keyword, j, K):
    public_key = serialization.load_pem_public_key(pk)
    # 基於 keyword 和 j 生成鍵依賴消息
    key_dependent_message = f"{keyword}_{PRF(K, (len(keyword), j))}".encode()
    # 使用 RSA 公鑰加密
    ciphertext = public_key.encrypt(
        key_dependent_message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

# HSS 加密函數
def HSS_Enc(pk, keywords, K):
    d = len(keywords)  # 關鍵詞的數量
    ciphertexts = []
    for j, keyword in enumerate(keywords):
        # 使用 PKE.OKDM 加密每個關鍵詞
        ciphertext = PKE_OKDM(pk, keyword, j, K)
        ciphertexts.append(ciphertext)
    return ciphertexts

if __name__ == "__main__":
    # 安全參數 λ
    lambda_security = 16  # 示例安全參數（16 byte）

    # 呼叫 HSS_Gen 函數生成密鑰
    pk, ek0, ek1, sk = HSS_Gen(lambda_security)
    
    print(f'公鑰 (pk): {pk}')
    print(f'加密密鑰 ek0: {ek0}')
    print(f'加密密鑰 ek1: {ek1}')

    # 示例關鍵詞
    keywords = ["keyword1", "keyword2", "keyword3", "keyword4"]

    # 執行 HSS 加密
    ciphertexts = HSS_Enc(pk, keywords, ek0[0])
    print(f'密文: {ciphertexts}')
