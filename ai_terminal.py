import subprocess
import os
import json
from datetime import datetime
from google import genai

# ================= CONFIG =================
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
HISTORY_FILE = "command_history.json"

BLOCKED_KEYWORDS = [
    "rm -rf", "shutdown", "reboot", "mkfs",
    "dd ", ":(){", "format", "del /f", "wipe"
]
# =========================================

client = genai.Client(api_key=GEMINI_API_KEY)


def get_os_name():
    return "Windows" if os.name == "nt" else "Linux/Mac"


def gemini(prompt):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text.strip()


def generate_command(user_text):
    prompt = f"""
Convert the following instruction into a SINGLE safe terminal command.

Target OS: {get_os_name()}

Rules:
- Return ONLY the command
- No explanation
- No markdown
- No backticks

Instruction:
{user_text}
"""
    return gemini(prompt)


def explain_command(command):
    prompt = f"""
Explain what this terminal command does in very simple language
for a non-technical user (2 lines max).

Command:
{command}
"""
    return gemini(prompt)


def explain_error(command, error):
    prompt = f"""
This terminal command failed.

Command:
{command}

Error:
{error}

Explain why it failed in simple language (2–3 lines).
"""
    return gemini(prompt)


def fix_command(command, error):
    prompt = f"""
The following command failed. Fix it.

Command:
{command}

Error:
{error}

Return ONLY the corrected command.
"""
    return gemini(prompt)


def is_safe(command):
    cmd = command.lower()
    return not any(bad in cmd for bad in BLOCKED_KEYWORDS)


def save_history(entry):
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)

    history.append(entry)

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def execute_command(command, user_input):
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True
    )

    entry = {
        "time": str(datetime.now()),
        "user_input": user_input,
        "command": command,
        "success": result.returncode == 0
    }

    if result.returncode == 0:
        print("\n✅ Execution Successful")
        if result.stdout.strip():
            print(result.stdout)
        save_history(entry)
        return

    print("\n❌ Execution Failed")
    print("Raw Error:")
    print(result.stderr or "Unknown error")

    reason = explain_error(command, result.stderr)
    print("\n🧠 Reason:")
    print(reason)

    fixed = fix_command(command, result.stderr)
    print("\n🔧 AI Suggested Fix:")
    print(fixed)

    retry = input("\nRetry with fixed command? (y/n): ").lower()
    if retry == "y" and is_safe(fixed):
        execute_command(fixed, user_input)
    else:
        save_history(entry)


def main():
    print("\n🤖 AI TERMINAL (English → Command)")
    print("Default terminal only | Type 'exit' to quit\n")

    while True:
        user_input = input("> ")

        if user_input.lower() == "exit":
            print("Goodbye 👋")
            break

        command = generate_command(user_input)

        print("\n🔧 AI Command:")
        print(command)

        if not is_safe(command):
            print("⚠️ Blocked for safety reasons")
            continue

        explanation = explain_command(command)
        print("\n📘 What this will do:")
        print(explanation)

        confirm = input("\nRun this command? (y/n): ").lower()
        if confirm != "y":
            print("Cancelled ❌")
            continue

        execute_command(command, user_input)
        print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
