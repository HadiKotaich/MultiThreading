import requests
from bs4 import BeautifulSoup
from Page import Page

class ContentProvider():
  def __init__(self):
    pass
  
  def fetch_webpage_content(self, url) -> Page:
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        page = Page(url, soup)
        return page
    else:
        raise Exception(f"Failed to retrieve content from {url} with status code {response.status_code}")
