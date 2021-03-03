import os
from typing import Dict, List
import json

import requests
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity


URL = "https://model-apis.semanticscholar.org/specter/v1/invoke"
MAX_BATCH_SIZE = 16



def embed(papers):
    embeddings_by_paper_id: Dict[str, List[float]] = {}

    for chunk in chunks(papers):
        # Allow Python requests to convert the data above to JSON
        response = requests.post(URL, json=chunk)

        if response.status_code != 200:
            raise RuntimeError("Sorry, something went wrong, please try later!")

        for paper in response.json()["preds"]:
            embeddings_by_paper_id[paper["paper_id"]] = paper["embedding"]

    return embeddings_by_paper_id

def chunks(lst, chunk_size=MAX_BATCH_SIZE):
    """Splits a longer list to respect batch size"""
    for i in range(0, len(lst), chunk_size):
        yield lst[i : i + chunk_size]


import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('SPECTERExpenses03.xlsx')
worksheet = workbook.add_worksheet()

path = 'C:\\Users\\huaweı\\Desktop\\position-rank-master\\AnaMetinler'
all_files = os.listdir(path)
for i in range(0,  len(all_files)):
    with open(path + '\\' + all_files[i], 'r', encoding="utf-8") as file:
        data = file.read().replace('\n', '')
        for j in range(0, len(all_files)):
            with open(path + '\\' + all_files[j], 'r', encoding="utf-8") as file:
                data1 = file.read().replace('\n', '')
                SAMPLE_PAPERS = [
                    {
                        "paper_id": "A",
                        "title": "Hospital outbreak of Middle East respiratory syndrome coronavirus",
                        "abstract": data
                    },
                    {
                        "paper_id": "B",
                        "title": "Hospital outbreak of Middle East respiratory syndrome coronavirus",
                        "abstract": data1
                    },

                ]
                all_embeddings = embed(SAMPLE_PAPERS)
                result = 1 - spatial.distance.cosine(list(all_embeddings.values())[0], list(all_embeddings.values())[1])
                worksheet.write(i, j, result)
                print(i,j,result)

workbook.close()


