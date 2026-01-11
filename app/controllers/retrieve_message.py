from flask import *
from models.encryption import Encryption

retrieve_message_bp = Blueprint('retrieve_message', __name__)

@retrieve_message_bp.route('/api/retrieve_message', methods=['GET', 'POST'])
def retrieve_message():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Data not found"}), 404

    if data.get('receiver_id') is None:
        return jsonify({'status': 'error', 'message': f'Missing {field}'}), 400
    receiver_id = data['receiver_id']

    encryption = Encryption()

    result = encryption.decrypt(receiver_id)
    if result:
        return jsonify({"success": True, "messages": result}), 200
    else:
        return jsonify({"success": False}), 400
