

With this setup, we generate the time series (using api generate_timeseries) in the background using Celery tasks, save it to the PostgreSQL database, and later fetch the data using the FastAPI (fetch_timeseries) backend.

The React.js frontend can fetch the data and plot it using Plotly.