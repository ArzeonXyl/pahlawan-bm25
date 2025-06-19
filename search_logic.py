# arzeonxyl/pahlawan-bm25/pahlawan-bm25-8ebf1d8ad63d6ecca710d88fc830f10dab0dd18b/search_logic.py
import json
from bm25 import parse_json_coll, score_BM25 # Mengimpor fungsi dari bm25.py
import os

def perform_search(query_text):
    # Tentukan path absolut untuk file data dan stopwords
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, 'data', 'pahlawan.json')
    stopwords_path = os.path.join(current_dir, 'stopwords_indonesia.txt')

    # Load stopwords
    with open(stopwords_path, 'r', encoding='utf-8') as stopwords_f:
        stop_words = [word.strip() for word in stopwords_f.read().split(',') if word.strip()] # Pastikan tidak ada string kosong

    # Load data & build BOW
    BowDocColl, OriginalDocs = parse_json_coll(data_path, stop_words)

    # Hitung DF
    df = {}
    for doc in BowDocColl:
        for term in doc[1]:
            df[term] = df.get(term, 0) + 1

    # Skoring BM25
    results = score_BM25(BowDocColl, query_text, df, stop_words)

    # Ambil top 10 hasil
    top_results = sorted(results.items(), key=lambda x: x[1], reverse=True)[:10]

    # Tampilkan hasil dengan data asli + score
    output = []
    for doc_id, score in top_results:
        doc = OriginalDocs[doc_id].copy()
        doc["score"] = score
        output.append(doc)

    return json.dumps(output, indent=2, ensure_ascii=False)
