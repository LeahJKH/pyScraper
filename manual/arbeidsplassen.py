# https://arbeidsplassen.nav.no/stillinger
import requests
from bs4 import BeautifulSoup
import re
import os

query = input("What are you looking for? ").strip().lower()
location_input = input("Which region? (e.g., oslo, bergen) ").strip().upper()

base_url = "https://arbeidsplassen.nav.no/stillinger"
# https://arbeidsplassen.nav.no/stillinger?county=OSLO&v=5&q=frontend

newUrl = "https://arbeidsplassen.nav.no/stillinger?county=" + location_input +"&v=5&q=" + query;

output_lines = []
    for page in range(1, 25):
        response = requests.get(newUrl)
        