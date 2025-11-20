import subprocess
import os
import sys

print("Welcome to Leah's job scraper!\n1. Manual\n2. Live server")
choice = input("Choice?: ").strip().lower()

python_cmd = sys.executable
script_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(script_dir, "frontend")

if choice.startswith("1" or "manual"):
    print("not implimented")
        # TODO connect backend
elif choice.startswith("2" or "live server"):
    subprocess.run("npm i", cwd=frontend_dir, shell=True, check=True)
    #will try too download neccesary files 
    try:
        subprocess.run("npm run dev", cwd=frontend_dir, shell=True, check=True)
    except FileNotFoundError:
        print("npm install didnt work you are missing files")
else:
    print("Invalid choice.")
