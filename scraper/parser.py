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
    paragraphs = soup.find_all('div', id='paragraphBlock')  # Adjust the selector based on actual HTML structure
    
    texts = ""

    for paragraph in paragraphs:
        texts += paragraph.get_text(separator=' ', strip=True) + ' '

    return {
        'title': title,
        'texts': texts
    }