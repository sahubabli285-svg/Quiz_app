import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)
DB_NAME = "quiz.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_option TEXT NOT NULL
        )
    """)
    cur.execute("SELECT COUNT(*) FROM questions")
    if cur.fetchone()[0] == 0:
        sample_questions = [
            (
                "Python mein list banane ke liye kaunsa bracket use hota hai?",
                "{ }",
                "[ ]",
                "( )",
                "< >",
                "B",
            ),
            (
                "HTTP mein 'POST' ka main kaam kya hota hai?",
                "Data delete karna",
                "Server ko data bhejna",
                "Sirf image load karna",
                "Browser band karna",
                "B",
            ),
            (
                "SQL mein table ka data nikalne ke liye kaunsi command chalti hai?",
                "SELECT",
                "INSERT",
                "DROP",
                "UPDATE",
                "A",
            ),
            (
                "HTML mein line break ke liye kaunsa tag use hota hai?",
                "<br>",
                "<lb>",
                "<break>",
                "<hr>",
                "A",
            ),
        ]
        cur.executemany("""
            INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_option)
            VALUES (?, ?, ?, ?, ?, ?)
        """, sample_questions)
        conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()
    return render_template("index.html", questions=questions)


@app.route("/submit", methods=["POST"])
def submit():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM questions")
    questions = cur.fetchall()
    conn.close()

    score = 0
    total = len(questions)
    for q in questions:
        user_ans = request.form.get(f"q_{q['id']}")
        if user_ans == q["correct_option"]:
            score += 1

    return render_template("result.html", score=score, total=total)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
