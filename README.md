# AI Terminal

**A human-friendly AI-powered terminal that lets you run commands in plain English.**  
No terminal knowledge required — just type what you want to do, and AI generates safe commands, explains them, and executes them in your default terminal.

---

## 🌟 Features

- **English → Terminal Commands**  
  Type normal language like `install numpy` and get the correct command automatically.

- **Command Explanation**  
  AI explains in simple words what the command will do before running it.

- **OS-Aware Commands**  
  Works on Windows, Linux, and macOS with proper OS-specific commands.

- **Auto-Fix & Retry**  
  If a command fails, AI suggests a fix and can retry automatically.

- **Command History**  
  All executed commands are saved with English input, actual command, timestamp, and success/failure status.

- **Safe Execution**  
  Dangerous commands like `rm -rf /` are blocked automatically.
---

## ⚡ How It Works

1. User types an instruction in plain English.  
2. AI converts it to a terminal command.  
3. AI explains the command in simple terms.  
4. User confirms execution.  
5. Command executes in the default terminal.  
6. History is saved, and errors are explained if any occur.



---

## Setup & Run
1. Install Python (if not already)
 - Download from python.org
 - During install, tick 'Add Python to PATH'
 Check version:
 ```bash
 python --version
 ```
2. Install Dependencies
 ```bash
 pip install google-genai
 ```
3. Configure API Key
 - Get your Google Gemini / Generative AI API key from Google Cloud Console
 - Open ai_terminal.py and set:
 ```python
 GEMINI_API_KEY = "YOUR_API_KEY_HERE"
 ```
4. Run the Terminal
 ```bash
 python ai_terminal.py
 ```
 Example commands:
 ```
 install numpy
 create a folder called test
 show current directory
 ```

---

## 📄 License

This project is licensed under the **MIT License** – see [LICENSE](LICENSE) for details.
