import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# References used for cryptography structure :
# PBKDF2HMAC: https://cryptography.io/en/latest/hazmat/primitives/key-derivation-functions/
# AES-GCM: https://cryptography.io/en/latest/hazmat/primitives/aead/
# PBKDF2:  https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
class SecurityManager:
    # Crypto Constants
    _SALT_SIZE = 16
    _NONCE_SIZE = 12
    _KEY_SIZE = 32  
    _PBKDF2_ITERATIONS = 600_000
    _MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def _derive_key_from_password(password, salt):
        # Password and Salt through PBKDF2 for key generations
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=SecurityManager._KEY_SIZE,
            salt=salt,
            iterations=SecurityManager._PBKDF2_ITERATIONS,
        )
        return kdf.derive(password.encode("utf-8"))
    
    @staticmethod
    def _validate_password(password):
        # Check password length meets minimums
        return len(password) >= SecurityManager._MIN_PASSWORD_LENGTH
    
    @staticmethod
    def _handle_encryption_error(error):
        print(f"Encryption error: {error}")
    
    @staticmethod
    def _handle_decryption_error(error):
        print("Decryption failed.")
    
    @staticmethod
    def encrypt_note(plaintext, password):
        if not SecurityManager._validate_password(password):
            SecurityManager._handle_encryption_error("Password does not meet minimum requirements")
            return None
        try:
            # Random salt and nonce for every new note
            salt = os.urandom(SecurityManager._SALT_SIZE)
            nonce = os.urandom(SecurityManager._NONCE_SIZE)
            # Turn the password into AES key
            key = SecurityManager._derive_key_from_password(password, salt)
            # Encrypt with AES-256-GCM
            aesgcm = AESGCM(key)
            ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
            # Concatinate salt + nonce + ciphertext for decryption later
            return salt + nonce + ciphertext
        except Exception as e:
            SecurityManager._handle_encryption_error(e)
            return None
    
    @staticmethod
    def decrypt_note(ciphertext_bundle, password):
        try:
            # Remove salt and nonce from front of concatinated bundle
            salt = ciphertext_bundle[:SecurityManager._SALT_SIZE]
            nonce = ciphertext_bundle[SecurityManager._SALT_SIZE:SecurityManager._SALT_SIZE + SecurityManager._NONCE_SIZE]
            ciphertext = ciphertext_bundle[SecurityManager._SALT_SIZE + SecurityManager._NONCE_SIZE:]
            # Rebuild the key from the extracted salt
            key = SecurityManager._derive_key_from_password(password, salt)
            # Wrong password OR corrupted data throws an exception
            aesgcm = AESGCM(key)
            plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            return plaintext_bytes.decode("utf-8")
        except Exception as e:
            SecurityManager._handle_decryption_error(e)
            return None
