# MTT Analysis

[![coverage report](https://gitlab.com/mrph-dev/analysis/badges/main/coverage.svg)](https://gitlab.com/mrph-dev/analysis/-/commits/main)

## Built with

### Frontend

The front end is built using [Svelte](https://svelte.dev/) to develop the front:

```
cd frontend

npm install

npm run dev

```

### Backend

The back end is built using [FastAPI](https://fastapi.tiangolo.com/) to develop back end

```
cd backend

pipenv shell

pipenv update

uvicorn main:app --reload
```

Add a .env file in the backend folder with a link to your mySQLDB

```
DATABASE_URL=mysql+pymysql://<username>:<password>@<location>:3306/testuser?charset=utf8mb4
```
