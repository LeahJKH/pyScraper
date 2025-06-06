import subprocess
import os
import sys

print("Welcome to Leah's job scraper!\n1. Manual\n2. Live server")
choice = input("Choose: ").strip().lower()

python_cmd = sys.executable
script_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(script_dir, "frontend")

if choice.startswith("1"):
    site = input("Search site: 1. Finn  2. Arbeidsplassen\n").strip().lower()
    if site.startswith("1"):
        subprocess.run([python_cmd, "manual/finn.py"])
    elif site.startswith("2"):
        subprocess.run([python_cmd, "manual/arbeidsplassen.py"])
    else:
        print("Invalid site.")
elif choice.startswith("2"):
    subprocess.Popen([python_cmd, "site/api.py"])

    try:
        subprocess.run("npm run dev", cwd=frontend_dir, shell=True, check=True)
    except FileNotFoundError:
        print("npm not found! Make sure Node.js and npm are installed and added to PATH.")
else:
    print("Invalid choice.")
