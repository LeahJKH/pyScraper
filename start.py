import subprocess
import os

def python_package_installed(package_name):
    result = subprocess.run(["pip", "show", package_name], capture_output=True, text=True)
    return result.returncode == 0

def install_missing_python_packages(requirements_path):
    with open(requirements_path, 'r') as f:
        packages = [line.strip().split('==')[0] for line in f if line.strip() and not line.startswith('#')]

    missing = [pkg for pkg in packages if not python_package_installed(pkg)]

    if missing:
        print(f"Installing missing Python packages: {missing}")
        subprocess.run(["pip", "install", "-r", requirements_path])
    else:
        print("All Python packages already installed.")

def node_modules_exist(frontend_path):
    return os.path.isdir(os.path.join(frontend_path, "node_modules"))

def main():
    print("Hello, welcome to Leah's job scraper! :3 Meowserz")
    print("Do you want to run it manually or use the live server? \n 1. Manual \n 2. Live server")

    chosen = input().strip().lower()

    if chosen in ("1", "manual"):
        print("Which site do you want to search in? \n 1. Finn \n 2. Arbeidsplassen")
        site = input().strip().lower()

        if site in ("1", "finn"):
            subprocess.run(["python", "manual/finn.py"])
        elif site in ("2", "arbeidsplassen"):
            subprocess.run(["python", "manual/arbeidsplassen.py"])
        else:
            print("Invalid choice for site.")

    elif chosen in ("2", "live server"):

        # Backend
        backend_path = os.path.join(os.getcwd(), "site")
        api_path = os.path.join(backend_path, "api.py")
        requirements_path = os.path.join(backend_path, "requirements.txt")

        if os.path.exists(api_path):
            if os.path.exists(requirements_path):
                install_missing_python_packages(requirements_path)
            else:
                print("⚠️ No requirements.txt found in backend folder.")

            subprocess.Popen(["python", "api.py"], cwd=backend_path)
        else:
            print("❌ Backend api.py not found at", api_path)

        # Frontend
        frontend_path = os.path.join(os.getcwd(), "frontend")
        package_json_path = os.path.join(frontend_path, "package.json")

        if os.path.exists(package_json_path):
            if not node_modules_exist(frontend_path):
                print("Installing npm packages...")
                subprocess.run(["npm", "install"], cwd=frontend_path, shell=True)
            else:
                print("npm packages already installed.")

            subprocess.Popen(["npm", "run", "dev"], cwd=frontend_path, shell=True)
        else:
            print("❌ Frontend package.json not found at", package_json_path)

    else:
        print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
