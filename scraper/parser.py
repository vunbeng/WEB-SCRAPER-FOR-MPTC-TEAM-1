from bs4 import BeautifulSoup

def parse_html(html_content):
    """
    Parses the HTML content and extracts relevant information.

    Args:
        html_content (str): The HTML content to parse.

    Returns:
        dict: A dictionary containing extracted information.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Example extraction logic (modify as needed)
    title = soup.title.string if soup.title else 'No title found'
    paragraphs = [p.get_text() for p in soup.find_all('p')]
    
    return {
        'title': title,
        'paragraphs': paragraphs
    }