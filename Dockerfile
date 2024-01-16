FROM python:3.11.5-alpine

WORKDIR /housing_api

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./app

CMD ["python", "./app/housing_data.py"]


