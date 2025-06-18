from scraper import fetcher
from scraper import parser

hello = fetcher.fetch_html("https://moc.gov.kh/news/3168")

if hello:
    parsed_data = parser.parse_html(hello.text)
    print(parsed_data.texts)