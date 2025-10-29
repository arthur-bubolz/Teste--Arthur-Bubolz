import sys
import warnings
from datetime import datetime
from typing import Union, Dict, Any

#Dependências de Terceiros (FastAPI/Pydantic)
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

#Dependências da Aplicação (Local)
import wikipedia as w
from crew import AiLatestDevelopment

#Ignora avisos específicos de bibliotecas (como pysbd) para manter o console limpo.
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

#Endereço e porta para aplicação
HOST_API = "0.0.0.0"
PORT_API = 8000

#Obter texto base da Wikipedia
def obter_texto_wikipedia(topico: str) -> Union[str, int]:
    return w.consulta_wikipedia(topico)

#Função principal para geração de artigo
def gerar_artigo_com_ia(topico: str) -> Dict[str, Any] | str:
    texto_wikipedia = obter_texto_wikipedia(topico)

    #Tratar erros de consulta na Wikipedia
    if isinstance(texto_wikipedia, int):
        return f"❌ Erro: Falha ao obter conteúdo da Wikipedia para '{topico}'. Código: {texto_wikipedia}"
    
    #Inputs - Crew AI
    inputs_ai = {
        'topic': topico,
        'texto_wiki': texto_wikipedia,
        'current_year': str(datetime.now().year)
    }

    #Execução de processo - Crew AI
    try:
        resultado_final = AiLatestDevelopment().crew().kickoff(inputs=inputs_ai)
        return resultado_final #Retorno de JSON com título, artigo e keywords
    except Exception as e:
        return f"⚠️ Erro ao executar a Crew AI: {e}" # Tratamento em casos de erro 

#Definições da API FastAPI
app = FastAPI(
    title="ArticleMaker API",
    description="API para gerar artigos informativos baseados em tópicos da Wikipedia e processamento de IA."
)

#Modelo Pydantic para o corpo da requisição POST.
class TopicRequest(BaseModel):
    value: str

#Endpoint de verificação de saúde da API.
@app.get("/")
async def health_check():
    return {"status": "OK", "message": "API operacional!"}

#Endpoint principal para solicitar a criação de um artigo.
@app.post("/articlemaker")
async def criar_artigo(tema_requisicao: TopicRequest):
    resultado_artigo = gerar_artigo_com_ia(tema_requisicao.value)
    return {"article": resultado_artigo}

#Inicialização do Servidor Local
def main():
    print(f"🚀 Iniciando servidor em http://{HOST_API}:{PORT_API}")
    uvicorn.run(app, host=HOST_API, port=PORT_API)

if __name__ == '__main__':
    main()