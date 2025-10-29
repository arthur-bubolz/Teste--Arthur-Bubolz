import requests
from bs4 import BeautifulSoup
import re

# Função para consultar a API da Wikipedia
def consulta_wikipedia(pagina):
    url = f"https://pt.wikipedia.org/w/api.php"
    
    params = {
        'action': 'query',
        'format': 'json',  
        'prop': 'extracts',  
        'exintro': True,  
        'titles': pagina  
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        
        for page_id, page_info in pages.items():
            if 'extract' in page_info:
                return clean_text(page_info['extract'])
            else:
                return 0
    else:
        return int(response.status_code)

#Função para limpar texto resultante da consulta
def clean_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    cleaned_text = soup.get_text()
    cleaned_text = re.sub(r'http\S+', '', cleaned_text)  
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
    cleaned_text = re.sub(r'[^\w\s,.?!]', '', cleaned_text)

    return cleaned_text


