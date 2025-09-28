from flask import Blueprint, render_template, request, redirect
from ..models.massage import Massage
from ..extensions import db
massage = Blueprint('massage', __name__)

# @massage.route('/chat_me_liza', methods = ['POST','GET'])
# def create():
#     if request.method == "POST":
#         mess = request.form['mess']
#         print(mess)
#         return redirect('/chat_me_liza')
#     else: return render_template('chats/meliza.html')
