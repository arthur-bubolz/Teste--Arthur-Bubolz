FROM python:3.11.9

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/ /app/app

WORKDIR /app/app

EXPOSE 8000

CMD ["python", "main.py"]
