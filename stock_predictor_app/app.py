"""
Google Stock Price Predictor — Flask Web App
Run: python app.py
Open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import pickle
import os
import yfinance as yf
from datetime import datetime, timedelta

app = Flask(__name__)

# ── Load pre-trained model ────────────────────────────────────────────
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")

with open(MODEL_PATH, "rb") as f:
    data = pickle.load(f)

model      = data["model"]
scaler     = data["scaler"]
feat_cols  = data["feat_cols"]
close_min  = data["close_min"]
close_max  = data["close_max"]
recent_dates  = data["recent_dates"]
recent_closes = data["recent_closes"]
last_row   = data["last_row"]

# ── Load full CSV history for chart ──────────────────────────────────
CSV_PATH = os.path.join(os.path.dirname(__file__), "GoogleStockPrice_Train.csv")
_csv = pd.read_csv(CSV_PATH)
for col in ["Open", "High", "Low", "Close"]:
    _csv[col] = pd.to_numeric(_csv[col].astype(str).str.replace(",", ""), errors="coerce")
_csv["Date"] = pd.to_datetime(_csv["Date"])
_csv = _csv.dropna(subset=["Open", "High", "Low", "Close"]).sort_values("Date")

# Fix pre-April 2014 data: Open/High/Low were sourced split-adjusted
# (÷2) while Close was not — multiply back to match Close scale
_split = pd.Timestamp("2014-04-02")
_mask  = _csv["Date"] < _split
_csv.loc[_mask, ["Open", "High", "Low"]] *= 2

all_dates  = _csv["Date"].dt.strftime("%Y-%m-%d").tolist()
all_closes = _csv["Close"].round(2).tolist()
all_ohlcv  = _csv[["Open", "High", "Low", "Close"]].round(2).values.tolist()


def compute_indicators(open_, high, low, close, volume,
                        prev_closes: list) -> dict:
    """Compute technical indicators given current + recent close prices."""
    closes = prev_closes + [close]
    closes_s = pd.Series(closes)

    sma20  = closes_s.rolling(20).mean().iloc[-1]
    sma50  = closes_s.rolling(50).mean().iloc[-1]
    ema20  = closes_s.ewm(span=20, adjust=False).mean().iloc[-1]

    bb_mid = closes_s.rolling(20).mean().iloc[-1]
    bb_std = closes_s.rolling(20).std().iloc[-1]
    bb_upper = bb_mid + 2 * bb_std
    bb_lower = bb_mid - 2 * bb_std

    delta = closes_s.diff()
    gain  = delta.clip(lower=0).rolling(14).mean().iloc[-1]
    loss  = (-delta.clip(upper=0)).rolling(14).mean().iloc[-1]
    rs    = gain / loss if loss != 0 else 0
    rsi   = 100 - (100 / (1 + rs))

    ema12 = closes_s.ewm(span=12, adjust=False).mean().iloc[-1]
    ema26 = closes_s.ewm(span=26, adjust=False).mean().iloc[-1]
    macd  = ema12 - ema26
    macd_sig = pd.Series([macd]).ewm(span=9, adjust=False).mean().iloc[-1]

    return {
        "Open": open_, "High": high, "Low": low,
        "Close": close, "Volume": volume,
        "SMA_20": sma20, "SMA_50": sma50, "EMA_20": ema20,
        "BB_upper": bb_upper, "BB_lower": bb_lower,
        "RSI": rsi, "MACD": macd, "MACD_signal": macd_sig,
    }


@app.route("/")
def index():
    last = last_row
    return render_template("index.html",
        last_open=round(last["Open"], 2),
        last_high=round(last["High"], 2),
        last_low=round(last["Low"], 2),
        last_close=round(last["Close"], 2),
        last_volume=int(last["Volume"]),
        close_min=close_min,
        close_max=close_max,
        recent_dates=recent_dates,
        recent_closes=recent_closes,
        all_dates=all_dates,
        all_closes=all_closes,
        all_ohlcv=all_ohlcv,
    )


@app.route("/predict", methods=["POST"])
def predict():
    try:
        body = request.get_json()
        open_  = float(body["open"])
        high   = float(body["high"])
        low    = float(body["low"])
        close  = float(body["close"])
        volume = float(body["volume"])

        # Use the historical closes from training data as context
        prev_closes = recent_closes.copy()

        feats = compute_indicators(open_, high, low, close, volume, prev_closes)
        X_raw = np.array([[feats[c] for c in feat_cols]])

        # Check for NaN (not enough history)
        if np.any(np.isnan(X_raw)):
            return jsonify({"error": "Not enough history to compute all indicators. Try values close to recent prices."}), 400

        X_scaled = scaler.transform(X_raw)
        pred = float(model.predict(X_scaled)[0])

        change     = pred - close
        change_pct = (change / close) * 100

        return jsonify({
            "predicted_close": round(pred, 2),
            "current_close":   round(close, 2),
            "change":          round(change, 2),
            "change_pct":      round(change_pct, 2),
            "indicators": {
                "SMA_20":  round(feats["SMA_20"], 2),
                "RSI":     round(feats["RSI"], 2),
                "MACD":    round(feats["MACD"], 4),
                "BB_upper":round(feats["BB_upper"], 2),
                "BB_lower":round(feats["BB_lower"], 2),
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/fetch_date")
def fetch_date():
    date_str = request.args.get("date", "")
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        # Fetch a window to ensure we land on a trading day
        start = dt
        end   = dt + timedelta(days=4)
        df = yf.download("GOOGL", start=start.strftime("%Y-%m-%d"),
                         end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
        if df.empty:
            return jsonify({"error": f"No trading data found for {date_str}. It may be a weekend or holiday."}), 404

        # Use the first available row (the requested date or next trading day)
        row = df.iloc[0]
        actual_date = df.index[0].strftime("%Y-%m-%d")
        # Scale factor: Yahoo Finance reflects Google's 20-for-1 split (Jul 2022).
        # Training data uses pre-split prices, so multiply by 20 to match the model's scale.
        SPLIT_FACTOR = 20
        return jsonify({
            "date":   actual_date,
            "open":   round(float(row["Open"])  * SPLIT_FACTOR, 2),
            "high":   round(float(row["High"])  * SPLIT_FACTOR, 2),
            "low":    round(float(row["Low"])   * SPLIT_FACTOR, 2),
            "close":  round(float(row["Close"]) * SPLIT_FACTOR, 2),
            "volume": int(row["Volume"] // SPLIT_FACTOR),
        })
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/next_close")
def next_close():
    """Return the actual closing price for the trading day after the given date."""
    date_str = request.args.get("date", "")
    try:
        dt    = datetime.strptime(date_str, "%Y-%m-%d")
        start = dt + timedelta(days=1)
        end   = dt + timedelta(days=6)   # wide window to skip weekends/holidays
        df = yf.download("GOOGL", start=start.strftime("%Y-%m-%d"),
                         end=end.strftime("%Y-%m-%d"), progress=False, auto_adjust=True)
        if df.empty:
            return jsonify({"error": "No trading data found after this date."}), 404

        row         = df.iloc[0]
        actual_date = df.index[0].strftime("%Y-%m-%d")
        SPLIT_FACTOR = 20
        return jsonify({
            "date":  actual_date,
            "close": round(float(row["Close"]) * SPLIT_FACTOR, 2),
        })
    except ValueError:
        return jsonify({"error": "Invalid date format."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"\n  Google Stock Predictor running at http://localhost:{port}\n")
    app.run(debug=False, host="0.0.0.0", port=port)
