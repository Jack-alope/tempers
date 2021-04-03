FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install pipenv -y
RUN pipenv install --system --deploy --ignore-pipfile
#RUN python3 -m pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn"  , "main:app", "--reload", "--host", "0.0.0.0"]
