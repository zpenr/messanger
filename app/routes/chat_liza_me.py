from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from ..extensions import db
from flask_login import current_user
liza_me = Blueprint('liza/liza_me', __name__)

@liza_me.route('/liza/chat_liza_me', methods=['POST', 'GET'])
def chat_liza_me():
    return handle_liza_me_chat()

@liza_me.route('/me/chat_liza_me', methods=['POST', 'GET'])
def chat_me_liza_me():
    return handle_liza_me_chat()

def handle_liza_me_chat():
    if current_user.is_authenticated:
        if current_user.name in ['me', 'liza']:
            try:
                if request.method == "POST":
                    mess = request.form.get('mess', '')
                    if len(mess) > 0:
                        # Determine author based on current user
                        author = 'liza' if current_user.name == 'liza' else 'me'
                        message = Massage(massage=mess, author_of_massage=author)
                        
                        db.session.add(message)
                        db.session.commit()
                        print(f"Liza-Me message saved: {mess} by {author}")
                        
                        # Redirect to appropriate URL based on current user
                        redirect_url = '/liza/chat_liza_me' if current_user.name == 'liza' else '/me/chat_liza_me'
                        return redirect(redirect_url)
                    else:
                        print("Empty Liza-Me message received")
                
                # GET request or POST with empty message
                messages = Massage.query.all()
                
                # Safe handling of empty message lists
                last_message = messages[-1].massage if messages else "Нет сообщений"
                
                print(f"Loading Liza-Me chat: {len(messages)} messages")
                
                try:
                    return render_template('chats/lizame.html', 
                                         messages=messages, 
                                         last_message=last_message)
                except Exception as e:
                    print(f"Template error: {e}")
                    # Fallback HTML
                    return f"""
                    <html>
                    <head><title>Chat Liza-Me</title></head>
                    <body>
                        <h1>Chat Liza-Me</h1>
                        <p>Last message: {last_message}</p>
                        <form method="POST">
                            <input type="text" name="mess" placeholder="Type message..." required>
                            <button type="submit">Send</button>
                        </form>
                        <p><a href="/{current_user.name}">Back to profile</a></p>
                    </body>
                    </html>
                    """, 200
                    
            except Exception as e:
                print(f"Liza-Me chat error: {e}")
                import traceback
                traceback.print_exc()
                return f"Liza-Me chat error: {str(e)}. Please try again.", 500
        else: 
            abort(403)
    else:
        return redirect('/')