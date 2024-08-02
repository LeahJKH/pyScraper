import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Your Google Sheets document ID and range
SHEET_ID = '1oMX31ORZ9SjK4DQN_aUW79BSJhgV6hYwUWEo7pdJFhk'
SHEET_RANGE = 'Sheet1!A1:D'  # Adjust range as needed

# Base URL for job listings
base_url = "https://www.finn.no/job/fulltime/search.html?industry=41&industry=8&industry=65&industry=32&industry=34&industry=66&location=0.20001&occupation=0.7&occupation=0.62&occupation=0.61&occupation=0.60&occupation=0.25&occupation=0.23&occupation=0.22&occupation=0.2"

# List of locations to filter
locations_of_interest = [
    "Færder", "Holmestrand", "Horten", "Larvik", "Sandefjord", "Tønsberg", "Bamle", "Drangedal",
    "Fyresdal", "Hjartdal", "Kragerø", "Kviteseid", "Midt-Telemark", "Nissedal", "Nome", "Notodden",
    "Porsgrunn", "Seljord", "Tinn", "Tokke", "Vinje", "Telemark", "Skien", "Sandefjord"
]

# Keywords to filter job titles
keywords = [
    "it", "IT", "Utvikler", "FullStack", "Backend", "Frontend", "PC", "Telefon", "Phone", "pc", "developer", "Developer",
    "Software", "Firmware", "Reperasjon", "Ikt", "IKT", "Dev", "Devops", "security", "Databaser", "Spill", "Game", "Tech",
    "teknologi", "Teknologi", "Artificial Intelligence", "AI", "Machine Learning", "ML", "Data Science", "Cloud Computing",
    "Cloud", "Big Data", "Analytics", "Cybersecurity", "Network", "Infrastructure", "Systems Admin", "SysAdmin", "DevOps",
    "Agile", "Scrum", "Kanban", "Microservices", "APIs", "Integration", "Blockchain", "IoT", "Internet of Things", "AR",
    "Augmented Reality", "VR", "Virtual Reality", "Database Administration", "SQL", "NoSQL", "Front-End", "Back-End",
    "Full-Stack", "UI/UX", "User Interface", "User Experience", "Software Engineering", "Web Development", "Mobile Development",
    "Embedded Systems", "Firmware Development", "Tech Support", "Tech Lead", "Software Architect", "Code", "Programming",
    "Scripting", "Version Control", "Git", "Continuous Integration", "CI/CD", "Testing", "QA", "Quality Assurance", "Debugging",
    "Optimization", "Software Design", "Technical Writing", "Tech Consultant", "Tech Strategy", "Startup", "Innovation",
    "Tech Trends", "Kunstig Intelligens", "Maskinlæring", "Datascience", "Skykomputing", "Stor Data", "Analyse", "Cybersikkerhet",
    "Nettverk", "Infrastruktur", "Systemadministrasjon", "Smidig", "Scrum", "Kanban", "Mikrotjenester", "API-er", "Integrasjon",
    "Blokkjedeteknologi", "Internet of Things (IoT)", "Augmented Reality (AR)", "Virtual Reality (VR)", "Databaseadministrasjon",
    "NoSQL", "Front-End", "Back-End", "Full-Stack", "UI/UX", "Brukergrensesnitt", "Brukeropplevelse", "Programvareutvikling",
    "Nettutvikling", "Mobilutvikling", "Innebygde Systemer", "Firmwareutvikling", "Teknisk Support", "Teknisk Leder",
    "Programvarearkitekt", "Kode", "Programmering", "Skript", "Versjonskontroll", "Kontinuerlig Integrasjon", "CI/CD", "Testing",
    "Kvalitetssikring (QA)", "Feilsøking", "Optimalisering", "Programvaredesign", "Teknisk Skriving", "Teknisk Konsulent",
    "Teknisk Strategi", "Oppstart", "Innovasjon", "Teknologitrender"
]

def fetch_jobs(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, 'html.parser')
    script_tag = soup.find('script', id='__NEXT_DATA__')

    if not script_tag:
        print("No <script> tag with id '__NEXT_DATA__' found.")
        return None

    json_text = script_tag.string
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON data. Error: {e}")
        return None

    return data

def extract_jobs(data):
    jobs = []
    try:
        job_listings = data['props']['pageProps']['search']['docs']
        if not job_listings:
            return jobs

        print(f"Found {len(job_listings)} jobs on this page.")
        
        for job in job_listings:
            title = job.get('heading', 'No title')
            employer = job.get('company_name', 'No employer')
            link = job.get('canonical_url', 'No link')
            location = job.get('location', 'No location')

            # Check if the job location is in the list of locations of interest
            if any(loc in location for loc in locations_of_interest):
                # Check if any of the keywords are in the job title
                if any(keyword in title for keyword in keywords):
                    jobs.append([title, employer, link, location])
                
    except KeyError as e:
        print(f"KeyError: {e} - Please check the JSON structure.")
    
    return jobs

def update_google_sheet(service, data):
    try:
        values = [['Title', 'Employer', 'Link', 'Location']] + data
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID,
            range=SHEET_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    all_jobs = []
    page_number = 1
    while True:
        url = f"{base_url}&page={page_number}"
        print(f"Fetching page {page_number}...")
        data = fetch_jobs(url)
        if not data:
            print("No data found or failed to fetch data.")
            break
        
        jobs = extract_jobs(data)
        
        # Continue to the next page even if no jobs are found
        if jobs:
            all_jobs.extend(jobs)
        else:
            print("No jobs found on this page. Moving to the next page.")
        
        page_number += 1

    print(f"Total jobs extracted: {len(all_jobs)}")

    # Authenticate and update Google Sheets
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    service = build('sheets', 'v4', credentials=creds)

    if all_jobs:
        update_google_sheet(service, all_jobs)

if __name__ == "__main__":
    main()