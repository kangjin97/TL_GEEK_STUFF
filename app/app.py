from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# Set up the Selenium WebDriver (Make sure to have the ChromeDriver installed)
service = Service('C:\webdrivers\chromedriver-win64\chromedriver.exe')  # Update the path to your ChromeDriver
driver = webdriver.Chrome(service=service)

# URL of the website to scrape
url = "https://questlog.gg/throne-and-liberty/en/auction-house/traitextract/accessories/ring"

# Open the website with Selenium
driver.get(url)

# Wait for the page to load
time.sleep(5)  # Adjust the sleep time if necessary

# Get the page source and close the driver
html_content = driver.page_source
driver.quit()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the specific data table
data_table = soup.find('div', class_='vue3-easy-data-table styled-data-table overflow-hidden rounded-md')

# Function to get CSS selector
def get_css_selector(element):
    parts = []
    for parent in element.parents:
        siblings = list(parent.children)
        index = siblings.index(element) + 1
        parts.append(f"{parent.name}:nth-child({index})")
        element = parent
    return ' > '.join(reversed(parts))

# Extract all spans within the data table
spans = data_table.find_all('span') if data_table else []

# Initialize lists to store CSS selectors and their text
selectors = []
texts = []

# Extract text content and CSS selectors
for span in spans:
    text_content = span.text.strip()
    if text_content:
        css_selector = get_css_selector(span)
        selectors.append(css_selector)
        texts.append(text_content)

# Create a DataFrame and save it to an Excel file
data = {'CSS Selector': selectors, 'Text': texts}
df = pd.DataFrame(data)
df.to_excel('web_text_data_with_css_selectors.xlsx', index=False)

print("Data has been successfully saved to web_text_data_with_css_selectors.xlsx")



