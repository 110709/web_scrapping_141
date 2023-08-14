import requests
from bs4 import BeautifulSoup
import csv

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
HEADERS = ["Name", "Distance", "Mass", "Radius"]
star_data = []

response = requests.get(START_URL)
if response.status_code == 200:
    page_content = response.content
else:
    print("Error fetching the page.")
    exit()

soup = BeautifulSoup(page_content, "html.parser")
tables = soup.find_all("table")

for table in tables:
    rows = table.find_all("tr")
    
    for row in rows:
        columns = row.find_all("td")
        
        if len(columns) == len(HEADERS):
            star = {}
            
            for i in range(len(HEADERS)):
                star[HEADERS[i]] = columns[i].get_text().strip()
            
            star_data.append(star)

csv_filename = "brightest_stars.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=HEADERS)
    writer.writeheader()
    
    for star in star_data:
        writer.writerow(star)

print("Data has been scraped and saved to", csv_filename)
