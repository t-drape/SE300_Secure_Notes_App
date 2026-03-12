```mermaid
sequenceDiagram
    participant User
    participant TSC as Terminal Start Command
    participant Menu
    participant SecurityManager
    participant Database
    participant PEC as Program Exit Command
    
    User->>TSC: Run application
    TSC->>Menu: Launch menu
    
    loop Until user exits
        Menu->>User: Display action menu
        User->>Menu: select()
        Menu->>Menu: act()
        
        alt 1) New Note
            User->>Menu: Provide note content
            User->>Menu: Provide password
            Menu->>SecurityManager: encrypt_note(plaintext, password)
            SecurityManager-->>Menu: concatenated ciphertext
            Menu->>Database: Save encrypted note
            Database-->>Menu: Confirmation

        else 2) Display Note
            Menu->>User: choose_file()
            User->>Menu: filename
            Menu->>Database: Retrieve encrypted note
            Database-->>Menu: encrypted_data
            User->>Menu: Provide password
            Menu->>SecurityManager: decrypt_note(ciphertext, password)
            SecurityManager-->>Menu: plaintext
            Menu->>User: Display note

        else 3) Change Note
            Menu->>User: choose_file()
            User->>Menu: filename
            Menu->>Database: Retrieve encrypted note
            Database-->>Menu: encrypted_data
            User->>Menu: Provide password
            Menu->>SecurityManager: decrypt_note(ciphertext, password)
            SecurityManager-->>Menu: plaintext
            User->>Menu: Provide additional content
            Menu->>SecurityManager: encrypt_note(plaintext, password)
            SecurityManager-->>Menu: concatenated ciphertext
            Menu->>Database: Save encrypted note
            Database-->>Menu: Confirmation

        else 4) Summarize Note
            Menu->>User: choose_file()
            User->>Menu: filename
            Menu->>Database: Retrieve encrypted note
            Database-->>Menu: encrypted_data
            User->>Menu: Provide password
            Menu->>SecurityManager: decrypt_note(ciphertext, password)
            SecurityManager-->>Menu: plaintext
            Menu->>Menu: AI summarization
            Menu->>User: Display summary

        else 5) Delete Note
            Menu->>User: choose_file()
            User->>Menu: filename
            Menu->>User: confirm_delete()
            User->>Menu: Confirm
            Menu->>Database: Delete note
            Database-->>Menu: Confirmation

        else 6) Exit
            User->>Menu: Select exit
            Menu->>PEC: Exit program
            PEC->>User: Terminate
        end
    end
```
