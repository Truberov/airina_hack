FROM python:3.10

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./classification_service /code/classification_service

EXPOSE 8080

ENTRYPOINT ["python", "-m", "classification_service"]