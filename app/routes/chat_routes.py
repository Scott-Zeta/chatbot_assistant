from flask import Blueprint, jsonify, request, render_template
from app.services.chat_service.assistant_service import AssistantService
from app.services.chat_service.thread_service import ThreadService
from app.services.chat_service.run_service import RunService
from app.utils.rate_limiter import rate_limit
from app.utils.validators import MessageSchema, validate_request
from app.utils.timer import timer

chat_bp = Blueprint('chat', __name__)
assistant_service = AssistantService()
thread_service = ThreadService()
run_service = RunService(thread_service)

@chat_bp.route('/')
def chat_widget():
    return render_template('bot_widget.html')

@chat_bp.route('/assist', methods=["POST"])
@timer
@rate_limit(calls=30, period=3600)
@validate_request(MessageSchema())
def assist():
    query = request.json.get('query')    
    try:
        thread_service.add_message(content=query)
        response = run_service.create_run(
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