import requests
import pandas as pd
from bs4 import BeautifulSoup
import json

# Base URL for job listings
base_url = "https://www.finn.no/job/fulltime/search.html?abTestKey=jobs_vestfold_telemark"

# List of locations to filter
locations_of_interest = [
    "Færder", "Holmestrand", "Horten", "Larvik", "Sandefjord", "Tønsberg", 
    "Bamle", "Drangedal", "Fyresdal", "Hjartdal", "Kragerø", "Kviteseid", 
    "Midt-Telemark", "Nissedal", "Nome", "Notodden", "Porsgrunn", "Seljord", 
    "Tinn", "Tokke", "Vinje", "Telemark", "Skien", "Sandefjord"
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
        print(f"Found {len(job_listings)} jobs on this page.")

        for job in job_listings:
            title = job.get('heading', 'No title')
            employer = job.get('company_name', 'No employer')
            link = job.get('canonical_url', 'No link')
            location = job.get('location', 'No location')

        

            # Check if the job location is in the list of locations of interest
            if any(loc in location for loc in locations_of_interest):
                jobs.append([title, employer, link, location])
                print(f"Job added: {title}, {employer}, {link}, {location}")
    except KeyError as e:
        print(f"KeyError: {e} - Please check the JSON structure.")
    
    return jobs

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
        if not jobs:
            print("No more jobs found or end of data.")
            break
        
        all_jobs.extend(jobs)
        page_number += 1

    print(f"Total jobs extracted: {len(all_jobs)}")
    if all_jobs:
        df = pd.DataFrame(all_jobs, columns=['Title', 'Employer', 'Link', 'Location'])
        df.to_csv('FilteredJobs.csv', index=False)
        print("Data saved to FilteredJobs.csv")

if __name__ == "__main__":
    main()