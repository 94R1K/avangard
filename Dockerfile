FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt .
RUN pip3 install --upgrade pip && pip3 install -r ./requirements.txt --no-cache-dir
COPY ./avangard_task .

EXPOSE 5000

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
