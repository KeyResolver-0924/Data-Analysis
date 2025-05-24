import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

job_board_url = "https://aijobs.net"
query = "/?region=us&search=python&sort_by=latest"
response = requests.get(job_board_url + query)

if response.status_code == 200:
    # Parse the HTML content
    html_content = response.text
else: 
    print(f"False retrieve the page: {response.status_code}")    
# Extract job links
    exit()

soup = BeautifulSoup(html_content, 'html.parser')
job_links = soup.select('ul#job-list a.col.py-2[href]')
jobs_url_list = [job_board_url + link['href'] for link in job_links]
# for job_url in jobs_url_list:
#     print(job_url)

# extract html from job listing (same as cell 2)
job_url = jobs_url_list[0]
response = requests.get(job_url)
html_content = response.text

# Find the script tag containing JSON-LD
script_tag = soup.find('script', type='application/ld+json')

# Load the JSON content
if script_tag:
    job_data = json.loads(script_tag.string)
    json_data = json.dumps(job_data, indent=4)

    # Extract job details
    job_title = job_data['name']
    job_description = job_data['description']
    job_url = job_data['url']
    job_logo = job_data['logo']

    job_all_data = {
        'job_title': job_title,
        'job_description': job_description,
        'job_url': job_url,
        'job_logo': job_logo
    }

    # Save the job data to a CSV file
    df = pd.DataFrame([job_all_data])
    print(df)
    df.to_csv('job_data.csv', index=False)
else:
    print("No JSON-LD script tag found.")


