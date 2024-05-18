from flask import Flask, render_template
 
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True

 
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/adopt")
def adopt():
    return render_template("adopt.html")




@app.route("/sell")
def sell():
    return render_template("sell.html")



 
if __name__ == "__main__":
    app.run()