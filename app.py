'''
app.py
Aplicativo principal
'''

from flask import Flask, abort, flash, redirect, render_template, request, url_for
import sqlite3
import random
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.secret_key = '_use_uma_secret_key_de_verdade_aqui_e_use_dotenv_em_deploy_'


@app.route("/api/things")
@app.route("/")
w
    page = request.args.get("p", 1, type=int)

    per_page = 10
    offset = (page - 1) * per_page

    with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row

        contents = conn.execute("""
            SELECT id, name, photo
            FROM thing
            WHERE status = 'on'
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """, (per_page, offset)).fetchall()

        total = conn.execute("""
            SELECT COUNT(*)
            FROM thing
            WHERE status = 'on'
        """).fetchone()[0]

    pages = (total + per_page - 1) // per_page

    if request.path.startswith('/api/'):
        return {
            "data": [dict(content) for content in contents],
            "metadata": {
                "total": total,
                "page": page,
                "pages": pages
            }
        }

    return render_template(
        'index.html',
        contents=contents,
        total=total,
        page=page,
        pages=pages,
        page_css='index.css'
    )


@app.route('/api/things/<int:thing_id>')
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

    if request.path.startswith('/api/'):
        return {
            "data": dict(content),
        }

    return render_template(
        "view.html",
        content=content
    )


@app.route("/api/things", methods=["POST"])
@app.route("/new", methods=['GET', 'POST'])
def new_thing():

    photo_number = random.randint(10, 999)

    if request.method == 'POST':

        # Dados
        if request.path.startswith("/api/"):
            data = request.get_json()
        else:
            data = request.form

        name = data["name"].strip()
        description = data["description"].strip()
        location = data["location"].strip()
        photo = data["photo"].strip()

        # Tratar os dados que vieram do front

        with sqlite3.connect('database.db') as conn:
            cursor = conn.execute("""
                INSERT INTO thing (
                    name, description, location, photo
                ) VALUES (?, ?, ?, ?)
            """, (name, description, location, photo))

            thing_id = cursor.lastrowid

            # Response
        if request.path.startswith("/api/"):
            return {
                "id": thing_id,
                "name": name,
                "description": description,
                "location": location,
                "photo": photo
            }, 201

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
