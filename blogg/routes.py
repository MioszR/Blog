from flask import render_template, request, flash, redirect, url_for, session
from blogg import app
from blogg.models import Entry, db
from blogg.forms import EntryForm
import functools


def entry(entry_id):
    errors = None
    if entry_id == None:
        form = EntryForm()
        if request.method == "POST":
            if form.validate_on_submit():
                post = Entry(title=form.title.data, body=form.body.data, is_published=form.is_published.data)  # noqa: E501
                db.session.add(post)
                db.session.commit()
                flash('Post został pomyślnie dodany!')
                return redirect(url_for("index"))
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)
    elif entry_id != 0:
        entry = Entry.query.filter_by(id=entry_id).first_or_404()
        form = EntryForm(obj=entry)
        if request.method == "POST":
            if form.validate_on_submit():
                form.populate_obj(entry)
                db.session.commit()
                flash('Post został pomyślnie zmieniony!')
                return redirect(url_for("index"))
            else:
                errors = form.errors
        return render_template("entry_form.html", form=form, errors=errors)


@app.route("/")
def index():
   all_post = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
   return render_template("homepage.html", all_posts=all_post)

@app.route("/new-post/", methods=["GET", "POST"])
def create_entry():
    return entry(entry_id=None)


@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def edit_entry(entry_id):
    return entry(entry_id)