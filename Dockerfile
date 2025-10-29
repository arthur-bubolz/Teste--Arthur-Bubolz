# Escolher uma imagem base do Python
FROM python:3.11.9

# Copiar o requirements.txt para dentro do contêiner
COPY ./requirements.txt /app/requirements.txt

# Instalar as dependências do Python
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copiar o código-fonte da aplicação para o contêiner
COPY ./app/ /app/app

WORKDIR /app/app

# Comando que executa o script principal
CMD ["python", "main.py"]