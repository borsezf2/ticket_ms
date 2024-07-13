FROM python:3.8.10

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 9017

CMD ["python3","app.py","--host", "0.0.0.0"]


