import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib
import lxml
import csv

base_url = "https://www.zillow.com/homes/for_sale/{city}/{page}_p/"

city = "victoria-bc"
start_page = 1
end_page = 14

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-CA,en-US;q=0.7,en;q=0.3",
    "Referer": "https://www.zillow.com/victoria-bc/?searchQueryState=%7B%22pagination",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
}

for page in range(start_page, end_page + 1):
    url = base_url.format(city = city, page = page)
    print(url)

    response = requests.get(url, headers=headers)
    print(f"{response.status_code}\n")

    if response.status_code == 200:
        html_content = response.content

        html_doc = BeautifulSoup(html_content, "lxml")
        print(f"{html_doc.prettify()}\n")

        home_listings = html_doc.find_all("li", class_="ListItem-c11n-8-102-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-102-0__sc-wtsrtn-0 hKdzLV kgwlbT")

        for home in home_listings:
            address_tag = home.find('address')
            address = address_tag.text.strip() if address_tag else "N/A"

            price_tag = home.find('span', {'data-test': 'property-card-price'})
            price = price_tag.text.strip() if price_tag else "N/A"

            details = home.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0 exCsDV'})
            
            if details:
                li_elements = details.find_all('li')
                bedrooms = li_elements[0].text.strip().split()[0] if len(li_elements) > 0 else "N/A"
                bathrooms = li_elements[1].text.strip().split()[0] if len(li_elements) > 1 else "N/A"
                square_feet = li_elements[2].text.strip().split()[0] if len(li_elements) > 2 else "N/A"
            else:
                bedrooms = bathrooms = square_feet = "N/A"

            print(f"Address: {address}")
            print(f"Price: {price}")
            print(f"Sqft: {square_feet}")
            print(f"Bd: {bedrooms}")
            print(f"Ba: {bathrooms}")
            print("\n")
                            
    print("\n--------------------------\n")