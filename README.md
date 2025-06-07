# Boolean-Retrieval-Model  
This project implements a Boolean retrieval model in Python that reads a  
collection of documents based on the Indian economy and builds an inverted and positional index,  
which is used to answer Boolean queries expressed as combinations of  
terms and Boolean operators and Proximity queries expressed as terms  
and k (Skip words value).

## Methodology  
1. Data Preprocessing for stop words removal, lower case, stemming  
and removing Unicode.  
2. Built Inverted Index and applied precedence to deal with Boolean  
queries and tokenization of queries.  
3. Built Positional Index and extracted positional lists for Proximity  
queries.  
4. Skipped k words mentioned by the query by subtracting  
positions and extracting the required k-positioned documents.  
5. Both inverted_index.txt and positional_index.txt files are created during execution.

## Dataset  
The dataset contains 30 text documents based on various Indian economy topics  
like GDP, inflation, employment, agriculture, budget policies, and more.  
These documents contain overlapping vocabulary to support Boolean and proximity search.

## Limitations:  
• It can run Boolean queries with unlimited "and or not"  
• It can run with both upper and lower case "and or not"  
• It can run complex queries with brackets  

## Usage  
• Boolean Queries: growth AND inflation  
• Phrasal Queries: foreign investment  
• Proximity Queries: digital economy /7  

## Requirements  
Python 3.6 or later  
pip (Python package installer)

## Installation  
• Download and extract Project  
• Install all the required Python packages  
• Run project.py file  
```bash
python project.py


