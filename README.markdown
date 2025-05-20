# Germany Public Transport Efficiency Tracker

A Streamlit-based data science application to analyze train delays in Germany, focusing on Deutsche Bahn services. The app visualizes delay patterns, route reliability, and public sentiment, with an **A/B testing** experiment to compare two delay distribution visualizations (histogram vs. box plot) to optimize user engagement.

## Features

- **Interactive Delay Map**: Displays average train delays by station across German cities using Folium, with color-coded markers for severity.
- **A/B-Tested Delay Distribution**: Users are randomly shown either a histogram (Variant A) or box plot (Variant B) for delay minutes, filterable by city.
- **Sentiment Word Cloud**: Visualizes public sentiment about Deutsche Bahn using mock X posts (extensible to real X API data).
- **Route Reliability Table**: Shows reliability scores (% of on-time trips) for train routes.
- **A/B Test Analysis**: Admin view with interaction metrics (filter clicks, time spent) and statistical comparison (t-test) of visualization variants.

## A/B Testing

The app tests two visualizations for the delay distribution:
- **Variant A (Histogram)**: Shows frequency of delays, emphasizing distribution shape.
- **Variant B (Box Plot)**: Highlights median, quartiles, and outliers for clearer insights.
- **Metrics**: Tracks city filter clicks and session time, logged to `ab_test_results.csv`.
- **Analysis**: Admin view displays average interactions and time spent per group, with a t-test to assess significance (p < 0.05).

## Prerequisites

- Python 3.8+
- Git
- Streamlit Cloud account (for deployment)
- Mock dataset (`train_delays.csv`) or real data from Deutsche Bahn APIs

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/transport-tracker.git
   cd transport-tracker
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Generate mock dataset:
   ```bash
   python generate_data.py
   ```

   The `generate_data.py` script (included) creates `train_delays.csv` with 100 rows of simulated data.

## Usage

1. Run the app locally:
   ```bash
   streamlit run app.py
   ```

2. Open `http://localhost:8501` in your browser.

3. Interact with the app:
   - **Delay Map**: Hover over markers to see station delays.
   - **Delay Distribution**: Use the city filter to explore delays (histogram or box plot, based on A/B group).
   - **Sentiment Word Cloud**: View mock sentiment (real X API integration possible).
   - **Route Reliability**: Check on-time performance by route.
   - **A/B Test Results**: Enable the admin view checkbox to see interaction metrics and t-test results.
   - Click "Log Session" to save interaction data (simulates session end).

4. Deploy to Streamlit Cloud:
   - Push the repository to GitHub.
   - Sign into [Streamlit Community Cloud](https://streamlit.io/cloud).
   - Create a new app, linking your GitHub repo and specifying `app.py`.
   - Ensure `train_delays.csv` and `requirements.txt` are included.

## Project Structure

- `app.py`: Main Streamlit application.
- `generate_data.py`: Script to create mock `train_delays.csv`.
- `requirements.txt`: Lists dependencies.
- `ab_test_results.csv`: Generated during runtime to store A/B test data.

## Limitations and Future Work

- **Mock Data**: Uses simulated train delays and X posts. Integrate real data from Deutsche Bahn Open Data or X API for production.
- **Session Logging**: Button-based logging is a prototype. Use JavaScript or server-side analytics for accurate session tracking.
- **Scalability**: CSV logging is simple but not robust. Consider a database (e.g., SQLite, Firebase) for large-scale testing.
- **Enhancements**: Add date filters, predictive models (e.g., delay forecasting), or test additional UI elements (e.g., map styles).

## Screenshot

*Add a screenshot of the app here (e.g., `screenshot.png`)*

## Dependencies

- Streamlit
- Pandas
- Plotly
- Folium
- Streamlit-Folium
- WordCloud
- NumPy
- SciPy

See `requirements.txt` for full details.

## License

MIT License

---
Built with ❤️ by [Your Name]. Contributions welcome!