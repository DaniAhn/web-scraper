# Zillow Scraper
Scrapes home listings from zillow.com and exports them to a csv file, with the option to plot a scatterplot comparing prices of home listings by square feet.

## Getting Started
### Installation
Make sure you have python installed. Install the required Python libraries by running the following command in the terminal window:
```
pip install requests beautifulsoup4 lxml matplotlib
```
### Usage
Navigate to the project directory in the terminal window.
#### Export data
Scrape zillow.com for home listings and export them to an external csv file by running the following command in the terminal:
```
python zillow-scraper export
```
The city is set to Victoria, BC by default. Edit the city to match the url for the search query of the desired location, along with the start and end pages. 

#### Plot data
To create a scatterplot comparing prices of home listings by square feet, run the following command in the terminal:
```
python zillow-scraper plot
```
This will open up a scatterplot in matplotlib. 

## Authors
Daniel Ahn
