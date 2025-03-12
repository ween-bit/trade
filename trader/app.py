from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import os
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for session management

# User data storage (for demonstration purposes, use a database in production)
users = {}

# Technical Analysis Functions
def calculate_bollinger_bands(prices, window=20, num_std_dev=2):
    rolling_mean = np.mean(prices[-window:])
    rolling_std = np.std(prices[-window:])
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)
    return upper_band, lower_band

def calculate_macd(prices, short_window=12, long_window=26, signal_window=9):
    short_ema = np.mean(prices[-short_window:])
    long_ema = np.mean(prices[-long_window:])
    macd_line = short_ema - long_ema
    signal_line = np.mean(macd_line[-signal_window:])
    return macd_line, signal_line

def calculate_fibonacci_levels(high, low):
    diff = high - low
    return {
        'level_0': high,
        'level_1': high - 0.236 * diff,
        'level_2': high - 0.382 * diff,
        'level_3': high - 0.5 * diff,
        'level_4': high - 0.618 * diff,
        'level_5': low
    }

def calculate_rsi(prices, period=14):
    gains = []
    losses = []
    for i in range(1, len(prices)):
        change = prices[i] - prices[i - 1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = np.mean(gains[-period:])
    avg_loss = np.mean(losses[-period:])
    rs = avg_gain / avg_loss if avg_loss != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Routes
@app.route('/')
def home():
    return render_template('bot.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users[username] = password  # Store user data (use a database in production)
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/realtime_chart', methods=['GET'])

def analyze_chart():
    if 'chart-upload' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['chart-upload']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Here you would add the logic to analyze the image using Bollinger Bands, MACD, Fibonacci, and RSI strategies
    # For now, we will return a placeholder response
    analysis_result = {
        'action': 'Buy',  # Placeholder action
        'message': 'Based on the analysis, it is recommended to buy.'
    }

    return render_template('realtime_chart.html')


if __name__ == '__main__':
    app.run(debug=True)
