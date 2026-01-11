from flask import *
from models.encryption import Encryption

send_message_bp = Blueprint('send_message', __name__)

@send_message_bp.route('/api/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data not found"}), 404

    required_fields = ['user_id', 'message', 'receiver_id']
    for field in required_fields:
        if data.get(field) is None:
            return jsonify({'status': 'error', 'message': f'Missing {field}'}), 400

    user_id = data['user_id']
    receiver_id = data['receiver_id']
    message = data['message']

    if user_id == receiver_id:
        return jsonify({'status': 'error', 'message': f'the sender is the same as the receiver. please select different receiver.'}), 400

    encryption = Encryption()
    result = encryption.encrypt(user_id,message,receiver_id)

    if result:
        return jsonify({"success": True, "messages": result}), 200
    else:
        return jsonify({"success": False}), 400
