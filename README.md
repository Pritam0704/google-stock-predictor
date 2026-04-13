# Google Stock Price Predictor

A data mining project that predicts Google (GOOGL) next-day closing prices using Linear Regression with technical indicators, served via a Flask web app.

## Live Demo

Pick any trading date → auto-fill real OHLCV data from Yahoo Finance → get a prediction → compare against the actual closing price.

## Features

- **Next-day close prediction** using Linear Regression (R² = 0.9349, RMSE = $8.31)
- **Auto-fill by date** — fetches live OHLCV data from Yahoo Finance for any trading date
- **Side-by-side comparison** — predicted price vs actual closing price with accuracy score
- **TradingView-style chart** with 1M / 3M / 6M / 1Y / All duration controls
- **Technical indicators** — SMA-20/50, EMA-20, Bollinger Bands, RSI-14, MACD

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | scikit-learn Linear Regression |
| Backend | Python / Flask |
| Data | Yahoo Finance via `yfinance` |
| Frontend | Vanilla JS + Chart.js |

## Dataset

- **Source:** Google Stock Price (2012–2016), 1,258 trading days
- **Features (13):** Open, High, Low, Close, Volume, SMA-20, SMA-50, EMA-20, Bollinger Bands (upper/lower), RSI-14, MACD, MACD Signal
- **Train / Test split:** 1,006 / 252 days

> **Data Quality Note:** The training CSV has a known inconsistency for pre-April 2014 rows — Open/High/Low values were sourced split-adjusted (post Google's 2-for-1 split in April 2014) while Close values were not. This is documented as a data quality finding. Yahoo Finance prices are additionally scaled ×20 to account for Google's 20-for-1 split in July 2022.

## Model Performance

| Metric | Score |
|--------|-------|
| Test R² | 0.9349 |
| Test RMSE | $8.31 |
| Test MAE | $6.15 |
| Train days | 1,006 |
| Test days | 252 |

## Getting Started

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/<your-username>/google-stock-predictor.git
cd google-stock-predictor
pip install -r stock_predictor_app/requirements.txt
```

### Run

```bash
python stock_predictor_app/app.py
```

Open [http://localhost:5001](http://localhost:5001) in your browser.

> **Note:** Port 5000 is reserved by macOS AirPlay Receiver, so the app runs on port 5001.

## Usage

1. **Pick a trading date** from the date picker and click **Auto-Fill** to load real OHLCV data
2. Click **Predict Tomorrow's Price**
3. View the side-by-side comparison of predicted vs actual closing price
4. Use the duration buttons (1M, 3M, 6M, 1Y, All) to explore the historical chart

## Project Structure

```
.
├── README.md
├── google_stock_analysis.ipynb       # EDA and model training notebook
└── stock_predictor_app/
    ├── app.py                        # Flask application
    ├── model.pkl                     # Pre-trained Linear Regression model
    ├── requirements.txt
    ├── GoogleStockPrice_Train.csv    # Training dataset
    └── templates/
        └── index.html                # Frontend UI
```

## Disclaimer

This project is for **educational purposes only**. Predictions should not be used for real financial decisions.
