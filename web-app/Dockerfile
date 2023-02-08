FROM python:3.10.9

COPY requirements.txt app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8003

ENTRYPOINT ["streamlit", "run", "Project_Overview.py", "--server.port=8003", "--server.address=0.0.0.0"]
