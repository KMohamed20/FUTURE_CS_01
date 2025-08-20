# sample_app/app.py
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Simple login form with XSS and SQLi vulnerabilities
HTML_FORM = '''
<h2>🔐 Login Portal (Vulnerable)</h2>
<form method="POST">
  <input type="text" name="username" placeholder="Username" required><br><br>
  <input type="password" name="password" placeholder="Password" required><br><br>
  <input type="submit" value="Login">
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 💀 SQL Injection Vulnerability
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        print(f"Executing query: {query}")  # Simulate DB execution

        # 💀 Cross-Site Scripting (XSS) Vulnerability
        if "<script>" in username or "<script>" in password:
            return f"<h1 style='color:red;'>XSS Executed! Hello {username}</h1>"

        # 💀 Weak Authentication (Default Credentials)
        if username == "admin" and password == "admin":
            return "<h1>✅ Login Successful (Admin Access)</h1>"
        else:
            return "<h1>❌ Login Failed</h1>"

    return HTML_FORM

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
