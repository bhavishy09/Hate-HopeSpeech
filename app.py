import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, request
from database import (
    init_db, create_user, verify_user, get_user_by_id,
    add_prediction, get_user_predictions, get_sentiment_stats
)
from services import gemini_chat


app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')

os.makedirs('instance', exist_ok=True)
init_db()

def predict_sentiment(video_id):
    sentiments = ['Positive', 'Neutral', 'Negative']
    return random.choice(sentiments)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = verify_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {user["username"]}!', 'success')
            return redirect(url_for('predict'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if not username or not email or not password:
            flash('Please fill in all fields', 'error')
            return render_template('signup.html')
        
        if '@' not in email or '.' not in email:
            flash('Please enter a valid email address', 'error')
            return render_template('signup.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long', 'error')
            return render_template('signup.html')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('signup.html')
        
        user_id = create_user(username, email, password)
        if user_id:
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Username or email already exists', 'error')
    
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        flash('Please log in to make predictions', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        video_id = request.form.get('video_id', '').strip()
        
        if not video_id:
            flash('Please enter a YouTube video ID', 'error')
            return render_template('predict.html')
        
        if len(video_id) < 5:
            flash('Please enter a valid YouTube video ID', 'error')
            return render_template('predict.html')
        
        sentiment = predict_sentiment(video_id)
        add_prediction(session['user_id'], video_id, sentiment)
        
        flash(f'Prediction completed! Sentiment: {sentiment}', 'success')
        
        recent_predictions = get_user_predictions(session['user_id'], limit=5)
        return render_template('predict.html', 
                             latest_prediction={'video_id': video_id, 'sentiment': sentiment},
                             recent_predictions=recent_predictions)
    
    recent_predictions = get_user_predictions(session['user_id'], limit=5)
    return render_template('predict.html', recent_predictions=recent_predictions)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to view your dashboard', 'error')
        return redirect(url_for('login'))
    
    predictions = get_user_predictions(session['user_id'])
    stats = get_sentiment_stats(session['user_id'])
    
    sentiment_data = {
        'Positive': stats.get('Positive', 0),
        'Neutral': stats.get('Neutral', 0),
        'Negative': stats.get('Negative', 0)
    }
    
    return render_template('dashboard.html', 
                         predictions=predictions, 
                         sentiment_data=sentiment_data)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('home'))


# chat enpoint
@app.route("/chat/<prompt>", methods=["POST"])
def chating(prompt):
    
    try:
        response = gemini_chat.chatbot(prompt)
        return jsonify({
            "status": "ok",
            "message": response
        })
    
    except Exception as err:
        return jsonify({
            "message": None,
            "error": str(err) 
        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
