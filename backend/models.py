from pydantic import BaseModel
from typing import Dict, Any

class KeyGenerationResponse(BaseModel):
    private_key: str
    public_key: str

class EncryptRequest(BaseModel):
    text: str
    public_key: str  # The RSA public key to wrap the AES key

class EncryptResponse(BaseModel):
    pipeline: Dict[str, Any]
    ciphertext_base64: str
    wrapped_key_base64: str
    nonce_base64: str

class DecryptRequest(BaseModel):
    private_key: str
    ciphertext_base64: str
    wrapped_key_base64: str
    nonce_base64: str

class DecryptResponse(BaseModel):
    plaintext: str
    pipeline: Dict[str, Any]
