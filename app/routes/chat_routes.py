from flask import Blueprint, jsonify, request, render_template
from app.services.assistant_service import AssistantService
from app.services.thread_service import ThreadService

chat_bp = Blueprint('chat', __name__)
assistant_service = AssistantService()
thread_service = ThreadService()

@chat_bp.route('/')
def chat_widget():
    return render_template('bot_widget.html')

@chat_bp.route('/assist', methods=["POST"])
def assist():
    query = request.json.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    try:
        thread_service.add_message(content=query)
        response = thread_service.run_assistant(
            assistant_id=assistant_service.assistant_id
        )
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history', methods=["GET"])
def history():
    try:
        history = thread_service.get_message_history()
        return jsonify({'history': history})
    except Exception as e:
        return jsonify({'error': str(e)}), 500