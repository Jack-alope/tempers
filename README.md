# Rianú

This project is called `rianú`, which aptly means tracking in Irish.  
If you are a fan of recursive acronyms `rianú is absolutely not useless`.

[![pylint](https://costa-lab.gitlab.io/rianu/badges/pylint.svg)](https://costa-lab.gitlab.io/rianu/lint/)

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
DATABASE_URL=mysql+pymysql://<username>:<password>@<location>:3306/<db_name>?charset=utf8mb4
```
