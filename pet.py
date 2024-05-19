# pyright: reportAny=false
from flask import Flask, request, render_template, redirect, url_for, session
import sqlite3 as sql
from hashlib import md5
from PIL import Image


DATABASE = "mydb.db"
with sql.connect(DATABASE) as con:
    try:
        cur = con.cursor()
        _ = cur.execute(
            """
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    address TEXT NOT NULL
)
"""
        )
        _ = cur.execute(
            """
CREATE TABLE IF NOT EXISTS dog (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    breed TEXT NOT NULL,
    age TEXT NOT NULL,
    height TEXT NOT NULL,
    weight TEXT NOT NULL,
    image TEXT NOT NULL,
    description TEXT NOT NULL
)
"""
        )
        _ = cur.execute(
            """
CREATE TABLE IF NOT EXISTS about_us (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    open_time TEXT NOT NULL
)
"""
        )
        _ = cur.execute(
            "INSERT INTO about_us (address,email,phone,open_time) VALUES (?,?,?,?)",
            (
                "Swoyambhu, Kathmandu",
                "pawsitivepetcare@gmail.com",
                "01-4890891",
                "Sun-Fri, 9am-6pm",
            ),
        )
        datas = [("admin", "password", "Admin User", "Kathmandu, Nepal")]
        _ = cur.executemany(
            """
                        INSERT INTO user (username, password, name, address)  VALUES (?,?,?,?)
                        """,
            datas,
        )

        con.commit()
    except Exception as e:
        print(f"Rolling Back {e}")
        con.rollback()

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = "randomKeysawdawdawdjawdauwdhiawuhduiawhduhawdhu"


def get_dogs(count:int=-1):
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        _ = cur.execute("SELECT * FROM dog")
        dogs = cur.fetchall()
        dogs_dic = [
            {
                "_id":_id,
                "name": name,
                "breed": breed,
                "age": age,
                "height": height,
                "weight": weight,
                'image': image,
                "desc": description,
            }
            for (
                _id,
                name,
                breed,
                age,
                height,
                weight,
                image,
                description,
            ) in dogs[:count]
        ]
        return dogs_dic


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    dogs_all = get_dogs(count=4)
    return render_template("home.html",context={"dogs":dogs_all})


@app.route("/about")
def about():
    (address, email, phone, open_time) = ("", "", "", "")
    with sql.connect(DATABASE) as con:
        cur = con.cursor()
        _ = cur.execute("SELECT * FROM about_us")
        cur_all = cur.fetchone()
        if cur_all:
            (_, address, email, phone, open_time) = cur_all

        return render_template(
            "about.html",
            context={
                "address": address,
                "email": email,
                "phone": phone,
                "open_time": open_time,
                "dogs": get_dogs(),
            },
        )


@app.route("/adopt/<_id>")
def adopt(_id:str):
    all_dogs = get_dogs()
    limited_dogs:list[dict[str,str]] =[] 
    main_dog = {}
    for dog in all_dogs:
        if str(dog["_id"])!=_id and len(limited_dogs)<6:
            limited_dogs.append(dog)
        elif str(dog["_id"]) ==_id:
            main_dog = dog
    if not main_dog:
        main_dog = limited_dogs[0]
    return render_template("adopt.html",context={"dog":main_dog,"dogs":limited_dogs })


@app.route("/adopt")
def my_adopt():
    return adopt("1")

@app.route("/sell",methods=["POST","GET"])
def sell():
    if request.method == "POST":
        conn = sql.connect(DATABASE)
        cursor = conn.cursor()
        name= request.form["name"]
        breed= request.form["breed"] 
        age= request.form["age"] 
        height= request.form["height"] 
        weight= request.form["weight"] 
        file = request.files['image']
        img = Image.open(file.stream) # type:ignore[reportUnknownMemberType]
        iamge_name = md5(img.tobytes())# type:ignore[reportUnknownMemberType]
        iamge_name = iamge_name.hexdigest()
        iamge_name = f"static/img/{iamge_name}.png"
        with open(iamge_name,"wb") as fp:
            img.save(fp)# type:ignore[reportUnknownMemberType]
        description= request.form["description"] 
        _ =cursor.execute(
        """
    INSERT INTO dog (name, breed, age, height, weight, image, description) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (name, breed, age, height, weight, iamge_name, description),
    )   
        
        conn.commit()
        conn.close()
        return render_template("sell.html")
    else:

        return render_template("sell.html")


@app.route("/seemore")
def seemore():
    return render_template("seemore.html",context={"dogs":get_dogs(count=10)})


@app.route("/login", methods=["POST", "GET"])
def account():
    msg = "Username or Password Didnot match"
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        with sql.connect(DATABASE) as con:
            cur = con.cursor()
            _ = cur.execute(
                "SELECT * FROM user WHERE username=? AND password=?",
                (username, password),
            )
            user = cur.fetchone()

            if user:
                session["username"] = username
                msg = "Successfully logged in"
                return redirect(url_for("dashboard"))
        return render_template("account.html", context={"msg": msg})
    else:
        return render_template("account.html")


@app.route("/dashboard")
def dashboard():
    if "username" in session:
        return f'Welcome {session["username"]}!'
    else:
        return redirect(url_for("account"))


@app.route("/logout")
def logout():
    session.pop("username", None) # type:ignore [reportUnknownType]
    return redirect(url_for("account"))


if __name__ == "__main__":
    app.run()
