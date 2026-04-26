# Secure Notes CLI Application

## Overview

Secure Notes is a privacy-focused command-line application for managing encrypted personal notes entirely offline. The system is designed to ensure that sensitive user data is never exposed, using strong cryptographic practices and a clean modular architecture.

All notes are encrypted using AES-256 before being stored locally and are only decrypted in memory when accessed. In addition to secure storage, the application includes built-in text analysis features such as summarization.

---

## Key Features

### Secure Note Management

* Create, view, modify, and delete notes
* All notes stored in a local SQLite database
* No external services or network communication

### Security

* AES-256 encryption for all stored data
* Password-based key derivation using PBKDF2
* No plaintext data written to disk
* Decryption performed only in memory

### Text Analysis

* Extractive summarization of notes
* Keyword extraction for quick insights
* Fully offline, rule-based processing

### Interface

* Menu-driven command-line interface
* Input validation and error handling
* Lightweight and responsive execution

---

## Architecture

The application follows a modular design to separate responsibilities and improve maintainability:

* **Menu**: Handles user interaction and application flow
* **SecurityManager**: Implements encryption and decryption logic
* **Database Layer (SQLite3)**: Manages persistent storage
* **AIProcessor**: Coordinates text processing tasks

  * **Summarizer**: Extractive summarization
  * **KeywordAnalyzer**: Keyword extraction

This structure supports clean integration between components while maintaining strong separation of concerns.

---

## Project Structure

```
SE300_Secure_Notes_App/
├── app/                # Core application logic
├── docs/               # Project documentation (SRD, SDD, verification)
├── requirements.txt
├── README.md
```

---

## Installation and Setup

Clone the repository:

```bash
git clone https://github.com/t-drape/SE300_Secure_Notes_App.git
cd SE300_Secure_Notes_App
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application:

```bash
cd app
python main.py
```

Follow the on-screen menu to interact with the system.

---

## Documentation

* [Verification Package](docs/Verification_Package.pdf)
* Software Requirements Document (SRD) in `/docs/SRD`
* Software Design Document (SDD) in `/docs/SDD`

These documents include system requirements, architecture, testing methodology, and validation procedures.

---

## Technical Highlights

* Fully offline architecture with no external dependencies
* Secure handling of sensitive data using modern cryptographic standards
* Modular design aligned with software engineering best practices
* Integration of rule-based NLP techniques without external APIs

---

## Authors

* TJ Drape
* Afonso Azevedo
* Roman Zalewski
* John Markham
