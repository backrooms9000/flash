'''
app.py
Aplicativo principal
'''

from flask import Flask, abort, flash, redirect, render_template, request, url_for
import sqlite3
import random

app = Flask(__name__)

app.secret_key = '_use_uma_secret_key_de_verdade_aqui_e_use_dotenv_em_deploy_'


@app.route("/")
def index():

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        contents = conn.execute("""
            SELECT id, name, photo
            FROM thing
                WHERE status = 'on'
                ORDER BY created_at DESC
        """).fetchall()

    total = len(contents)

    return render_template(
        'index.html',
        contents=contents,
        total=total
    )


@app.route('/view/<int:thing_id>')
def view(thing_id):

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row
        content = conn.execute("""
            SELECT *
            FROM thing
                WHERE status = 'on'
                AND id = ?
                ORDER BY created_at
        """, (thing_id,)).fetchone()

    if content is None:
        abort(404)

    return render_template(
        "view.html",
        content=content
    )


@app.route("/new", methods=['GET', 'POST'])
def new_thing():

    photo_number = random.randint(10, 999)

    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        location = request.form['location'].strip()
        photo = request.form['photo'].strip()

        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute("""
                INSERT INTO thing (
                    name, description, location, photo
                ) VALUES (?, ?, ?, ?)
            """, (name, description, location, photo))
        
            flash('Registro cadastrado com sucesso!', 'success')

            return redirect(url_for('view', thing_id=cursor.lastrowid))

    return render_template(
        "new.html",
        photo_number=photo_number
    )


@app.route('/edit/<int:thing_id>', methods=['GET', 'POST'])
def edit(thing_id):

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row

        content = conn.execute("""
            SELECT *
            FROM thing
            WHERE status = 'on'
              AND id = ?
        """, (thing_id,)).fetchone()

    if content is None:
        abort(404)

    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form['description'].strip()
        location = request.form['location'].strip()
        photo = request.form['photo'].strip()

        with sqlite3.connect('database.db') as conn:
            conn.execute("""
                UPDATE thing
                SET
                    name = ?,
                    description = ?,
                    location = ?,
                    photo = ?
                WHERE status = 'on'
                  AND id = ?
            """, (name, description, location, photo, thing_id))

        flash('Registro atualizado com sucesso!', 'success')

        return redirect(url_for('view', thing_id=thing_id))

    return render_template(
        'edit.html',
        content=content
    )


@app.route('/delete/<int:thing_id>')
def delete(thing_id):

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row

        content = conn.execute("""
            SELECT id
            FROM thing
                WHERE status = 'on'
                    AND id = ?
        """, (thing_id,)).fetchone()

        if content is None:
            abort(404)

        conn.execute("""
            UPDATE thing 
                SET status = 'del'
                WHERE status = 'on'
                    AND id = ?
        """, (thing_id,))

        flash('Registro apagado com sucesso!', 'success')

        return redirect(url_for('index', thing_id=thing_id))


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
