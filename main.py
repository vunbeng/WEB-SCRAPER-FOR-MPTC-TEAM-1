from scraper import fetcher, parser, aligner
from database import app
import time


def main(url):
    """
    Main function to run the scraper, parse the HTML, and store the data in the database.
    """
    # Fetch HTML content
    response = fetcher.fetch_html(url)
    
    if response:
        # Parse the HTML content
        parsed_data = parser.parse_html(response.text)
        
        # Align Khmer and English texts
        aligned_data = aligner.split_text(parsed_data)
        
        # Create a new entry in the database
        app.create_entry(url=response.url, 
                         khmer_texts=aligned_data['khmer'], 
                         english_texts=aligned_data['english'])


    
if __name__ == "__main__":
    url_range = input("Enter the range of pages to scrape (e.g., 1-5): ")
    start_index, end_index = map(int, url_range.split('-'))

    start_time = time.time()
    print("Starting the scraper...")


    for i in range(start_index, end_index + 1):
        url = f"https://moc.gov.kh/news/{i}"
        main(url)

    end_time = time.time()
    print(f"Scraper finished in {end_time - start_time:.2f} seconds")
    