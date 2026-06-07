from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)
flashcards = []

BASE_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Flashcard App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 760px;
            margin: 0 auto;
            padding: 24px;
            line-height: 1.6;
            background: #f8f9fb;
            color: #1c1f2b;
        }
        h1 {
            margin-top: 0;
            color: #23395d;
        }
        .card {
            background: white;
            border: 1px solid #dde3ef;
            border-radius: 12px;
            box-shadow: 0 4px 16px rgba(15, 32, 80, 0.08);
            padding: 18px;
            margin-bottom: 16px;
        }
        .question {
            font-weight: 700;
            margin-bottom: 10px;
        }
        .answer {
            margin-top: 10px;
            padding: 14px;
            background: #eef4ff;
            border-radius: 8px;
            display: none;
        }
        button,
        input[type="submit"] {
            cursor: pointer;
            border: none;
            border-radius: 8px;
            padding: 10px 16px;
            font-size: 16px;
            color: white;
            background: #3268f4;
            transition: background 0.2s ease;
        }
        button:hover,
        input[type="submit"]:hover {
            background: #244dc4;
        }
        form {
            margin-bottom: 30px;
        }
        label {
            display: block;
            margin-bottom: 6px;
            font-weight: 600;
        }
        input[type="text"],
        textarea {
            width: 100%;
            padding: 12px;
            border: 1px solid #c8d0e7;
            border-radius: 10px;
            margin-bottom: 16px;
            font-size: 15px;
        }
        footer {
            margin-top: 32px;
            color: #5a6374;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <h1>Flashcard App</h1>
    <p>Create flashcards and review them on a clean web page.</p>

    <div class="card">
        <h2>Add a new flashcard</h2>
        <form method="post" action="{{ url_for('add') }}">
            <label for="question">Question</label>
            <textarea id="question" name="question" rows="2" required></textarea>

            <label for="answer">Answer</label>
            <textarea id="answer" name="answer" rows="3" required></textarea>

            <input type="submit" value="Add Flashcard" />
        </form>
    </div>

    <div class="card">
        <h2>Your flashcards</h2>
        {% if flashcards %}
            {% for idx, card in enumerate(flashcards, 1) %}
                <div class="card">
                    <div class="question">{{ idx }}. {{ card.question }}</div>
                    <button type="button" onclick="toggleAnswer('answer-{{ idx }}')">Show / Hide Answer</button>
                    <div id="answer-{{ idx }}" class="answer">{{ card.answer }}</div>
                </div>
            {% endfor %}
        {% else %}
            <p>No flashcards yet. Add one above to get started.</p>
        {% endif %}
    </div>

    <footer>
        Built with Flask and memory-only storage. Refresh the page to see new cards.
    </footer>

    <script>
        function toggleAnswer(id) {
            const element = document.getElementById(id);
            if (!element) return;
            element.style.display = element.style.display === 'block' ? 'none' : 'block';
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(BASE_HTML, flashcards=flashcards)

@app.route("/add", methods=["POST"])
def add():
    question = request.form.get("question", "").strip()
    answer = request.form.get("answer", "").strip()
    if question and answer:
        flashcards.append({
            "question": question,
            "answer": answer,
        })
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
