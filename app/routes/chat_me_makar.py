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
            if request.method == "POST":
                mess = request.form['mess']
                if len(mess)>0:
                    message = MassageMakar( massage = mess, author_of_massage = 'me')

                    try:
                        db.session.add(message)
                        db.session.commit()
                        
                        return redirect('/me/chat_me_makar')
                    except Exception as e:
                        print(str(e))
                else: 
                    messages = Massage.query.all()
                    last_message = messages[-1].massage
                    messagesMakar = MassageMakar.query.all()
                    if len(messagesMakar)>0:
                        last_message_makar = messagesMakar[-1].massage
                    else: last_message_makar = "Нет сообщений"
                return render_template('chats/memakar.html', messages = messagesMakar, last_message=last_message, last_message_makar = last_message_makar )
                
            else:
                messages = Massage.query.all()
                last_message = messages[-1].massage
                messagesMakar = MassageMakar.query.all()
                if len(messagesMakar)>0:
                    last_message_makar = messagesMakar[-1].massage
                else: last_message_makar = "Нет сообщений"
                return render_template('chats/memakar.html', messages = messagesMakar, last_message=last_message, last_message_makar = last_message_makar)
        else: abort(403)