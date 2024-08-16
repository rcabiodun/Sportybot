import requests
from bs4 import BeautifulSoup

# Step 1: Make a GET request to the website
url = 'https://livescores.biz/'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Step 2: Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.text)

    # Step 3: Find the elements that contain the article titles
    # This will vary depending on the structure of the website
    # Here we're assuming the titles are in <h2> tags with a class name "title"
    # titles = soup.find_all('h2', class_='title')

    # # Step 4: Extract and print the titles
    # for title in titles:
    #     print(title.get_text())
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')
