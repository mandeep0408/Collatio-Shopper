from bs4 import BeautifulSoup
import pandas as pd

# Read the index.html file
with open('index.html', 'r') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find all div elements with class "a-section a-spacing-base a-text-center"
div_list = soup.find_all('div', class_='a-section a-spacing-base a-text-center')

# Initialize empty lists to store the extracted data
links = []
titles = []
prices = []
mrps = []

# Loop through each div element
for div in div_list:

    # Extract title from span element with class "a-size-base-plus a-color-base"
    span_title = div.find('span', class_='a-size-base-plus a-color-base')
    title = span_title.text if span_title else ''

    # Extract price from span element with class "a-price-whole"
    span_price = div.find('span', class_='a-price-whole')
    price = span_price.text.replace(',', '') if span_price else ''

    # Extract MRP from span element with class "a-offscreen"
    span_mrp = div.find('span', class_='a-offscreen')
    mrp = span_mrp.text.replace(',', '') if span_mrp else ''

    # Extract link from img element with class "s-image"
    img = div.find('img', class_='s-image')
    link = img['src'] if img else ''

    # Append the extracted data to the respective lists
    links.append(link)
    titles.append(title)
    prices.append(price)
    mrps.append(mrp)

# Create a dictionary to store the extracted data
data = {
    'Title': titles,
    'Price': prices,
    'MRP': mrps,
    'Link': links,
    
}

# Convert the dictionary to a DataFrame using pandas
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv('amazon_data.csv', index=False)
