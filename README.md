# Analysis-of-Remote-Education-Tools-in-Italian-Universities
This project aims to assess the current state of remote education tools in Italian universities. 
Specifically, it focuses on analyzing the availability of platforms like Google Meet and Microsoft Teams. 
The goal is to gain insights into the usage of these platforms by conducting a domain analysis of each university.
To analyze Google Workspace services, the project utilized the automation of the "nslookup" command on each university domain
from the provided CSV file. This process involved retrieving MX records and TXT records for each domain and extracting relevan
t information for verification. For the assessment of Microsoft Teams services, the project employed web scraping techniques 
in multi-threaded execution. This allowed simultaneous scraping of university domains to identify the presence of Microsoft Teams services.
