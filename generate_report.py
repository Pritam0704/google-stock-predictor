"""Generate project report PDF using ReportLab."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "Google_Stock_Predictor_Report.pdf")

# ── Colours ───────────────────────────────────────────────────────────────────
NAVY   = colors.HexColor("#0D1B2A")
TEAL   = colors.HexColor("#1C7293")
GREEN  = colors.HexColor("#2A9D8F")
RED    = colors.HexColor("#E63946")
LIGHT  = colors.HexColor("#F5F7FA")
DARK   = colors.HexColor("#1E293B")
GRAY   = colors.HexColor("#64748B")
AMBER  = colors.HexColor("#F59E0B")
WHITE  = colors.white
BLACK  = colors.black

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

# Base styles
title_style = S("DocTitle",
    fontSize=26, fontName="Helvetica-Bold",
    textColor=WHITE, alignment=TA_CENTER,
    spaceAfter=6)

subtitle_style = S("DocSubtitle",
    fontSize=13, fontName="Helvetica",
    textColor=colors.HexColor("#94A3B8"), alignment=TA_CENTER,
    spaceAfter=4)

h1 = S("H1",
    fontSize=16, fontName="Helvetica-Bold",
    textColor=NAVY, spaceBefore=18, spaceAfter=8,
    borderPadding=(0, 0, 4, 0))

h2 = S("H2",
    fontSize=12, fontName="Helvetica-Bold",
    textColor=TEAL, spaceBefore=12, spaceAfter=6)

h3 = S("H3",
    fontSize=10, fontName="Helvetica-Bold",
    textColor=DARK, spaceBefore=8, spaceAfter=4)

body = S("Body",
    fontSize=10, fontName="Helvetica",
    textColor=DARK, leading=16, spaceAfter=6,
    alignment=TA_JUSTIFY)

bullet = S("Bullet",
    fontSize=10, fontName="Helvetica",
    textColor=DARK, leading=15, spaceAfter=3,
    leftIndent=16, bulletIndent=4)

code_style = S("Code",
    fontSize=8.5, fontName="Courier",
    textColor=colors.HexColor("#1e293b"),
    backColor=colors.HexColor("#f1f5f9"),
    leading=13, spaceAfter=4,
    leftIndent=12, rightIndent=12,
    borderPadding=6)

highlight = S("Highlight",
    fontSize=10, fontName="Helvetica-Bold",
    textColor=TEAL, leading=15, spaceAfter=4)

note = S("Note",
    fontSize=9, fontName="Helvetica-Oblique",
    textColor=GRAY, leading=14, spaceAfter=6,
    leftIndent=12)

caption = S("Caption",
    fontSize=9, fontName="Helvetica",
    textColor=GRAY, leading=13, spaceAfter=8,
    alignment=TA_CENTER)


def hr():
    return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"),
                      spaceAfter=8, spaceBefore=4)

def section_rule():
    return HRFlowable(width="100%", thickness=2.5, color=TEAL,
                      spaceAfter=10, spaceBefore=2)

def P(text, style=None):
    return Paragraph(text, style or body)

def B(text):
    return Paragraph(f"• &nbsp; {text}", bullet)

def Code(text):
    return Paragraph(text.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style)

def info_table(rows, col_widths=None):
    """Create a styled 2-column key-value table."""
    data = [[P(f"<b>{k}</b>", h3), P(v, body)] for k, v in rows]
    t = Table(data, colWidths=col_widths or [5*cm, 11*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LIGHT),
        ('TEXTCOLOR',  (0,0), (0,-1), TEAL),
        ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING',    (0,0), (-1,-1), 6),
        ('FONTNAME',   (0,0), (0,-1), 'Helvetica-Bold'),
    ]))
    return t

def metric_table(headers, rows):
    data = [headers] + rows
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,0), NAVY),
        ('TEXTCOLOR',   (0,0), (-1,0), WHITE),
        ('FONTNAME',    (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0), (-1,-1), 9),
        ('ALIGN',       (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F0F9FF")]),
        ('GRID',        (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E1")),
        ('PADDING',     (0,0), (-1,-1), 7),
    ]))
    return t

# ── Cover page builder ────────────────────────────────────────────────────────
def cover_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Background
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, w, h, fill=1, stroke=0)
    # Teal accent bar
    canvas.setFillColor(TEAL)
    canvas.rect(0, h - 8, w, 8, fill=1, stroke=0)
    canvas.rect(0, 0, w, 5, fill=1, stroke=0)
    # Side accent
    canvas.setFillColor(colors.HexColor("#1C7293"))
    canvas.rect(0, 0, 6, h, fill=1, stroke=0)
    canvas.restoreState()

def later_page(canvas, doc):
    canvas.saveState()
    w, h = A4
    # Header line
    canvas.setStrokeColor(TEAL)
    canvas.setLineWidth(1.5)
    canvas.line(2*cm, h - 1.5*cm, w - 2*cm, h - 1.5*cm)
    # Footer
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(2*cm, 1.2*cm, "Google Stock Price Predictor — Data Mining Project 2026")
    canvas.drawRightString(w - 2*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

# ── Document ──────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2.5*cm,
    title="Google Stock Price Predictor — Project Report",
    author="Data Mining Project 2026",
)

story = []

# ═══════════════════════════════════════════════════════════════════
# COVER
# ═══════════════════════════════════════════════════════════════════
story.append(Spacer(1, 3*cm))
story.append(P("Google Stock Price Predictor", title_style))
story.append(Spacer(1, 0.3*cm))
story.append(P("Complete Project Explanation", subtitle_style))
story.append(Spacer(1, 0.2*cm))
story.append(P("Data Mining Project 2026", subtitle_style))
story.append(Spacer(1, 2*cm))

cover_tbl = Table([
    [P("<b>Model</b>",    h2), P("Linear Regression + Technical Indicators", body)],
    [P("<b>Dataset</b>",  h2), P("Google Stock Price (GOOGL) · Jan 2012 – Dec 2016", body)],
    [P("<b>Records</b>",  h2), P("1,258 trading days", body)],
    [P("<b>Test R²</b>",  h2), P("0.9349  (93.49% variance explained)", body)],
    [P("<b>RMSE</b>",     h2), P("$8.31 per prediction", body)],
], colWidths=[4.5*cm, 11*cm])
cover_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#112233")),
    ('BACKGROUND', (1,0), (1,-1), colors.HexColor("#0f1e2e")),
    ('TEXTCOLOR',  (0,0), (0,-1), TEAL),
    ('TEXTCOLOR',  (1,0), (1,-1), WHITE),
    ('GRID',       (0,0), (-1,-1), 0.5, colors.HexColor("#1C3A5A")),
    ('PADDING',    (0,0), (-1,-1), 10),
    ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(cover_tbl)
story.append(Spacer(1, 2*cm))
story.append(P("This document explains every part of the project — from the notebook code to<br/>how predictions are made — in simple, easy-to-understand language.", caption))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 1 — Notebook Walkthrough
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 1: How the Notebook Works", h1))
story.append(section_rule())
story.append(P(
    "The notebook <b>google_stock_analysis.ipynb</b> is where all the data analysis and model "
    "training happens. Think of it as the 'research lab' of the project. It answers 5 research "
    "questions step by step and ultimately builds the model saved in <b>model.pkl</b>.", body))

story.append(P("Cell 1 — Importing Libraries", h2))
story.append(P(
    "The first code cell loads all the tools needed for the project:", body))
story.append(B("<b>pandas</b> — works like Excel; reads CSV files and organises data into tables"))
story.append(B("<b>numpy</b> — handles mathematical calculations, especially with arrays of numbers"))
story.append(B("<b>matplotlib / seaborn</b> — draws charts and graphs"))
story.append(B("<b>scikit-learn</b> — contains the machine learning algorithms (LinearRegression, SVR, RandomForest) and tools for measuring how good the model is"))
story.append(Spacer(1, 0.2*cm))
story.append(Code(
    "import pandas as pd\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "from sklearn.linear_model import LinearRegression\n"
    "from sklearn.metrics import mean_squared_error, r2_score"
))

story.append(P("Cell 2 — Loading and Cleaning the Data", h2))
story.append(P(
    "This cell reads the CSV file that contains Google's daily stock prices from 2012 to 2016. "
    "It then cleans the data:", body))
story.append(B("Removes commas from numbers like '7,380,500' so Python can treat them as real numbers"))
story.append(B("Converts the Date column from plain text into actual dates Python understands"))
story.append(B("Sorts rows from oldest to newest"))
story.append(B("Splits the data — 80% for training (1,006 rows) and 20% for testing (252 rows)"))
story.append(Spacer(1, 0.2*cm))
story.append(Code(
    "df = pd.read_csv('GoogleStockPrice_Train.csv')\n"
    "for col in ['Open','High','Low','Close','Volume']:\n"
    "    df[col] = df[col].astype(str).str.replace(',','').astype(float)\n"
    "df['Date'] = pd.to_datetime(df['Date'])\n"
    "df = df.sort_values('Date').reset_index(drop=True)\n"
    "split_idx = int(len(df) * 0.8)   # 80/20 split\n"
    "df_train = df.iloc[:split_idx]    # first 1,006 rows\n"
    "df_test  = df.iloc[split_idx:]    # last 252 rows"
))

story.append(P("Cell 3 — Exploratory Data Analysis (EDA)", h2))
story.append(P(
    "Before building the model, the notebook draws charts to understand the data:", body))
story.append(B("Closing price over time — shows how Google's stock grew from ~$660 to ~$800 (with the notable 2014 data artefact from the stock split)"))
story.append(B("Trading volume bar chart — shows how many shares were traded each day"))
story.append(B("Daily returns histogram — shows the distribution of day-to-day percentage changes, which follows a roughly bell-shaped (normal) curve"))

story.append(P("Research Question 1 — Does Volume Affect Price Change?", h2))
story.append(P(
    "The notebook checks whether days with heavy trading cause bigger price moves. "
    "It uses <b>Pearson Correlation</b> — a number between -1 and +1:", body))
story.append(B("r = 0.0569 (volume vs direction of change) → almost no relationship"))
story.append(B("r = 0.2348 (volume vs magnitude of change) → moderate link"))
story.append(P(
    "<b>Conclusion:</b> High volume does NOT reliably predict which direction the price moves, "
    "but it is somewhat linked to how large the move is.", note))

story.append(P("Research Question 2 — Can We Predict Tomorrow's Closing Price? (Baseline)", h2))
story.append(P(
    "Two models are tested using only the 5 basic columns (Open, High, Low, Close, Volume) "
    "as input features:", body))
story.append(metric_table(
    ["Model", "RMSE", "MAE", "R²"],
    [["Linear Regression", "$9.44", "$7.10", "0.9249"],
     ["SVR (Support Vector)", "$11.92", "$8.90", "0.8803"]]))
story.append(Spacer(1, 0.3*cm))
story.append(P(
    "<b>Finding:</b> Even without technical indicators, Linear Regression already explains "
    "92.49% of the price variation. SVR is less accurate at this baseline.", note))

story.append(P("Research Question 3 — Do Technical Indicators Help?", h2))
story.append(P(
    "The notebook adds 8 more computed features: SMA-20, SMA-50, EMA-20, Bollinger Band Upper, "
    "Bollinger Band Lower, RSI-14, MACD, and MACD Signal. Both models are retrained:", body))
story.append(metric_table(
    ["Model", "Before (RMSE / R²)", "After (RMSE / R²)", "Change"],
    [["Linear Regression", "$9.44 / 0.9249", "$8.31 / 0.9349", "✅ Improved"],
     ["SVR",               "$11.92 / 0.8803", "Worse",          "❌ Degraded"]]))
story.append(Spacer(1, 0.3*cm))
story.append(P(
    "<b>Finding:</b> Indicators make Linear Regression more accurate. SVR gets worse because "
    "it cannot handle the extra correlated features well without retuning.", note))

story.append(P("Research Question 4 — Does Volatility Affect Accuracy?", h2))
story.append(P(
    "Volatility is measured as the rolling 20-day standard deviation of daily returns. "
    "Days are grouped into Low, Medium, and High volatility regimes:", body))
story.append(metric_table(
    ["Regime", "LR RMSE", "SVR RMSE"],
    [["Low",    "~$5–6",  "~$12+"],
     ["Medium", "~$7–8",  "~$15"],
     ["High",   "~$12+",  "~$25+"]]))
story.append(Spacer(1, 0.3*cm))
story.append(P(
    "<b>Finding:</b> The model is most accurate on calm days and least accurate on turbulent days. "
    "This makes intuitive sense — on volatile days the market is unpredictable.", note))

story.append(P("Research Question 5 — Which Model Wins?", h2))
story.append(P(
    "All three models (Linear Regression, SVR, Random Forest) are evaluated on the test set "
    "and cross-validated with 5-fold TimeSeriesSplit:", body))
story.append(metric_table(
    ["Model", "Test R²", "Test RMSE", "CV RMSE Mean", "Winner?"],
    [["Linear Regression", "0.9349", "$8.31",  "~$30",  "🏆 Yes"],
     ["Random Forest",     "~0.90",  "~$10",   "~$40",  "No"],
     ["SVR",               "~0.88",  "~$12+",  "~$45+", "No"]]))
story.append(Spacer(1, 0.3*cm))
story.append(P(
    "<b>Finding:</b> Linear Regression is the best model. Detailed reasoning is in Section 6.", note))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 2 — How app.py Works
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 2: How app.py Works", h1))
story.append(section_rule())
story.append(P(
    "The file <b>app.py</b> is the web application. It loads the trained model and serves "
    "a website where you can enter stock data and get a prediction back. "
    "It is built with <b>Flask</b> — a lightweight Python web framework.", body))

story.append(P("Step 1 — Loading the Model on Startup", h2))
story.append(P(
    "When the app starts, it immediately loads <b>model.pkl</b> — the file that contains "
    "everything saved from the notebook training:", body))
story.append(Code(
    "with open('model.pkl', 'rb') as f:\n"
    "    data = pickle.load(f)\n\n"
    "model        = data['model']        # the trained LinearRegression object\n"
    "scaler       = data['scaler']       # the StandardScaler used during training\n"
    "feat_cols    = data['feat_cols']    # list of the 13 feature names\n"
    "recent_closes = data['recent_closes']  # last 60 closing prices (for indicators)"
))
story.append(P(
    "Think of model.pkl as a 'brain in a box'. The notebook trained the brain, "
    "then packed it into a file. app.py unpacks and uses it.", note))

story.append(P("Step 2 — The Three URL Routes (Endpoints)", h2))
story.append(info_table([
    ("GET /",           "Serves the main webpage (index.html). Passes the last known OHLCV values and chart data so the page loads with useful defaults."),
    ("POST /predict",   "Receives Open, High, Low, Close, Volume from the user → computes indicators → scales the features → runs the model → returns the predicted price as JSON."),
    ("GET /fetch_date", "Receives a date → downloads real OHLCV data from Yahoo Finance via yfinance → multiplies by 20 (split correction) → returns to the browser to auto-fill the form."),
    ("GET /next_close", "Receives a date → downloads the NEXT trading day's actual closing price from Yahoo Finance → multiplies by 20 → returns for comparison against the prediction."),
]))

story.append(P("Step 3 — The Prediction Logic (compute_indicators function)", h2))
story.append(P(
    "This is the most important function. When /predict receives values, "
    "it calls compute_indicators() to calculate all 13 features:", body))
story.append(Code(
    "def compute_indicators(open_, high, low, close, volume, prev_closes):\n"
    "    closes = prev_closes + [close]       # append today to history\n"
    "    closes_s = pd.Series(closes)\n\n"
    "    sma20 = closes_s.rolling(20).mean().iloc[-1]   # avg of last 20 closes\n"
    "    sma50 = closes_s.rolling(50).mean().iloc[-1]   # avg of last 50 closes\n"
    "    ema20 = closes_s.ewm(span=20).mean().iloc[-1]  # exponentially weighted avg\n\n"
    "    bb_upper = sma20 + 2 * closes_s.rolling(20).std().iloc[-1]  # upper band\n"
    "    bb_lower = sma20 - 2 * closes_s.rolling(20).std().iloc[-1]  # lower band\n\n"
    "    rsi = ...  # momentum indicator (see Section 5)\n"
    "    macd = ema12 - ema26  # trend indicator (see Section 5)"
))

story.append(P("Step 4 — Scaling and Predicting", h2))
story.append(P(
    "After computing the 13 features, two more steps happen:", body))
story.append(B("<b>Scaling</b> — The scaler (loaded from model.pkl) normalises the input "
    "values to the same scale used during training. This is critical — if training used "
    "scaled data, prediction must use the same scaling."))
story.append(B("<b>Predicting</b> — model.predict(X_scaled) runs the Linear Regression "
    "equation and returns the predicted next-day closing price in one line."))
story.append(Code(
    "X_raw    = np.array([[feats[c] for c in feat_cols]])\n"
    "X_scaled = scaler.transform(X_raw)   # normalise to training scale\n"
    "pred     = float(model.predict(X_scaled)[0])   # one number: the prediction"
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 3 — Train / Test Split
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 3: How the Data is Split for Training and Testing", h1))
story.append(section_rule())
story.append(P(
    "Before training a model, the dataset is divided into two parts: "
    "a <b>Training Set</b> (what the model learns from) and a "
    "<b>Test Set</b> (used to check if the model actually works on data it has never seen).", body))

story.append(P("The 80/20 Chronological Split", h2))
story.append(P(
    "The dataset has <b>1,258 rows</b> (trading days). The split is done <b>chronologically</b> — "
    "NOT randomly. This is very important for time-series data:", body))
story.append(metric_table(
    ["Set", "Rows", "Date Range", "Purpose"],
    [["Training Set", "1,006 (80%)", "Jan 2012 → ~Apr 2015", "Model learns patterns from this data"],
     ["Test Set",     "252 (20%)",  "~Apr 2015 → Dec 2016",  "Model is evaluated on this unseen data"]]))
story.append(Spacer(1, 0.3*cm))

story.append(P("Why Chronological? Not Random?", h2))
story.append(P(
    "In normal machine learning (like classifying cats vs dogs), you shuffle the data randomly "
    "before splitting. But stock prices are a <b>time series</b> — each day depends on the previous days. "
    "If you split randomly:", body))
story.append(B("The model could 'see the future' during training (e.g., train on 2016 data, test on 2014 data)"))
story.append(B("This would make accuracy look artificially high — the model would be cheating"))
story.append(B("Chronological split ensures the model only ever learns from the past and predicts the future"))

story.append(P("What 'Training' Actually Means", h2))
story.append(P(
    "During training, the model sees pairs of inputs and outputs:", body))
story.append(B("<b>Input (features X):</b> 13 values for a given day — Open, High, Low, Close, Volume + 8 technical indicators"))
story.append(B("<b>Output (target y):</b> The closing price of the NEXT day"))
story.append(P(
    "The model finds the mathematical relationship: "
    "<i>'If today looks like X, tomorrow's close will be approximately Y.'</i> "
    "It does this for all 1,006 training days, adjusting itself until it fits the pattern.", body))

story.append(P("TimeSeriesSplit Cross-Validation", h2))
story.append(P(
    "The notebook also uses <b>5-fold TimeSeriesSplit</b> — a more rigorous check. "
    "It trains and tests 5 times on different rolling windows of the data, "
    "always ensuring the test period is always after the training period. "
    "This gives a more realistic measure of how well the model generalises.", body))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 4 — How Next Day's Price is Predicted
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 4: How the Next Day's Closing Price is Predicted", h1))
story.append(section_rule())
story.append(P(
    "The core idea: <b>today's stock data reliably tells us approximately what tomorrow's "
    "closing price will be.</b> Here is the exact step-by-step process:", body))

story.append(P("Step 1 — You Provide Today's Data", h2))
story.append(P(
    "You enter (or auto-fill from Yahoo Finance) five values for a chosen trading day:", body))
story.append(metric_table(
    ["Value", "What It Means", "Example"],
    [["Open",   "Price when the market opened that morning",         "$782.75"],
     ["High",   "Highest price reached during the day",             "$782.78"],
     ["Low",    "Lowest price reached during the day",              "$770.41"],
     ["Close",  "Price when the market closed that afternoon",      "$771.82"],
     ["Volume", "Number of shares traded that day",                 "1,770,000"]]))
story.append(Spacer(1, 0.3*cm))

story.append(P("Step 2 — 8 Technical Indicators are Computed Automatically", h2))
story.append(P(
    "The app computes 8 additional values from Close's price history (last 60 days). "
    "These capture trends and momentum. (See Section 5 for a full explanation of each.)", body))

story.append(P("Step 3 — Feature Scaling (Normalisation)", h2))
story.append(P(
    "The 13 raw numbers are on very different scales — Volume is in millions while RSI is 0–100. "
    "The <b>StandardScaler</b> converts each number to a z-score:", body))
story.append(Code("z = (value - mean_from_training) / std_from_training"))
story.append(P(
    "This puts all 13 features on the same playing field so that large numbers "
    "(like Volume = 1,770,000) don't overwhelm small numbers (like RSI = 55.3). "
    "The scaler was fitted on the training data and saved — the same transformation "
    "is applied to every new prediction.", body))

story.append(P("Step 4 — The Linear Regression Equation", h2))
story.append(P(
    "Linear Regression learned a formula during training. It looks like this:", body))
story.append(Code(
    "Predicted_Close = w1*Open + w2*High + w3*Low + w4*Close + w5*Volume\n"
    "                + w6*SMA20 + w7*SMA50 + w8*EMA20 + w9*BB_upper\n"
    "                + w10*BB_lower + w11*RSI + w12*MACD + w13*MACD_sig\n"
    "                + bias"
))
story.append(P(
    "Where <b>w1 through w13</b> are weights (numbers) that the model learned during training. "
    "Each weight tells the model how much that feature matters. "
    "The model simply multiplies each scaled input by its weight, adds them all up, "
    "and that sum is the predicted next-day closing price.", body))

story.append(P("Step 5 — Comparing to the Real Price", h2))
story.append(P(
    "After the prediction is made, the app fetches the actual closing price for the next "
    "trading day from Yahoo Finance (×20 scaled) and shows a side-by-side comparison — "
    "predicted vs actual — along with the error percentage.", body))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 5 — Technical Indicators
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 5: Technical Indicators — What They Are and Why They Help", h1))
story.append(section_rule())
story.append(P(
    "Technical indicators are mathematical calculations based on past prices. "
    "They summarise information about trend, momentum, and volatility that is "
    "not visible from a single day's OHLCV data alone.", body))

story.append(P("1. SMA-20 and SMA-50 — Simple Moving Average", h2))
story.append(P(
    "A Simple Moving Average smooths out day-to-day noise by averaging the last N closing prices:", body))
story.append(Code("SMA_20 = average of last 20 closing prices\nSMA_50 = average of last 50 closing prices"))
story.append(B("<b>Why it helps:</b> If today's close is above its SMA-20, the stock is in a short-term uptrend. If SMA-20 is above SMA-50, momentum is positive. These trends help the model distinguish rising days from falling days."))
story.append(B("<b>Example:</b> Close = $780, SMA-20 = $760 → stock is trading above its 20-day average → upward momentum signal."))

story.append(P("2. EMA-20 — Exponential Moving Average", h2))
story.append(P(
    "Like SMA but gives more weight to recent prices. Yesterday's price matters more than "
    "last month's price:", body))
story.append(Code("EMA_today = α × Close_today + (1 - α) × EMA_yesterday   where α = 2/(20+1)"))
story.append(B("<b>Why it helps:</b> Reacts faster to price changes than SMA. The model gets a more up-to-date picture of the trend."))

story.append(P("3. Bollinger Bands (BB_upper and BB_lower)", h2))
story.append(P(
    "Bollinger Bands create a channel around the price — two standard deviations above and below the SMA-20:", body))
story.append(Code(
    "BB_upper = SMA_20 + 2 × standard_deviation(last 20 closes)\n"
    "BB_lower = SMA_20 - 2 × standard_deviation(last 20 closes)"
))
story.append(B("<b>Why it helps:</b> When the close is near BB_upper, the stock may be overbought (likely to fall). Near BB_lower, it may be oversold (likely to rise). The model uses these as upper and lower 'guardrails' for the prediction."))
story.append(B("<b>Why 2 standard deviations?</b> Statistically, ~95% of prices fall within 2 standard deviations of the mean. Prices outside the bands are statistically unusual."))

story.append(P("4. RSI-14 — Relative Strength Index", h2))
story.append(P(
    "RSI is a momentum oscillator that measures the speed and size of recent price movements. "
    "It produces a number from 0 to 100:", body))
story.append(Code(
    "gain = average gain over last 14 days\n"
    "loss = average loss over last 14 days\n"
    "RS   = gain / loss\n"
    "RSI  = 100 - (100 / (1 + RS))"
))
story.append(metric_table(
    ["RSI Value", "Meaning", "Implication"],
    [["Above 70", "Overbought", "Stock has risen too fast — possible reversal downward"],
     ["30 to 70",  "Neutral",   "Normal territory — trend likely continues"],
     ["Below 30",  "Oversold",  "Stock has fallen too fast — possible reversal upward"]]))
story.append(Spacer(1, 0.3*cm))
story.append(B("<b>Why it helps:</b> RSI tells the model whether the recent trend has gone too far in one direction, helping it anticipate potential turning points."))

story.append(P("5. MACD and MACD Signal", h2))
story.append(P(
    "MACD (Moving Average Convergence Divergence) measures the difference between two EMAs:", body))
story.append(Code(
    "MACD        = EMA(12 days) - EMA(26 days)\n"
    "MACD_signal = EMA(9 days) of MACD   ← smoothed version of MACD"
))
story.append(B("<b>Why it helps:</b> When MACD crosses above its signal line, it's a bullish signal (price likely rising). When it crosses below, bearish. The model treats these as trend confirmation features."))
story.append(B("<b>Improvement from adding indicators:</b> RMSE improved from $9.44 → $8.31 and R² from 0.9249 → 0.9349. All 8 indicators together gave the model a richer understanding of the market state."))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 6 — Why Linear Regression is Best
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 6: Why Linear Regression is the Best Model Here", h1))
story.append(section_rule())
story.append(P(
    "Three models were compared: <b>Linear Regression</b>, <b>SVR</b>, and <b>Random Forest</b>. "
    "Linear Regression won. Here is why, explained simply.", body))

story.append(P("The Core Reason — Stock Prices Have Strong Linear Autocorrelation", h2))
story.append(P(
    "Autocorrelation means: today's value is highly related to yesterday's value. "
    "For stock prices, this is very strong. If Google closed at $780 today, "
    "it will almost certainly close somewhere near $780 tomorrow — not $400 and not $1,200. "
    "This relationship is <b>linear</b> — a straight-line pattern — which is exactly what "
    "Linear Regression is designed to capture.", body))

story.append(P("Why SVR Lost", h2))
story.append(B("SVR uses a complex mathematical boundary called a 'kernel function' to make predictions."))
story.append(B("This complexity is helpful for non-linear problems, but it's overkill for stock prices."))
story.append(B("When the 8 technical indicators were added, SVR got confused by the highly correlated features (SMA-20, SMA-50, and EMA-20 all measure similar things) and its performance degraded."))
story.append(B("SVR also requires careful hyperparameter tuning (C, gamma, epsilon) which was done only with default settings."))

story.append(P("Why Random Forest Lost", h2))
story.append(B("Random Forest builds hundreds of decision trees and combines their answers."))
story.append(B("This makes it very powerful for complex, non-linear problems with large datasets."))
story.append(B("However, our dataset has only ~1,006 training rows. Random Forest tends to overfit small datasets — it memorises the training data instead of learning the general pattern."))
story.append(B("The cross-validation RMSE for Random Forest (~$40) was much higher than the test RMSE (~$10), confirming overfitting."))

story.append(P("Why Linear Regression Won — Summary", h2))
story.append(metric_table(
    ["Reason", "Explanation"],
    [["Linearity of the problem",   "Tomorrow's price ≈ today's price ± small change → linear relationship"],
     ["Small dataset",              "Linear Regression generalises well on 1,006 rows; tree models overfit"],
     ["Correlated features",        "LR handles multicollinearity better than SVR in this configuration"],
     ["Simplicity = reliability",   "The simplest model that fits the data is usually the most trustworthy"],
     ["Speed",                      "Trains and predicts in milliseconds — ideal for a live web app"]]))
story.append(Spacer(1, 0.5*cm))
story.append(P(
    "This is a real-world example of Occam's Razor in machine learning: "
    "<i>'The simplest explanation that fits the data is usually the best one.'</i>", note))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# SECTION 7 — R², RMSE, MAE Explained
# ═══════════════════════════════════════════════════════════════════
story.append(P("Section 7: Understanding R², RMSE, and MAE", h1))
story.append(section_rule())
story.append(P(
    "These three numbers tell us how well the model's predictions match the real prices. "
    "Think of them as the model's 'report card'.", body))

story.append(P("R² — R-Squared (Coefficient of Determination)", h2))
story.append(P(
    "<b>What it is:</b> R² measures how much of the price variation the model can explain. "
    "It ranges from 0 to 1 (or 0% to 100%).", body))
story.append(Code(
    "R² = 1 - (Sum of squared prediction errors)\n"
    "         -----------------------------------\n"
    "         (Sum of squared deviations from mean)"
))
story.append(P("<b>How to read it simply:</b>", h3))
story.append(B("R² = 1.0 (100%) → Perfect predictions. Every prediction exactly matches reality."))
story.append(B("R² = 0.9349 → Our model explains 93.49% of all price variation. Very good."))
story.append(B("R² = 0.5 → Model explains only half the variation. Poor."))
story.append(B("R² = 0.0 → Model is no better than just guessing the average price every time."))
story.append(P(
    "<b>Our model: R² = 0.9349</b><br/>"
    "This means: for every $1 that Google's price moves from the average, "
    "our model correctly captures $0.93 of that movement. Only $0.07 is unexplained.", highlight))

story.append(P("RMSE — Root Mean Squared Error", h2))
story.append(P(
    "<b>What it is:</b> RMSE measures the average size of prediction errors, "
    "in the same units as the price (dollars).", body))
story.append(Code(
    "RMSE = √( average of (predicted - actual)² for all test days )"
))
story.append(P(
    "The squaring step means large errors are punished more heavily than small ones. "
    "Then we take the square root to get back to dollar units.", body))
story.append(P("<b>How to read it simply:</b>", h3))
story.append(B("On average, our predictions are off by $8.31"))
story.append(B("If the actual close is $780, our model predicts somewhere between $771.69 and $788.31 most of the time"))
story.append(B("Compared to a stock price of ~$780, an $8.31 error is about 1.07% — very accurate"))
story.append(P(
    "<b>Our model: RMSE = $8.31</b><br/>"
    "If you bet on our prediction every day, you'd be off by about $8 on average. "
    "That is roughly 1% of the stock price.", highlight))
story.append(P(
    "RMSE penalises big mistakes more than small ones. If the model makes one very wrong "
    "prediction (e.g., $50 off), the RMSE shoots up significantly.", note))

story.append(P("MAE — Mean Absolute Error", h2))
story.append(P(
    "<b>What it is:</b> MAE is the simplest error metric — the average distance between "
    "predicted and actual price, without squaring.", body))
story.append(Code(
    "MAE = average of |predicted - actual| for all test days"
))
story.append(P("<b>How to read it simply:</b>", h3))
story.append(B("MAE = $6.15 means: the typical (median-like) prediction is off by $6.15"))
story.append(B("Unlike RMSE, big errors don't have extra weight — it treats a $50 error as just 50× a $1 error"))
story.append(B("MAE is always ≤ RMSE. If they're close, it means errors are consistent. If RMSE >> MAE, there are occasional large mistakes."))
story.append(P(
    "<b>Our model: MAE = $6.15</b><br/>"
    "The typical prediction error is $6.15. Since RMSE ($8.31) is somewhat higher, "
    "there are occasional larger errors — probably during high-volatility days.", highlight))

story.append(P("Comparing the Three Metrics", h2))
story.append(metric_table(
    ["Metric", "Value", "In Simple Terms", "Good Value?"],
    [["R²",   "0.9349", "Model explains 93.49% of price variation", "✅ Excellent (>0.90)"],
     ["RMSE", "$8.31",  "Average error (big mistakes weighted more)", "✅ Good (~1% of price)"],
     ["MAE",  "$6.15",  "Typical error (all mistakes equal weight)",  "✅ Good (~0.8% of price)"]]))
story.append(Spacer(1, 0.5*cm))

story.append(P("How These Metrics Are Computed in the Notebook", h2))
story.append(Code(
    "from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score\n\n"
    "y_pred = model.predict(X_test_scaled)   # predictions on test set\n\n"
    "r2   = r2_score(y_test, y_pred)                         # R²\n"
    "rmse = np.sqrt(mean_squared_error(y_test, y_pred))      # RMSE\n"
    "mae  = mean_absolute_error(y_test, y_pred)              # MAE\n\n"
    "print(f'R²: {r2:.4f}  RMSE: ${rmse:.2f}  MAE: ${mae:.2f}')\n"
    "# Output: R²: 0.9349  RMSE: $8.31  MAE: $6.15"
))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ═══════════════════════════════════════════════════════════════════
story.append(P("Final Summary", h1))
story.append(section_rule())
story.append(P(
    "Here is a one-page summary of everything the project does, end to end:", body))

story.append(metric_table(
    ["#", "What Happens", "Where"],
    [["1",  "Google stock data (2012–2016) loaded and cleaned",                     "Notebook Cell 2"],
     ["2",  "80/20 chronological split: 1,006 train days, 252 test days",           "Notebook Cell 2"],
     ["3",  "8 technical indicators computed (SMA, EMA, BB, RSI, MACD)",            "Notebook Cell 4"],
     ["4",  "Features scaled with StandardScaler",                                  "Notebook Cells 3,5"],
     ["5",  "Linear Regression trained, SVR and RF compared",                       "Notebook Cells 3–6"],
     ["6",  "Best model (LR) achieves R²=0.9349, RMSE=$8.31, MAE=$6.15",           "Notebook Cell 6"],
     ["7",  "Model + scaler saved to model.pkl",                                     "Notebook (final cell)"],
     ["8",  "app.py loads model.pkl and starts a web server on port 5001",          "app.py"],
     ["9",  "User picks a date → Yahoo Finance returns real OHLCV (×20 scaled)",   "app.py /fetch_date"],
     ["10", "App computes 8 indicators from 60-day history → scales → predicts",   "app.py /predict"],
     ["11", "Next-day actual close fetched from Yahoo Finance for comparison",       "app.py /next_close"],
     ["12", "Predicted vs Actual shown side by side with accuracy score",           "index.html"]]))

story.append(Spacer(1, 0.8*cm))
story.append(P(
    "The project demonstrates a complete data mining pipeline: from raw CSV data through "
    "exploratory analysis, feature engineering with technical indicators, model selection, "
    "evaluation, and deployment as an interactive web application.", body))
story.append(Spacer(1, 0.4*cm))
story.append(hr())
story.append(P(
    "Google Stock Price Predictor · Data Mining Project 2026 · For educational purposes only",
    caption))

# ── Build PDF ─────────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=cover_page, onLaterPages=later_page)
print(f"PDF generated: {OUTPUT}")
