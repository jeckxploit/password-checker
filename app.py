from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# Load weak passwords
try:
    with open("weak_passwords.txt", "r", encoding="utf-8") as f:
        WEAK_PASSWORDS = set(line.strip() for line in f.readlines())
except FileNotFoundError:
    WEAK_PASSWORDS = set()

def check_password_strength(password: str) -> dict:
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("⚠️ Password kurang dari 8 karakter")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("⚠️ Tidak ada huruf kapital")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("⚠️ Tidak ada huruf kecil")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("⚠️ Tidak ada angka")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("⚠️ Tidak ada simbol")

    if password.lower() in WEAK_PASSWORDS:
        feedback.append("❌ Password terlalu umum! Ganti segera.")
        score = 0

    levels = [
        "Sangat Lemah",
        "Lemah",
        "Sedang",
        "Kuat",
        "Sangat Kuat",
    ]
    level = levels[score] if score < len(levels) else levels[-1]

    return {"score": score, "level": level, "feedback": feedback}

# HTML template
TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Password Checker Modern</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <!-- Font Awesome -->
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>
    <!-- Styling -->
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea, #764ba2);
            display: flex;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
            padding: 1rem;
        }
        .container {
            background: #fff;
            border-radius: 16px;
            padding: 2.5rem;
            max-width: 450px;
            width: 100%;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        h2 {
            text-align: center;
            margin-bottom: 1.5rem;
            color: #333;
        }
        input[type="text"] {
            width: 100%;
            padding: 0.8rem;
            font-size: 1rem;
            border-radius: 8px;
            border: 1px solid #ccc;
            margin-bottom: 1rem;
        }
        button {
            width: 100%;
            padding: 0.8rem;
            font-size: 1rem;
            background: #6c5ce7;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5a4bcf;
        }
        .result {
            margin-top: 1.5rem;
        }
        .strength {
            margin: 0.5rem 0;
            font-weight: 600;
            font-size: 1.1rem;
        }
        .feedback-list {
            list-style: none;
            padding-left: 0;
        }
        .feedback-list li {
            margin: 0.4rem 0;
            display: flex;
            align-items: center;
            color: #555;
        }
        .feedback-list i {
            margin-right: 0.6rem;
        }
        .level-0 { color: #e74c3c; }      /* Sangat Lemah */
        .level-1 { color: #e67e22; }      /* Lemah */
        .level-2 { color: #f1c40f; }      /* Sedang */
        .level-3 { color: #2ecc71; }      /* Kuat */
        .level-4 { color: #3498db; }      /* Sangat Kuat */
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Password Checker</h2>
        <form method="POST">
            <input type="text" name="password" placeholder="Masukkan password" required>
            <button type="submit">Cek Password</button>
        </form>

        {% if result %}
        <div class="result">
            <p class="strength level-{{ result.score }}">
                Level: {{ result.level }} ({{ result.score }}/5)
            </p>
            {% if result.feedback %}
            <ul class="feedback-list">
                {% for fb in result.feedback %}
                <li><i class="fas fa-exclamation-circle text-warning"></i> {{ fb }}</li>
                {% endfor %}
            </ul>
            {% else %}
            <p class="text-success"><i class="fas fa-check-circle"></i> Password sudah sangat baik!</p>
            {% endif %}
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        password = request.form['password']
        result = check_password_strength(password)
    return render_template_string(TEMPLATE, result=result)

if __name__ == '__main__':
    app.run()
