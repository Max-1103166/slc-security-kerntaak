from flask import Flask, request, jsonify
import base64
import secrets
app = Flask(__name__)
KEYS = {}

@app.post("/hsm/get_key")
def get_key():
    user_id = int(request.json.get("user_id"))
    receiver_id = int(request.json.get("receiver_id"))
    salt = request.json.get("salt")
    # checkt of de key al bestaat, zo niet maakt hij deze key aan
    if (user_id , receiver_id, salt) not in KEYS:
        KEYS[user_id , receiver_id, salt] = base64.urlsafe_b64encode(secrets.token_bytes(16)).decode()
    return jsonify({"key": KEYS[user_id , receiver_id, salt]})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
