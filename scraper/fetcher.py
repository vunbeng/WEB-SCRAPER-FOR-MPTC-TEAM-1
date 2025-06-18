import requests

def fetch_html(url):
    """
    Fetches the HTML content of a given URL.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        return response
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None