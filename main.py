from scraper import fetcher, parser, aligner
from database import app

response = fetcher.fetch_html("https://moc.gov.kh/news/3167")

if response:
    parsed_data = parser.parse_html(response.text)
    aligned_data = aligner.split_text(parsed_data)

    app.create_entry(url=response.url, 
                     khmer_texts=aligned_data['khmer'], 
                     english_texts=aligned_data['english'])
    
