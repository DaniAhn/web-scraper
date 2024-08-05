import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import sys
import lxml
import csv

class HomeListing:
    """
    Home listing on zillow.com.
    """
    def __init__(self, address: str, price: str, sqft: str, bd: str, ba: str):
        """
        Initializes a home listing object.

        Args:
            address (str): Address of the home.
            price (str): Price of the home. 
            sqft (str): Total square feet of the home.
            bd (str): Number of bedrooms.
            ba (str): Number of bathrooms.
        """
        self.address = address
        self.price = price
        self.sqft = sqft
        self.bd = bd
        self.ba = ba

def main()-> None:
    """
    Main entry point of the function. 
    """
    filename = "home_listings.csv"

    arg_list = sys.argv[1:]

    # Determines action based on provided command line arguments.
    if len(arg_list) != 1:
        exit()
    elif arg_list[0] == 'export': # Scrapes zillow.com and exports data to csv.
        home_listings = scrape_data()
        export_data(filename, home_listings)
    elif arg_list[0] == 'plot': # Reads data from csv and creates a scatterplot.
        plot_data(filename)
    else:
        exit()

def scrape_data()-> list[HomeListing]:
    """
    Scrapes home listings from zillow.com.

    Returns:
        list[HomeListing]: List of home listings successfully scraped.
    """
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

    # Iterates through every page in the search from the start page to the end page.
    for page in range(start_page, end_page + 1):

        # Formats url based on city and page number.
        url = base_url.format(city = city, page = page)
        print(url)

        # Sends a request to retrieve html content
        response = requests.get(url, headers=headers)
        print(f"{response.status_code}\n")

        if response.status_code == 200:
            # Creates a BeautifulSoup object to parse html content. 
            html_content = response.content
            html_doc = BeautifulSoup(html_content, "lxml")

            # Creates a container for home listings in the current page.
            listing_container = html_doc.find_all("li", class_="ListItem-c11n-8-102-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-102-0__sc-wtsrtn-0 hKdzLV kgwlbT")

            # Extracts data from the html content of each home listing.
            for home in listing_container:

                # Finds html tags corresponding to each of the data points.
                address_tag = home.find('address')
                price_tag = home.find('span', {'data-test': 'property-card-price'})

                details = home.find('ul', {'class': 'StyledPropertyCardHomeDetailsList-c11n-8-102-0__sc-1j0som5-0 exCsDV'})

                # Creates variables to store each of the attributes.
                if address_tag and price_tag:
                    address = address_tag.text.strip()
                    price = price_tag.text.strip()

                    if details:
                        li_elements = details.find_all('li')

                        if len(li_elements) == 3:
                            bedrooms = li_elements[0].text.strip().split()[0]
                            bathrooms = li_elements[1].text.strip().split()[0]
                            square_feet = li_elements[2].text.strip().split()[0]

                            # If all fields of data are filled, creates a home listing object.
                            home_listing = HomeListing(address, price[2:], 
                                                       square_feet, bedrooms, bathrooms)
                            
                            """
                            # Prints each home listing and its attributes to the terminal.
                            print(f"Address: {home_listing.address}")
                            print(f"Price: {home_listing.price}")
                            print(f"Sqft: {home_listing.sqft}")
                            print(f"Bd: {home_listing.bd}")
                            print(f"Ba: {home_listing.ba}")
                            print("\n")
                            """
                            
                            home_listings.append(home_listing)

    return home_listings

def export_data(filename: str, home_listings: list[HomeListing])-> None:
    """
    Exports home listings to a csv file.

    Args:
        filename (str): Name of the output csv file.
        home_listings (list[HomeListing]): List of home listing objects.
    """
    with open(filename, "w") as csv_file:
        # Sets each of the field names.
        fieldnames = ["Address", "Price", "Square Feet", "Bedrooms", "Bathrooms"]

        # Creates a csv DictWriter.
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Fills out the data points of each listing in a row.
        for listing in home_listings:
            writer.writerow({
                "Address": listing.address,
                "Price": f"${listing.price}", 
                "Square Feet": listing.sqft, 
                "Bedrooms": listing.bd, 
                "Bathrooms": listing.ba
            })

def plot_data(filename: str)-> None:
    """
    Plots a scatterplot of prices corresponding to square feet.

    Args:
        filename (str): Name of the input csv file.
    """
    home_listings = []

    # Creates a list of home listing objects based on input csv data. 
    with open(filename, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            home_listings.append(HomeListing(
                row["Address"], row["Price"].replace("$", ""), row["Square Feet"], 
                row["Bedrooms"], row["Bathrooms"]
            ))

    # Removes items in the list with empty sqft data.
    home_listings = [listing for listing in home_listings if "--" not in listing.sqft]

    for listing in home_listings:
        print(listing.sqft)
    # Creates lists for each of the data points in the scatterplot.
    sqft_dataset = [int((listing.sqft).replace(",", "")) for listing 
                    in home_listings]
    price_dataset = [int((listing.price).replace(",", "")) for listing 
                    in home_listings]

    plt.scatter(sqft_dataset, price_dataset, s=10)

    plt.xlim(0, 6000)
    plt.ylim(0, 4000000)

    plt.gca().yaxis.set_major_formatter(tkr.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    # Creates the scatterplot title along with labels for the x and y axes.
    plt.title("Price of Homes on Zillow in Victoria, BC by Square Feet", 
            family="Georgia", fontsize=16, pad=20, weight="bold")
    
    plt.xlabel(r"Square Feet ($\mathrm{ft}^2$)", family="Georgia", fontsize=12)
    plt.ylabel("Price (USD)", family="Georgia", fontsize=12)

    plt.grid(True, linestyle="--", linewidth=1, alpha=0.8)

    plt.show()

if __name__ == "__main__":
    main()