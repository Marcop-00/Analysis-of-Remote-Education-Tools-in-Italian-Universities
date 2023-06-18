import csv
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Function to search the presence of Microsoft Teams or MS Teams on the page
def search_page(url):
    try:
        # Make a request to the specified URL
        response = requests.get(url)
        # Create a BeautifulSoup object from the response
        soup = BeautifulSoup(response.content, "html.parser")
    except:
        return False
    
    # Check for the presence of "Microsoft Teams" or "MS Teams" on the page
    if "Microsoft Teams" in str(soup) or "MS Teams" in str(soup):
        print(f"Microsoft Teams found at {url}")
        return True
    else:
        return False

# Main function to perform the search on each domain
def main_function(domain):
    url = f"https://www.{domain}/"
    if search_page(url):
        # If Microsoft Teams is found on the main page, print it and exit the function
        print(f"Microsoft Teams found at {url}")
        return True
    else:
        try:
            response = requests.get(url)
            # Create a BeautifulSoup object from the response
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all links on the page
            links = [link.get("href") for link in soup.find_all("a")]
            for link in links:
                if link.startswith("http") and search_page(link):
                    break
        except:
            return False

# Open the CSV file that contains the university domains
with open("Domini_atenei.csv") as file:
    reader = csv.reader(file)
    domains = [row[0] for row in reader]

# Create a thread pool with a maximum of 5 workers
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    results = [executor.submit(main_function, domain) for domain in domains]
