import requests
from bs4 import BeautifulSoup
import os
import re

location_codes = {
    "oslo": "1.20001.20061", "agder": "1.20001.22042", "akershus": "1.20001.20003",
    "buskerud": "1.20001.20007", "finnmark": "1.20001.20020", "innlandet": "1.20001.22034",
    "møre og romsdal": "1.20001.20015", "nordland": "1.20001.20018", "rogaland": "1.20001.20012",
    "svalbard": "1.20001.20506", "telemark": "1.20001.20009", "troms": "1.20001.20019",
    "trøndelag": "1.20001.20016", "vestfold": "1.20001.20008", "vestland": "1.20001.22046",
    "bergen": "2.20001.22046.20220", "østfold": "1.20001.20002", "norge": "0.20001",
    "utlandet": "0.20534", "porsgrunn": "2.20001.20009.20146", "ålesund": "2.20001.20015.20282"
}

def safe_text(text):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', text.lower().strip())

def main():
    query = input("What job are you looking for? ").strip()
    regions = [r.strip().lower() for r in input("Regions (comma-separated): ").split(",")]

    locations = [(loc, location_codes[loc]) for loc in regions if loc in location_codes]
    if not locations:
        print("No valid locations.")
        return

    safe_query = safe_text(query)
    safe_locs = "_".join(safe_text(loc) for loc, _ in locations)

    os.makedirs("finn_jobs", exist_ok=True)
    filepath = os.path.join("finn_jobs", f"finn_jobs_{safe_query}_{safe_locs}.txt")

    results = []
    for page in range(1, 51):
        params = [("q", query), ("page", str(page))] + [("location", code) for _, code in locations]
        r = requests.get("https://www.finn.no/job/fulltime/search.html", params=params)

        if r.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {r.status_code}")
            break

        soup = BeautifulSoup(r.text, "html.parser")
        ads = soup.find_all("article", class_="sf-search-ad")

        if not ads:
            print(f"No more ads found at page {page}, stopping.")
            break

        for ad in ads:
            # Skip if ad is imported from NAV
            if any("Hentet fra NAV" in span.text for span in ad.select("span")):
                continue

            title_tag = ad.find("a", class_="sf-search-ad-link")
            if not title_tag:
                continue
            title = title_tag.text.strip()
            link = title_tag.get("href", "#")
            company_info = ", ".join(span.text.strip() for span in ad.select("div.flex.flex-col.text-xs span"))

            results.append(f"Title: {title}")
            results.append(f"Link: {link}")
            if company_info:
                results.append(f"Company Info: {company_info}")
            results.append("-" * 60)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(results))

    print(f"Saved {len(results) // 4} job ads to {filepath}")

if __name__ == "__main__":
    main()
