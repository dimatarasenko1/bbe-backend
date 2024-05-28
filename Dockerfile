FROM python:3.11

WORKDIR /app
ENV HOME /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80:80

CMD ["uvicorn", "main:app", "--port", "80", "--host", "0.0.0.0"]