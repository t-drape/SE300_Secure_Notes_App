```mermaid
classDiagram
    class SecurityManager {
        -derive_key_from_password(password, salt)
        -validate_password(password)
        -handle_encryption_error(error)
        -handle_decryption_error(error)
        +encrypt_note(plaintext, password)
        +decrypt_note(ciphertext, password)
    }
```
