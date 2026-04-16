# Google Stock Price Predictor

A data mining project that predicts Google (GOOGL) next-day closing prices using Linear Regression with technical indicators, served via a Flask web app.

## Live Demo

**[https://google-stock-predictor.onrender.com](https://google-stock-predictor.onrender.com)**

> **Note:** The app is hosted on Render's free tier. If it hasn't been visited recently, the first load may take ~30 seconds to wake up.

Pick any trading date (2012–2016) → auto-fill real OHLCV data from Yahoo Finance → get a prediction → compare against the actual closing price.

## Features

- **Next-day close prediction** using Linear Regression (R² = 0.9349, RMSE = $8.31)
- **Auto-fill by date** — fetches live OHLCV data from Yahoo Finance for any trading date
- **Side-by-side comparison** — predicted price vs actual closing price with accuracy score
- **TradingView-style chart** with candlestick/line toggle, pan/scroll/zoom, and 1M/3M/6M/1Y/All duration controls
- **Prediction history table** — stores up to 15 predictions with average accuracy and reset button
- **Technical indicators** — SMA-20/50, EMA-20, Bollinger Bands, RSI-14, MACD

## Tech Stack

| Layer | Technology |
|-------|-----------|
| ML Model | scikit-learn Linear Regression |
| Backend | Python / Flask |
| Data | Yahoo Finance via `yfinance` |
| Frontend | Vanilla JS + TradingView Lightweight Charts |
| Hosting | Render (free tier) |

## Dataset

- **Source:** Google Stock Price (2012–2016), 1,258 trading days
- **Features (13):** Open, High, Low, Close, Volume, SMA-20, SMA-50, EMA-20, Bollinger Bands (upper/lower), RSI-14, MACD, MACD Signal
- **Train / Test split:** 1,006 / 252 days

> **Data Quality Note:** The training CSV has a known inconsistency for pre-April 2014 rows — Open/High/Low values were sourced split-adjusted (post Google's 2-for-1 split in April 2014) while Close values were not. This is corrected in `app.py` by multiplying pre-2014 Open/High/Low by 2. Yahoo Finance prices are additionally scaled ×20 to account for Google's 20-for-1 split in July 2022.

## Model Performance

| Metric | Score |
|--------|-------|
| Test R² | 0.9349 |
| Test RMSE | $8.31 |
| Test MAE | $6.15 |
| Train days | 1,006 |
| Test days | 252 |

## Getting Started (Run Locally)

### Prerequisites

- Python 3.8+

### Installation

```bash
git clone https://github.com/Pritam0704/google-stock-predictor.git
cd google-stock-predictor
pip install -r stock_predictor_app/requirements.txt
```

### Run

```bash
python stock_predictor_app/app.py
```

Open [http://localhost:5001](http://localhost:5001) in your browser.

> **Note:** Port 5000 is reserved by macOS AirPlay Receiver, so the app runs on port 5001 locally.

## Deployment (Render)

This app is deployed on [Render](https://render.com). To deploy your own instance:

1. Fork this repository
2. Sign up at [render.com](https://render.com) with your GitHub account
3. Click **New +** → **Web Service** → connect your forked repo
4. Use these settings:

| Field | Value |
|-------|-------|
| Runtime | Python 3 |
| Build Command | `pip install -r stock_predictor_app/requirements.txt` |
| Start Command | `gunicorn --chdir stock_predictor_app app:app` |
| Instance Type | Free |

5. Click **Create Web Service** — Render will build and deploy automatically.

## Usage

1. **Pick a trading date** (2012–2016) from the date picker — OHLCV data auto-fills from Yahoo Finance
2. The prediction runs automatically — no button click needed
3. View the side-by-side comparison of predicted vs actual closing price with accuracy score
4. Use the duration buttons (1M, 3M, 6M, 1Y, All) to explore the historical chart
5. Switch between candlestick and line chart views
6. Track multiple predictions in the history table

## Project Structure

```
.
├── README.md
├── Procfile                              # Render deployment config
├── google_stock_analysis.ipynb           # EDA and model training notebook
└── stock_predictor_app/
    ├── app.py                            # Flask application
    ├── model.pkl                         # Pre-trained Linear Regression model
    ├── requirements.txt
    ├── GoogleStockPrice_Train.csv        # Training dataset
    └── templates/
        └── index.html                    # Frontend UI
```

## Disclaimer

This project is for **educational purposes only**. Predictions should not be used for real financial decisions.
