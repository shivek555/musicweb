from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key'  # Replace with a strong, unique secret key

# Load user data from a JSON file
USERS_FILE = 'users.json'

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users_data):
    with open(USERS_FILE, 'w') as file:
        json.dump(users_data, file, indent=2)

# Load users initially
users = load_users()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.get(username)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('music_player'))

    return render_template('index.html', is_login=True)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username not in users:
            hashed_password = generate_password_hash(password, method='sha256')
            users[username] = {'password': hashed_password}
            save_users(users)
            session['username'] = username
            return redirect(url_for('music_player'))

    return render_template('index.html', is_register=True)

@app.route('/music_player')
def music_player():
    # Render the music player template
    return render_template('music_player.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')
if __name__ == '__main__':
    app.run(debug=True)
