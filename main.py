import csv
from scrap_page import scrap_company_info

input_file = "input.txt"
output_file = "output.csv"


def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.read().splitlines()
    return urls


print("Scraping started. Please wait...\n")

# Read URLs from the text file
company_urls = read_urls(input_file)

# Scrape each URL and gather the dictionaries
dictionaries = [scrap_company_info(url) for url in company_urls]

# Extract keys for the CSV header from the first dictionary
header = dictionaries[0].keys()

# Write the values to the CSV file
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    for dictionary in dictionaries:
        writer.writerow(dictionary)

print(f"Scraping Complete! Generated the file {output_file}")
