import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import lxml
import csv

class HomeListing:
    def __init__(self, address: str, price: str, sqft: str, bd: str, ba: str):
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

home_listings = []

for page in range(start_page, end_page + 1):
    url = base_url.format(city = city, page = page)
    print(url)

    response = requests.get(url, headers=headers)
    print(f"{response.status_code}\n")

    if response.status_code == 200:
        html_content = response.content

        html_doc = BeautifulSoup(html_content, "lxml")

        listing_container = html_doc.find_all("li", class_="ListItem-c11n-8-102-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-102-0__sc-wtsrtn-0 hKdzLV kgwlbT")

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

                        home_listing = HomeListing(address, price[2:], square_feet, bedrooms, bathrooms)
                        print(f"Address: {home_listing.address}")
                        print(f"Price: {home_listing.price}")
                        print(f"Sqft: {home_listing.sqft}")
                        print(f"Bd: {home_listing.bd}")
                        print(f"Ba: {home_listing.ba}")
                        print("\n")

                        home_listings.append(home_listing)

with open("home_listings.csv", "w") as csv_file:
    fieldnames = ["Address", "Price", "Square Feet", "Bedrooms", "Bathrooms"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for listing in home_listings:
        writer.writerow({
            "Address": listing.address,
            "Price": f"${listing.price}", 
            "Square Feet": listing.sqft, 
            "Bedrooms": listing.bd, 
            "Bathrooms": listing.ba
        })

for listing in home_listings:
    if listing.sqft == "--":
        home_listings.remove(listing)

sqft_dataset = [int((listing.sqft).replace(",", "")) for listing 
                in home_listings]
price_dataset = [int((listing.price).replace(",", "")) for listing 
                 in home_listings]

plt.scatter(sqft_dataset, price_dataset)

plt.xlabel("Square Feet")
plt.ylabel("Price (USD)")
plt.title("Price of Homes on Zillow in Victoria, BC by Square Feet")

plt.grid(True)

plt.show()