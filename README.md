Boolean-Retrieval-Model
This project implements a Boolean retrieval model in Python that reads a collection of documents based on the Indian economy and builds both an inverted index and a positional index. These indexes are used to answer:

Boolean queries using combinations of terms and Boolean operators (AND, OR, NOT)

Proximity queries using terms and a skip-word value k (e.g., policy reform /5)

Methodology
Data Preprocessing: Stop word removal, lowercasing, stemming, and Unicode cleanup

Inverted Index: Built to support Boolean queries with proper operator precedence

Positional Index: Built to enable proximity search using term positions

Proximity Handling: Identifies documents where query terms appear within k words

Both inverted_index.txt and positional_index.txt files are generated during execution.

Dataset
The dataset consists of 30 text documents focused on the Indian economy, covering topics like GDP, inflation, employment, trade, budget policies, and more. The documents use overlapping vocabulary to support effective Boolean retrieval.

Limitations
Supports Boolean queries with unlimited use of AND, OR, and NOT

Works with both uppercase and lowercase operators

Supports complex nested queries using brackets

Usage
Boolean Query: growth AND inflation

Phrasal Query: foreign investment

Proximity Query: digital economy /7

Requirements
Python 3.6 or later

pip (Python package installer)

Installation
Download and extract the project files

Install any required Python packages

Run the script:

bash
Copy
Edit
python project.py
