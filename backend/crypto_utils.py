import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import base64

class CryptoManager:
    def __init__(self):
        pass

    @staticmethod
    def generate_rsa_keypair():
        """Generates a secure RSA-2048 keypair."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        
        # Serialize keys
        pem_private = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        pem_public = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return pem_private.decode('utf-8'), pem_public.decode('utf-8')

    @staticmethod
    def encrypt_aes_gcm(plaintext: bytes, nonce: bytes = None) -> tuple:
        """Encrypts data using AES-256-GCM and randomly generated key/nonce."""
        aes_key = AESGCM.generate_key(bit_length=256)
        aesgcm = AESGCM(aes_key)
        if nonce is None:
            nonce = os.urandom(12)
        
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return aes_key, nonce, ciphertext

    @staticmethod
    def decrypt_aes_gcm(aes_key: bytes, nonce: bytes, ciphertext: bytes) -> bytes:
        """Decrypts AES-GCM data."""
        aesgcm = AESGCM(aes_key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext

    @staticmethod
    def encrypt_rsa(public_key_pem: str, data: bytes) -> bytes:
        """Encrypts (wraps) a key or small data using RSA public key."""
        public_key = serialization.load_pem_public_key(public_key_pem.encode('utf-8'))
        ciphertext = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return ciphertext

    @staticmethod
    def decrypt_rsa(private_key_pem: str, ciphertext: bytes) -> bytes:
        """Decrypts data using RSA private key."""
        private_key = serialization.load_pem_private_key(
            private_key_pem.encode('utf-8'),
            password=None
        )
        plaintext = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return plaintext

    @staticmethod
    def compute_hash(data: bytes) -> str:
        """Computes SHA-256 hash for integrity verification."""
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data)
        return base64.b64encode(digest.finalize()).decode('utf-8')
