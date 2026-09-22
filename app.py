# Importando as dependências
from flask import Flask, render_template
import sqlite3

# Inicializar variáveis e componentes

# Nome do aplicativo (Site da Web) → global
sitename = "My Flask"

# Inicializa o plaicativo Flask (HTTP)
app = Flask(__name__)

# Passa valores em comum para todas as páginas / rotas
@app.context_processor
def inject_globals():
    return {
        "sitename": sitename
    }

# Rota da página inicial (rota raiz ou root)
@app.route("/")
def index():

    # with controla a conesão e fecha quando não é mais necessária
    with sqlite3.connect('database.db') as conn:
        # Retorna os dados do banco no formato compatível com dict
        conn.row_factory = sqlite3.Row

        contents = conn.execute('''
            SELECT 
                c_id,
                c_title,
                substr(c_text, 1, 50) || '...' as c_resume
            FROM content 
                WHERE c_status = 'on'
                ORDER BY c_created_at DESC;            
        ''').fetchall()

    total = len(contents)

    return render_template(
        "home.html",
        tag_title=sitename,
        contents=contents,
        total=total
    )


'''
Criando páginas / rotas → Passos iniciais:
    1) Crie o template HTML em `/templates`
    2) Define a rota em `app.py`
    3) Cria a função para a rota
    4) Desenvolva a função para retornar o template HTML renderizado
'''

# Rota para exibir um content completo
@app.route('/view/<int:content_id>')
def view(content_id):

    exists = False
    tag_title = f"{sitename} - Conteúdo não existente"

 with sqlite3.connect('database.db') as conn:
        conn.row_factory = sqlite3.Row

        content = conn.execute('''
            SELECT 
                c_id, c_created_at, c_title, c_text,
                u_id, u_name, u_photo
            FROM content
            INNER JOIN fbuser ON c_owner = u_id
                WHERE c_status = 'on'
                AND c_id = ?;        
        ''', (content_id,)).fetchone()

    if content != None:
        exists = True
        tag_title = f"{sitename} - {content['c_title']}"

    return render_template(
        'view.html',
        tag_title=tag_title,
        content=content,
        exists=exists
    )

# Rota para '/contacts'
@app.route("/contacts", methods=['GET', 'POST'])
def contacts():
    return render_template(
        'contacts.html',
        tag_title=f"{sitename} - Faça Contato"
    )

@app.route("/about")
def about():
    return render_template(
        'about.html',
        tag_title=f"{sitename} - Sobre..."
    )


# Ativa o modo DEBUG e o main loop no localhost
if __name__ == "__main__":
    app.run(debug=True)
