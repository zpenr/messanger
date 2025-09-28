from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from ..models.messageMakar import MassageMakar
from ..extensions import db
from flask_login import current_user
makar_me = Blueprint('makar/makar_me', __name__)

@makar_me.route('/makar/chat_makar_me', methods=['POST', 'GET'])
def chat_makar_me():
    return handle_makar_me_chat()

@makar_me.route('/me/chat_makar_me', methods=['POST', 'GET'])
def chat_me_makar_me():
    return handle_makar_me_chat()

def handle_makar_me_chat():
    if current_user.is_authenticated:
        if current_user.name in ['me', 'makar']:
            try:
                if request.method == "POST":
                    mess = request.form.get('mess', '')
                    if len(mess) > 0:
                        # Determine author based on current user
                        author = 'makar' if current_user.name == 'makar' else 'me'
                        message = MassageMakar(massage=mess, author_of_massage=author)
                        
                        db.session.add(message)
                        db.session.commit()
                        print(f"Makar-Me message saved: {mess} by {author}")
                        
                        # Redirect to appropriate URL based on current user
                        redirect_url = '/makar/chat_makar_me' if current_user.name == 'makar' else '/me/chat_makar_me'
                        return redirect(redirect_url)
                    else:
                        print("Empty Makar-Me message received")
                
                # GET request or POST with empty message
                messages = Massage.query.all()
                messagesMakar = MassageMakar.query.all()
                
                # Safe handling of empty message lists
                last_message = messages[-1].massage if messages else "Нет сообщений"
                last_message_makar = messagesMakar[-1].massage if messagesMakar else "Нет сообщений"
                
                print(f"Loading Makar-Me chat: {len(messages)} messages, {len(messagesMakar)} makar messages")
                
                try:
                    return render_template('chats/makarme.html', 
                                         messages=messagesMakar, 
                                         last_message=last_message, 
                                         last_message_makar=last_message_makar)
                except Exception as e:
                    print(f"Template error: {e}")
                    # Fallback HTML
                    return f"""
                    <html>
                    <head><title>Chat Makar-Me</title></head>
                    <body>
                        <h1>Chat Makar-Me</h1>
                        <p>Last message: {last_message}</p>
                        <p>Last Makar message: {last_message_makar}</p>
                        <form method="POST">
                            <input type="text" name="mess" placeholder="Type message..." required>
                            <button type="submit">Send</button>
                        </form>
                        <p><a href="/{current_user.name}">Back to profile</a></p>
                    </body>
                    </html>
                    """, 200
                    
            except Exception as e:
                print(f"Makar-Me chat error: {e}")
                import traceback
                traceback.print_exc()
                return f"Makar-Me chat error: {str(e)}. Please try again.", 500
        else: 
            abort(403)
    else:
        return redirect('/')
