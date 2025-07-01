import re
import asyncio
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 🧠 Load LaBSE once
model = SentenceTransformer("sentence-transformers/LaBSE")

# ✂️ Khmer Chunker (also handles numeric bullets and punctuation)
def chunk_kh(text: str) -> list[str]:
    pattern = r"[។៖,]|[~\-]+|\(\d+\)[\-–]?"
    return [s.strip() for s in re.split(pattern, text) if s.strip()]

# ✂️ English Chunker (also splits by semicolons, parentheses, bullets, conjunctions)
def chunk_en(text: str) -> list[str]:
    pattern = r"[.;:!?]|\(\d+\)|\band\b|\bbut\b|\bor\b"
    return [s.strip() for s in re.split(pattern, text, flags=re.IGNORECASE) if s.strip()]

# 🧬 Embed phrases with LaBSE
async def embed_phrases(phrases: list[str]) -> np.ndarray:
    return model.encode(phrases, normalize_embeddings=True)

# 🔗 Align Khmer & English chunks by cosine similarity
async def align_clauses(kh_text: str, en_text: str, threshold=0.6, top_k=10):
    kh_chunks = chunk_kh(kh_text)
    en_chunks = chunk_en(en_text)

    kh_vecs, en_vecs = await asyncio.gather(
        embed_phrases(kh_chunks),
        embed_phrases(en_chunks)
    )

    scores = cosine_similarity(kh_vecs, en_vecs)
    pairs = []

    for i, row in enumerate(scores):
        j = np.argmax(row)
        score = row[j]
        if score >= threshold:
            pairs.append({
                "khmer": kh_chunks[i],
                "english": en_chunks[j],
                "score": float(score)
            })

    return sorted(pairs, key=lambda x: x["score"], reverse=True)[:top_k]

async def main():
    kh = """
        (បន្ទាយមានជ័យ)៖ នាព្រឹកថ្ងៃអង្គារ ទី១៣ ខែឧសភា ឆ្នាំ២០២៥ លោក តាន់ យុវរដ្ឋ អគ្គនាយករងនៃអគ្គនាយកដ្ឋានជំរុញពាណិជ្ជកម្ម និង លោក កែ សួន សុភាព អភិបាលរងនៃគណៈអភិបាលខេត្តបន្ទាយមានជ័យ បានអញ្ជើញជាគណៈអធិបតីក្នុងពិធីបើកសិក្ខាសាលាស្តីពី “ការពង្រឹងសមត្ថភាពអ្នកផលិត និងកែច្នៃផលិតផល” ក្នុងការស្វែងរកទីផ្សារក្នុងនិងក្រៅប្រទេស នៅខេត្តបន្ទាយមានជ័យ ដែលមានការចូលរួមពីអាជ្ញារធរខេត្ត មន្រ្តីរាជការមកពីមន្ទីរពាក់ព័ន្ធ ជាពិសេសធុរជន ពាណិជ្ជករ សិប្បករ និងអាជីវករក្នុងខេត្តជាច្រើនរូប។ សិក្ខាសាលានេះ ធ្វើឡើងក្នុងគោលបំណងដើម្បីពង្រឹងសមត្ថភាពអ្នកផលិតឱ្យអភិវឌ្ឍផលិតផលរបស់ខ្លួនស្របតាមស្តង់ដា លក្ខខណ្ឌតម្រូវនានាដែលកំណត់ដោយច្បាប់ និងឆ្លើយតបទៅនឹងតម្រូវការទីផ្សារ សំដៅលើកកម្ពស់ភាពប្រកួតប្រជែង តាមរយៈការជ្រៀតចូល និងទទួលបានចំណែកទីផ្សារសមរម្យ។ សិក្ខាសាលានេះ ក៏បានផ្តល់ជូននូវចំណេះដឹងថ្មីៗជូនដល់ផលិតករ អាជីវករទាក់ទងនឹងការផលិត ការវេចខ្ចប់ ព្រមទាំងនីតិវិធីចុះបញ្ជីក្រុមហ៊ុន ផងដែរ។
        """
    en = """
        Mr. TAN Yuvaroath, Deputy Director-General of the General Directorate of Trade Promotion, presided over the opening ceremony of the seminar on "Strengthening the Capacity of Producers and Processors" to explore domestic and international market opportunities in Banteay Meanchey Province. ... (Banteay Meanchey): On the morning of Tuesday, 13 May 2025, Mr. TAN Yuvaroath, Deputy Director-General of the General Directorate of Trade Promotion, and Mr. KE Soun Sopheap, Deputy Governor of Banteay Meanchey Province, presided over the opening ceremony of the seminar on "Strengthening the Capacity of Producers and Processors" to explore domestic and international market opportunities in Banteay Meanchey Province.  The event was attended by provincial authorities, civil servants from relevant departments, and entrepreneurs, traders, and businessmen from across the province. The main objective of this seminar was to strengthen the capacity of producers to develop products compliant with legal standards and requirements, and to respond to market demands. This aimed to enhance competitiveness through market penetration and the attainment of a fair market share. The seminar also provided participants with new knowledge related to production, packaging, and the company registration process.        """

    results = await align_clauses(kh, en)

    for match in results:
        print(f"KH: {match['khmer']}")
        print(f"EN: {match['english']}")
        print(f"SCORE: {match['score']:.4f}")
        print("-" * 40)

asyncio.run(main())