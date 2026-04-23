# Secure Notes CLI Application

## Overview

The Secure Notes Application is a privacy-focused, local command-line tool that allows users to securely create, manage, and analyze personal notes. The system operates entirely offline and ensures that all user data remains encrypted and under full local control.

All notes are encrypted using AES-256 before being stored and are only decrypted in memory when accessed. The application also includes built-in AI functionality for summarizing notes and extracting keywords.

---

## Features

### Core Functionality
- Create new notes
- Display existing notes
- Append to notes
- Delete notes (with confirmation)

### Security
- AES-256 encryption for all stored notes
- PBKDF2 key derivation from user password
- No plaintext data stored on disk
- Password required for all encryption and decryption

### AI Capabilities
- Extractive note summarization
- Keyword extraction
- Fully offline, rule-based processing

### Interface
- Menu-driven command-line interface
- Input validation for all user actions
- Lightweight and fast execution

---

## System Architecture

The system is designed using a modular architecture with clearly separated responsibilities:

- Menu: Handles user interaction and controls application flow
- SecurityManager: Manages encryption and decryption
- DbConnect: Handles database operations using SQLite3
- AIProcessor: Coordinates AI operations
    - Summarizer: Generates summaries
    - KeywordAnalyzer: Extracts keywords

This design improves maintainability, scalability, and security.

---

## Technologies Used

- Python 3.10+
- SQLite3 (local database)
- AES-256 encryption
- PBKDF2 key derivation
- Rule-based natural language processing

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/t-drape/SE300_Secure_Notes_App.git
cd SE300_Secure_Notes_App
