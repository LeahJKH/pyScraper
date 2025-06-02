import os

print("Hello, welcome to Leah's job scraper! :3 Meowserz")
print("Do you want to run it manually or use the live server? \n 1. Manual \n 2. Live server")


chosen = input().strip().lower()

if chosen == "1" or chosen == "manual":
    print("Which site do you want to search in? \n 1. Finn \n 2. Arbeidsplassen")
    site = input().strip().lower()

    if site == "1" or site == "finn":
        os.system("python3 manual/finn.py")
    elif site == "2" or site == "arbeidsplassen":
        os.system("python3 manual/arbeidsplassen.py")
    else:
        print("Invalid choice for site.")

elif chosen == "2" or chosen == "live server":
    os.system("python3 live_server.py")
else:
    print("Invalid choice. Please select 1 or 2.")
