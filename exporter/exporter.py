import aligner
import asyncio
import sqlite3

import csv

def query_db():
    conn = sqlite3.connect('./database/database.db')
    cursor = conn.cursor()
    cursor.execute("""
SELECT *
FROM articles
WHERE english_texts IS NOT NULL AND khmer_texts IS NOT NULL
  AND LENGTH(TRIM(english_texts)) > 0
  AND LENGTH(TRIM(khmer_texts)) > 0
""")
    results = cursor.fetchall()
    conn.close()
    return results

def print_scores(match):
    print(f"KH: {match['khmer']}")
    print(f"EN: {match['english']}")
    print(f"SCORE: {match['score']:.4f}")
    print("-" * 40)


def main():

    results = query_db()

    csv_file = open('scraped_pairs.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['ID', 'English_Text', 'Khmer_Text'])
    
    count = 0

    for row in results:
        kh_text = row[2]
        en_text = row[3]

        # Align the Khmer and English texts
        matches = asyncio.run(aligner.align_clauses(kh_text, en_text))

        # Print the results
        for match in matches:
            count += 1
            print_scores(match)
            csv_writer.writerow([count, match['english'], match['khmer']])



        

main()