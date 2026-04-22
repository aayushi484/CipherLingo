from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import base64

from models import KeyGenerationResponse, EncryptRequest, EncryptResponse, DecryptRequest, DecryptResponse
from crypto_utils import CryptoManager
from linguistic_engine import LinguisticEngine

app = FastAPI(title="Linguistic Encryption System API", version="1.0.0")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for hackathon/local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

linguistic_engine = LinguisticEngine()

@app.get("/")
def health_check():
    return {"status": "Secure linguistic core online"}

@app.get("/profiles")
def get_profiles():
    return {"message": "Universal Polyglot Cipher Active"}

@app.post("/generate-keys", response_model=KeyGenerationResponse)
def generate_keys():
    """Generates standard RSA-2048 keypairs for the frontend client."""
    try:
        priv_key, pub_key = CryptoManager.generate_rsa_keypair()
        return KeyGenerationResponse(private_key=priv_key, public_key=pub_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/encrypt", response_model=EncryptResponse)
def encrypt_message(req: EncryptRequest):
    try:
        import os
        pipeline = {}
        
        # Generate AES Nonce here to seed the Linguistic transform
        nonce = os.urandom(12)
        
        # 1. Linguistic Transform using Nonce
        linguistic_text = linguistic_engine.transform(req.text, nonce)
        pipeline["step_1_polyglot_linguistic"] = linguistic_text
        
        # 2. AES-GCM Encrypt
        aes_key, _, ciphertext = CryptoManager.encrypt_aes_gcm(linguistic_text.encode('utf-8'), nonce)
        
        # Convert AES results directly to base64 for transport/storage
        ciphertext_b64 = base64.b64encode(ciphertext).decode('utf-8')
        nonce_b64 = base64.b64encode(nonce).decode('utf-8')
        
        pipeline["step_2_aes_ciphertext_base64"] = ciphertext_b64
        pipeline["step_2_aes_key_base64"] = base64.b64encode(aes_key).decode('utf-8')
        
        # 3. Wrap AES Key with RSA
        wrapped_key = CryptoManager.encrypt_rsa(req.public_key, aes_key)
        wrapped_key_b64 = base64.b64encode(wrapped_key).decode('utf-8')
        
        pipeline["step_3_rsa_wrapped_key"] = wrapped_key_b64
        
        # 4. Package Sequence
        pipeline["step_4_package_sequence"] = True
        
        return EncryptResponse(
            pipeline=pipeline,
            ciphertext_base64=ciphertext_b64,
            wrapped_key_base64=wrapped_key_b64,
            nonce_base64=nonce_b64
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Encryption failed: {str(e)}")

@app.post("/decrypt", response_model=DecryptResponse)
def decrypt_message(req: DecryptRequest):
    try:
        pipeline = {}
        
        ciphertext = base64.b64decode(req.ciphertext_base64)
        nonce = base64.b64decode(req.nonce_base64)
        wrapped_key = base64.b64decode(req.wrapped_key_base64)
        
        # 1. Payload verified via structural unpack
        pipeline["step_1_payload_unpacking"] = True
        
        # 2. RSA Unwrap Key
        aes_key = CryptoManager.decrypt_rsa(req.private_key, wrapped_key)
        pipeline["step_2_rsa_unwrapped_key_b64"] = base64.b64encode(aes_key).decode('utf-8')
        
        # 3. AES-GCM Decrypt
        linguistic_bytes = CryptoManager.decrypt_aes_gcm(aes_key, nonce, ciphertext)
        linguistic_text = linguistic_bytes.decode('utf-8')
        pipeline["step_3_aes_decrypted_linguistic"] = linguistic_text
        
        # 4. Linguistic Inverse Transform
        plaintext = linguistic_engine.inverse_transform(linguistic_text, nonce)
        pipeline["step_4_final_plaintext"] = plaintext
        
        return DecryptResponse(
            plaintext=plaintext,
            pipeline=pipeline
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")
