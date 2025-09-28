from flask import Blueprint, render_template, request, redirect, abort
from ..models.massage import Massage
from ..extensions import db
from flask_login import current_user
liza_me = Blueprint('liza/liza_me', __name__)

@liza_me.route('/liza/chat_liza_me', methods=['POST', 'GET'])
def chat_liza_me():
    if current_user.is_authenticated:
        if current_user.name in ['me', 'liza']:
            if request.method == "POST":
                mess = request.form['mess']
                if len(mess)>0:
                    message = Massage( massage = mess, author_of_massage = 'liza')

                    try:
                        db.session.add(message)
                        db.session.commit()
                        
                        return redirect('/liza/chat_liza_me')
                    except Exception as e:
                        print(str(e))
                else: 
                    messages = Massage.query.all()
                    last_message = messages[-1].massage
                return render_template('chats/lizame.html', messages = messages, last_message=last_message)
                
            else:
                messages = Massage.query.all()
                last_message = messages[-1].massage
                return render_template('chats/lizame.html', messages = messages, last_message=last_message)
        else: abort(403)