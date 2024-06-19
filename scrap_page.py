import time

import requests
from bs4 import BeautifulSoup

from link_exception import LinkException
from scrap_utils import extract_financial_data_from_table

company_name_css_class = "Profile__Name"
profile_info_css_class = "Profile__Info"
email_css_class = "listing-email"
website_css_class = "listing-website-url"
address_css_class = "listing-street-address"
director_css_class = "DecisionPerson--prh"
financial_table_css_class = "Financials__Table"


def get_page_soup(page_url: str):
    # Fetch the content from the URL
    time.sleep(0.3)
    response = requests.get(page_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'lxml')

        return soup

    else:
        raise LinkException(f"Failed to retrieve the page. Status code: {response.status_code}. URL = {page_url}")


def extract_company_info(company_soup: BeautifulSoup):
    company_name = ''
    y_tunnus = ''
    email = ''
    website = ''
    address = ''
    city = ''
    country = 'Finland'
    managing_director = ''
    short_description = ''
    turnover_2023 = ''
    turnover_2022 = ''
    num_employees = ''
    entity_type = ''

    # Company name
    company_name_tag = company_soup.find(class_=company_name_css_class)
    if company_name_tag:
        company_name = company_name_tag.text

    # Y-tunnus
    profile_info_tag = company_soup.find(class_=profile_info_css_class)
    y_tunnus_tag = profile_info_tag.find('li')
    for tag in y_tunnus_tag.find_all(['i', 'div']):
        tag.decompose()
    if y_tunnus_tag:
        y_tunnus = y_tunnus_tag.text.replace("Y-tunnus", "").strip()

    # Company email
    email_tag = company_soup.find(class_=email_css_class)
    if email_tag:
        email = email_tag.text

    # Company website
    website_tag = company_soup.find(class_=website_css_class)
    if website_tag:
        website = website_tag.text

    # Company address
    address_tag = company_soup.find(class_=address_css_class)
    if address_tag:
        address = address_tag.text
        city = address.split()[-1]

    # Managing director
    director_tag = company_soup.find(class_=director_css_class).find("strong")
    if director_tag:
        managing_director = director_tag.text

    # Short description
    dt_tag = company_soup.find('dt', string="Toimialat")
    dd_tag = dt_tag.find_next_sibling('dd')
    short_description_tag = dd_tag.find("a")
    if short_description_tag:
        short_description = short_description_tag.text

    # Financial data
    table_tag = company_soup.find(class_=financial_table_css_class)
    financial_dict = extract_financial_data_from_table(table_tag)
    for year_key in financial_dict:
        if "2022" in year_key:
            turnover_2022 = financial_dict[year_key]
        elif "2023" in year_key:
            turnover_2023 = financial_dict[year_key]

    # Number of employees
    dt_tag = company_soup.find('dt', string="Toimipaikan henkilöstöluokka")
    dd_tag = dt_tag.find_next_sibling('dd')
    if dd_tag:
        num_employees = dd_tag.text.split()[0]

    # Type of entity
    dt_tag = company_soup.find('dt', string="Yhtiömuoto")
    dd_tag = dt_tag.find_next_sibling('dd')
    dd_tag.find("span").decompose()
    if dd_tag:
        entity_type = dd_tag.text

    company_info_dict = {
        "Company Name": company_name,
        "Y-tunnus": y_tunnus,
        "Email": email,
        "Website": website,
        "Office address": address,
        "City": city,
        "Country": country,
        "Managing Director": managing_director,
        "Short description (one chapter) of core business": short_description,
        "Turnover 2023": turnover_2023,
        "Turnover 2022": turnover_2022,
        "No of employees": num_employees,
        "Type of an entity": entity_type
    }

    return company_info_dict


def scrap_company_info(company_url: str):
    company_soup = get_page_soup(company_url)
    company_info = extract_company_info(company_soup)
    return company_info


if __name__ == "__main__":
    my_page_url = "https://www.finder.fi/Huolinta/Finnshipping+Ltd+Oy/Helsingfors/yhteystiedot/162707"

    my_soup = get_page_soup(my_page_url)
    extract_company_info(my_soup)
