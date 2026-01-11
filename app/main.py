from flask import Flask, render_template, g
from controllers.send_message import send_message_bp
from controllers.retrieve_message import retrieve_message_bp
import sqlite3

DATABASE = "./databases/database.db"
app = Flask(__name__, static_folder='static/', template_folder='templates/')

app.register_blueprint(send_message_bp)
app.register_blueprint(retrieve_message_bp)

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db
@app.route('/')
def main():
    db = get_db()
    users = db.execute("SELECT id, name FROM users").fetchall()

    return render_template('encrypt_decrypt_message.html', users=users)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)