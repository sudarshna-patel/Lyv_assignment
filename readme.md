Lyv Assignment to generate timeseries data

With this setup, we generate the time series (using api generate_timeseries) in the background using Celery tasks, save it to the PostgreSQL database, and later fetch the data using the FastAPI (fetch_timeseries) backend.

The React.js frontend can fetch the data and plot it using Plotly.


# Running the Application
cd backend
# In one terminal, start the FastAPI backend server
1) uvicorn main:app --reload
# In another terminal, start the Celery worker, make sure redis is running before executing celery
2) celery -A main.celery worker --loglevel=info

# In a third terminal, navigate to the frontend directory and start the React.js frontend
cd frontend
npm install
npm start

Note: This app doesn't use ML model instead it generates synthetic timeseries data. I used the sine function to simulate the daily and seasonal variations.