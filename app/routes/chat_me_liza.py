from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from ..models.messageMakar import MassageMakar
from ..extensions import db
from flask_login import current_user
me_liza = Blueprint('me/me_liza', __name__)

@me_liza.route('/me/chat_me_liza', methods=['POST', 'GET'])
def chat_me_liza():
    if current_user.is_authenticated:
        if current_user.name in ['me']:
            if request.method == "POST":
                mess = request.form['mess']
                if len(mess)>0:
                    message = Massage( massage = mess, author_of_massage = 'me')

                    try:
                        db.session.add(message)
                        db.session.commit()
                        
                        return redirect('/me/chat_me_liza')
                    except Exception as e:
                        print(str(e))
                else: 
                    messages = Massage.query.all()
                    last_message = messages[-1].massage
                    messagesMakar = MassageMakar.query.all()
                    if len(messagesMakar)>0:
                        last_message_makar = messagesMakar[-1].massage
                    else: last_message_makar = "Нет сообщений"
                return render_template('chats/meliza.html', messages = messages, last_message=last_message, last_message_makar = last_message_makar)
                
            else:
                messages = Massage.query.all()
                last_message = messages[-1].massage
                messagesMakar = MassageMakar.query.all()
                if len(messagesMakar)>0:
                    last_message_makar = messagesMakar[-1].massage
                else: last_message_makar = "Нет сообщений"
                return render_template('chats/meliza.html', messages = messages, last_message=last_message, last_message_makar = last_message_makar)
        else: abort(403)