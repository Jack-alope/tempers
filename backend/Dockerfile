FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install pipenv -y
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 8000
CMD ["uvicorn", "main:app", "--root-path", "/api", "--host", "0.0.0.0"]
