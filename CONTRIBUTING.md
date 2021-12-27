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
    pipenv update
    uvicorn main:app --reload
    ```
6. Start the frontend in a different terminal window.
    ```bash
    cd frontend/
    ```

    Comment line 46-49 of `rollup.config.js`
    
    
    ```
    npm install
    npm run dev
    ```
7. Access the user interface via `http://localhost:5000/`. Changes you make to the code should be automatically updated, no need to rebuild every time.
