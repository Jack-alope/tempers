## Development 
If you are looking to develop and contribute to this software here is a good place to start. 
1. Create a mySQL database, either locally or on a remote server. 
2. Fork and clone this repository. 
3. Create a `.env` file in the `backend/` directory with the login to your mysql database. It should look something like:
    ```bash
    DATABASE_URL=mysql+pymysql://<username>:<password>@<location>:3306/<db_name>
    ```
4. Change the `API_URL` in `frontend/rollup.config.js` to `http://0.0.0.0:8000`
5. Start the backend in one terminal window.
    ```bash
    cd backend/
    pipenv shell
    pipenv sync --dev
    uvicorn main:app --reload
    ```
6. Start the frontend in a different terminal window.
    ```bash
    cd frontend/
    ```

    Comment line 46-49 of `rollup.config.js`
    
    
    ```
    npm ci
    npm run dev
    ```
7. Access the user interface via `http://localhost:5000/`. Changes you make to the code should be automatically updated, no need to rebuild every time.

---
## Making Database Changes

To manage database versioning we use [alembic](https://github.com/sqlalchemy/alembic) after making changes to the database schema in [models.py](backend/models.py) from your python environment run:
```
alembic revision --autogenerate -m "<commit message>"
```
This with automatically generate code to upgrade and downgrade the database to and from that point.  

Then to upgrade the database to reflect the changes run:

```
alembic upgrade head 
```
View revsions to the database by running:
```
alembic history
```


---

## Commiting Changes

### Python Pre Commit Checks

Before committing it is recommended to run [Black](https://github.com/psf/black) and [Pylint](https://github.com/PyCQA/pylint), this keeps code in consistent of of high quality. To do this from your python environment fun:

    
    black <path/to/backend>
    
Black will auto automatically reformat the python code accoring to blacks format rules.

```
pylint $(git ls-files '*.py'
```

Pylint will show warnings in the console, this doesn't have to be perfect, but try to ensure its at least a 7/10.

### Svelte Pre commit checks
Note: There are alot of linting errors in svelte at the moemt so dont worry about running this too much, till we make some preogress getting it up to speed.

```
npm run lint:fix
```

## Commit 
Note: Remember to exclude the changed comments in [rollup.config.js](./frontend/rollup.config.js) on line 46
```
git commit -m "<commit message>"
```

