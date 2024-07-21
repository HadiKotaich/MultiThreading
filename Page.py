from urllib.parse import urljoin, urlparse

class Page():
  def __init__(self, url, soup):
    self.links = self.get_all_links(url, soup)
    self.content_peek = self.get_content_peek(soup)
    self.title = self.content_peek.split('\n')[0]

  def get_all_links(self, url, soup):
      # Find all anchor tags
      anchor_tags = soup.find_all('a')
      parsed_url = urlparse(url)
      base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
      # Extract and clean URLs
      links = []
      for tag in anchor_tags:
          href = tag.get('href')
          if href:
              # Construct absolute URLs if they are relative
              full_url = urljoin(url, href)
              if full_url.startswith(base_url):
                links.append(full_url)

      return links

  def get_content_peek(self, soup):
    # Get text from paragraphs, ignoring some tags containing additional info
    text = ' '.join([p.get_text() for p in soup.find_all(['p']) if not p.has_attr('class')])
    # Shorten the text to provide a summary
    summary = soup.title.string + "\n" + text[:500] + "..." if len(text) > 500 else text
    return summary
