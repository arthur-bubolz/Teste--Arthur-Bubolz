import requests

#Realiza uma requisição POST para a API ArticleMaker, enviando um tema.
def request(input):
    url = "http://localhost:8000/articlemaker"

    data = {
        "value": input
    }

    response = requests.post(url, json=data)

    if response.status_code == 200:
        resultado_json = response.json()
        return resultado_json #Em casos de sucesso retorna o conteúdo
    else:
        return f"Erro: {response.status_code}" #Em casos de falha retorna erro
    
def main():
    input = 'Saimaa'
    resultado = request(input)
    print(resultado)

if __name__ == '__main__':
    main()