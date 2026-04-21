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
    _PBKDF2_ITERATIONS = 600000
    _MIN_PASSWORD_LENGTH = 8
    
    # SDD_TT_4_001 :: [SRD::T_15, SRD::T_46]
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
    
    # SDD_TT_4_002 :: [SRD::T_31]
    @staticmethod
    def validate_password(password):
        # Check password length meets minimums
        return len(password) >= SecurityManager._MIN_PASSWORD_LENGTH
        
    # SDD_TT_4_003 :: [SRD::T_51]
    @staticmethod
    def _handle_encryption_error(error):
        print(f"Encryption error: {error}")

    # SDD_TT_4_004 :: [SRD::T_52]
    @staticmethod
    def _handle_decryption_error(error):
        print("Decryption failed.")

    # SDD_TT_4_005 :: [SRD::T_15, SRD::T_28, SRD::T_35, SRD::T_46, SRD::T_47, SRD::T_49]
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
            
    # SDD_TT_4_006 :: [SRD::T_16, SRD::T_28, SRD::T_36, SRD::T_46, SRD::T_50]
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
