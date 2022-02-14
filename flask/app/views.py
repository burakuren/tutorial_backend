from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import current_user, login_required
import json
from . import db 
from .models import Note
views = Blueprint("views",__name__,url_prefix='/')

@views.route("/",methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:

            flash("Note is too short!",category="error")
        else:

            new_note = Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()

            flash("Note added!",category="success")

    return render_template("home.html", user=current_user)

@views.route("/delete-note",methods=["POST"])
def delete_note():
    data = json.loads(request.data)
    noteID = data["noteID"]
    note = Note.query.filter_by(id=noteID).first()

    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted!",category="success")
        
    return jsonify({})
