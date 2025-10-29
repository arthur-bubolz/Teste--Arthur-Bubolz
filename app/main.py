import sys
import warnings
import wikipedia as w
import uvicorn
from datetime import datetime
from crew import AiLatestDevelopment
from pydantic import BaseModel
from fastapi import FastAPI
from pydantic import BaseModel

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run(topico):
    """
    Run the crew.
    """

    texto = w.consulta_wikipedia(topico)

    if type(texto) == int:
        result = 'Erro - {texto}'
    else:
        inputs = {
            'topic': topico,
            'texto_wiki' : texto,
            'current_year' : str(datetime.now().year)
        }

    try:
        result = AiLatestDevelopment().crew().kickoff(inputs=inputs)
    except Exception as e:
        result = f"An error occurred while running the crew: {e}"
    return result

app = FastAPI()

class Topic(BaseModel):
    value: str
    
@app.get("/")
async def root():
    return {"message": "All working!"}

@app.post("/articlemaker")
async def square(topic: Topic):
    return {"article": run(topic.value)}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == '__main__':
    main()