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

## Commiting Changes

### Pre Commit Checks

Before commiting changes  `pre-commit install` needs to be run from withing the python environment.  This installs a git pre-commit hook that ensures the code is formatted and linted correctlly before commiting.  

```
cd backend/
pipenv shell
pipenv sync --dev
pre-commit install

git commit -m "<commit message>"
```

This will format coding using [Black](https://github.com/psf/black).
This will also lint the code with [pylint](https://github.com/PyCQA/pylint.


If [Black](https://github.com/psf/black) fixs code run
```
git commit -m "<commit message>"
```
This will commit the newly formated code.

If [pylint](https://github.com/PyCQA/pylint) fails it will show errors that need to be fixed.  Note: pylint does not need a perficet score of 10 to commit it just needs above a 7.