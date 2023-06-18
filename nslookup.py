import csv
import subprocess

# Create an empty list to store the domains
domains = []
# Create an empty list to store both the domains and the found information
domain_info_list = []

# Open the CSV file "Domini_atenei.csv"
with open("Domini_atenei.csv", "r") as file:
    reader = csv.reader(file)
    for row in reader:
        # Add each domain to the list
        domains.append(row[0])

# Set three counters to keep track of domains using Google Workspace, Microsoft 365, or both
google_counter = 0
microsoft_counter = 0
both_counter = 0

for domain in domains:
    # Execute the "nslookup" command to get information about TXT records
    process1 = subprocess.run(["nslookup", "-q=txt", domain], stdout=subprocess.PIPE, universal_newlines=True)
    output = process1.stdout
    print("Domain:", domain)
    print(output)

    # Execute another "nslookup" command to get information about MX records
    process2 = subprocess.run(["nslookup", "-q=mx", domain], stdout=subprocess.PIPE, universal_newlines=True)
    output2 = process2.stdout
    print(output2)
    
    # Check if the domain uses Google Workspace
    if "ASPMX.L.GOOGLE.COM" in output2 or "google-site-verification" in output or "spf.google" in output:
        google_counter += 1
        # Check if the domain uses Microsoft 365
        if "MS=" in output or "outlook.com" in output2 or "spf.protection.outlook" in output:
            both_counter += 1
            print("Uses both")
            # Add the domain and the info to the final list
            domain_info_list.append((domain, "Uses Both"))
        else:
            print("Uses Google Workspace")
            domain_info_list.append((domain, "Uses Google Workspace"))
    else:
        print("Does not use Google Workspace")
        # Check if the domain uses Microsoft 365
        if "MS=" in output or "outlook.com" in output2 or "spf.protection.outlook" in output:
            microsoft_counter += 1
            print("Uses Microsoft 365")
            domain_info_list.append((domain, "Uses Microsoft 365"))
        else:
            print("Does not use either")
            domain_info_list.append((domain, "Does not use either service"))

# Calculate and print the percentages of domains using Google Workspace and Microsoft 365
total_domains = len(domains)
google_percentage = (google_counter / total_domains) * 100
microsoft_percentage = (microsoft_counter / total_domains) * 100
both_percentage = ((google_counter + microsoft_counter - both_counter) / total_domains) * 100

# Format the percentage
google_percentage_formatted = "{:.2f}".format(google_percentage)
microsoft_percentage_formatted = "{:.2f}".format(microsoft_percentage)
both_percentage_formatted = "{:.2f}".format(both_percentage)


print("Domains and email service information:")
for domain, info in domain_info_list:
    print(domain, ":", info)


print("Percentage of domains using only Google Workspace:", google_percentage_formatted, "%" )
print("Percentage of domains using only Microsoft 365:", microsoft_percentage_formatted, "%")
print("Percentage of domains using both Google Workspace and Microsoft 365:", both_percentage_formatted, "%")
