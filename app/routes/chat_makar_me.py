from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from ..models.messageMakar import MassageMakar
from ..extensions import db
from flask_login import current_user
makar_me = Blueprint('makar/makar_me', __name__)

@makar_me.route('/makar/chat_makar_me', methods=['POST', 'GET'])
def chat_makar_me():
    if current_user.is_authenticated:
        if current_user.name in ['me', 'makar'] :
            if request.method == "POST":
                mess = request.form['mess']
                if len(mess)>0:
                    message = MassageMakar( massage = mess, author_of_massage = 'makar')

                    try:
                        db.session.add(message)
                        db.session.commit()
                        
                        return redirect('/makar/chat_makar_me')
                    except Exception as e:
                        print(str(e))
                else: 
                    messages = Massage.query.all()
                    last_message = messages[-1].massage
                    messagesMakar = MassageMakar.query.all()
                    if len(messagesMakar)>0:
                        last_message_makar = messagesMakar[-1].massage
                    else: last_message_makar = "Нет сообщений"
                return render_template('chats/makarme.html', messages = messagesMakar, last_message=last_message, last_message_makar = last_message_makar )
                
            else:
                messages = Massage.query.all()
                last_message = messages[-1].massage
                messagesMakar = MassageMakar.query.all()
                if len(messagesMakar)>0:
                    last_message_makar = messagesMakar[-1].massage
                else: last_message_makar = "Нет сообщений"
                return render_template('chats/makarme.html', messages = messagesMakar, last_message=last_message, last_message_makar = last_message_makar)
        else: abort(403)
