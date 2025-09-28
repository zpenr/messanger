from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from flask_login import current_user
from ..models.messageMakar import MassageMakar
from ..extensions import db

me_makar = Blueprint('me/me_makar', __name__)

@me_makar.route('/me/chat_me_makar', methods=['POST', 'GET'])
def chat_me_makar():
    if current_user.is_authenticated:
        if current_user.name in ['me']:
            try:
                if request.method == "POST":
                    mess = request.form.get('mess', '')
                    if len(mess) > 0:
                        message = MassageMakar(massage=mess, author_of_massage='me')
                        
                        db.session.add(message)
                        db.session.commit()
                        print(f"Makar message saved: {mess}")
                        
                        return redirect('/me/chat_me_makar')
                    else:
                        print("Empty Makar message received")
                
                # GET request or POST with empty message
                messages = Massage.query.all()
                messagesMakar = MassageMakar.query.all()
                
                # Safe handling of empty message lists
                last_message = messages[-1].massage if messages else "Нет сообщений"
                last_message_makar = messagesMakar[-1].massage if messagesMakar else "Нет сообщений"
                
                print(f"Loading Makar chat: {len(messages)} messages, {len(messagesMakar)} makar messages")
                
                try:
                    return render_template('chats/memakar.html', 
                                         messages=messagesMakar, 
                                         last_message=last_message, 
                                         last_message_makar=last_message_makar)
                except Exception as e:
                    print(f"Template error: {e}")
                    # Fallback HTML
                    return f"""
                    <html>
                    <head><title>Chat Me-Makar</title></head>
                    <body>
                        <h1>Chat Me-Makar</h1>
                        <p>Last message: {last_message}</p>
                        <p>Last Makar message: {last_message_makar}</p>
                        <form method="POST">
                            <input type="text" name="mess" placeholder="Type message..." required>
                            <button type="submit">Send</button>
                        </form>
                        <p><a href="/me">Back to profile</a></p>
                    </body>
                    </html>
                    """, 200
                    
            except Exception as e:
                print(f"Makar chat error: {e}")
                import traceback
                traceback.print_exc()
                return f"Makar chat error: {str(e)}. Please try again.", 500
        else: 
            abort(403)
    else:
        return redirect('/')