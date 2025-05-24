import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

# URL of the website
job_board_url = "https://aijobs.net"
query = "/?reg=5" # north america jobs

# Send a GET request to the website
response = requests.get(job_board_url + query)

# Check if the request was successful
if response.status_code == 200:
    # Get the HTML content
    html_content = response.text
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# Find all job links within the <ul> list
job_links = soup.select('ul#job-list a.col.py-2[href]')

# explanation from ChatGPT:
# This selects all <a> tags with class col py-2 inside the <ul> element with id="job-list"
# Extract href attributes and create full URLs
job_url_list = [job_board_url + link['href'] for link in job_links]

for job_url in job_url_list:
    print(job_url)

def extract_job_info(url):
    """
    Extracts job information from a given job listing URL.

    Args:
        url (str): The URL of the job listing.

    Returns:
        dict: A dictionary containing the following key-value pairs:
            - 'company_name' (str): Name of the hiring organization.
            - 'job_title' (str): Title of the job.
            - 'job_description' (str): Detailed description of the job.
            - 'salary_min' (float or str): Minimum salary offered for the job.
            - 'salary_max' (float or str): Maximum salary offered for the job.
               Returns 'N/A' if salary information is unavailable.
    """
    try:
        # Fetch the HTML content of the job listing
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        html_content = response.text
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find the script tag containing JSON-LD
        script_tag = soup.find('script', type='application/ld+json')
        
        if script_tag:
            job_data = json.loads(script_tag.string)
            
            # Extract relevant fields with default values if not present
            company_name = job_data.get('hiringOrganization', {}).get('name', 'N/A')
            job_title = job_data.get('title', 'N/A')
            job_description = job_data.get('description', 'N/A')
            salary_data = job_data.get('baseSalary', {}).get('value', {})
            salary_min = salary_data.get('minValue', 'N/A')
            salary_max = salary_data.get('maxValue', 'N/A')
            
            return {
                'company_name': company_name,
                'job_title': job_title,
                'job_description': job_description,
                'salary_min': salary_min,
                'salary_max': salary_max
            }
        else:
            return {'error': 'No JSON-LD script found in the page'}
    
    except requests.RequestException as e:
        return {'error': f"Request failed: {e}"}
    
    except json.JSONDecodeError:
        return {'error': 'Failed to parse JSON-LD content'}
    
    except Exception as e:
        return {'error': f"An unexpected error occurred: {e}"}
# extract job info from all job urls
job_info_list = []

for job_url in job_url_list:
    # extract job info
    job_info = extract_job_info(job_url)

    # store results in list if no errors occured
    try:
        print(job_info["job_title"])
        job_info_list.append(job_info)
    except:
        print(f"Could not extract info from: {job_url}")
        continue