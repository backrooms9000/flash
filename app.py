from flask import Flask, render_template

sitename = "My Flask"

app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "_base.html",
        sitename=sitename
    )
     

@app.route("/about")
def about():
    return render_template( 
        'about.html',
        sitename=sitename
   )


if __name__ == "__main__":
    app.run(debug=True)
