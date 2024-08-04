import requests
from bs4 import BeautifulSoup
import matplotlib
import lxml
import csv

class HomeListing:
    def __init__(self, address, price, sqft, bd, ba):
        self.address = address
        self.price = price
        self.sqft = sqft
        self.bd = bd
        self.ba = ba


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

        listing_container = html_doc.find_all("li", class_="ListItem-c11n-8-102-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-102-0__sc-wtsrtn-0 hKdzLV kgwlbT")

        home_listings = []

        for home in listing_container:
            address_tag = home.find('address')
            price_tag = home.find('span', {'data-test': 'property-card-price'})

            details = home.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0 exCsDV'})

            if address_tag and price_tag:
                address = address_tag.text.strip()
                price = price_tag.text.strip()

                if details:
                    li_elements = details.find_all('li')

                    if len(li_elements) == 3:
                        bedrooms = li_elements[0].text.strip().split()[0]
                        bathrooms = li_elements[1].text.strip().split()[0]
                        square_feet = li_elements[2].text.strip().split()[0]

                        home_listing = HomeListing(address, price, square_feet, bedrooms, bathrooms)
                        home_listings.append(home_listing)

        with open("home_listings.csv", "w") as csv_file:
            fieldnames = ["Address", "Price", "Square Feet", "Bedrooms", "Bathrooms"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for listing in home_listings:
                writer.writerow({
                    "Address": listing.address, 
                    "Price": listing.price, 
                    "Square Feet": listing.sqft, 
                    "Bedrooms": listing.bd, 
                    "Bathrooms": listing.ba
                })

