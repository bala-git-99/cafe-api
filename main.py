from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update
from db_operations import *

'''
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

API_KEY = "TopSecretAPIKey"


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def get_random_cafe():
    r_cafe = random_cafe()
    r_cafe_dict = r_cafe.object_to_dict()
    return jsonify(cafe=r_cafe_dict)


@app.route("/all", methods=["GET"])
def get_all_cafes():
    all_cafes = select_all()
    list_of_all_cafes = [cafe.object_to_dict() for cafe in all_cafes]
    return jsonify(cafes=list_of_all_cafes)


@app.route("/search", methods=["GET"])
def search_a_cafe():
    search_location = request.args.get("loc")
    searched_cafes = search(search_location)
    if searched_cafes is None:
        error_msg = "Sorry, we don't have a cafe at that location."
        return jsonify(error={"Not Found": error_msg})
    else:
        return jsonify(cafes=[cafe.object_to_dict() for cafe in searched_cafes])


@app.route("/add", methods=["POST"])
def add_a_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("location"),
        has_sockets=bool(request.form.get("has_sockets")),
        has_toilet=bool(request.form.get("has_toilet")),
        has_wifi=bool(request.form.get("has_wifi")),
        can_take_calls=bool(request.form.get("can_take_calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe_to_update = db.session.get(Cafe, cafe_id)
    new_price = request.args.get("new_price")
    if not cafe_to_update:
        error_msg = "Sorry, a cafe with that id was not found in the database."
        return jsonify(error={"Not Found": error_msg}), 404
    else:
        # update_query = (
        #     update(Cafe).where(Cafe.id == cafe_id).values(coffee_price=new_price)
        # )
        # db.session.execute(update_query)
        # db.session.commit()
        # Simple Alternative
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."}), 200


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    cafe_to_delete = db.session.get(Cafe, cafe_id)
    input_key = request.args.get("api-key")
    if not cafe_to_delete:
        error_msg = "Sorry, a cafe with that id was not found in the database."
        return jsonify(error={"Not Found": error_msg}), 404
    elif input_key != API_KEY:
        error_msg = "Sorry, that's not allowed. Make sure you have the correct api_key."
        return jsonify(error={"Forbidden": error_msg}), 403
    else:
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify(response={"success": "Successfully delete the cafe from database."}), 200

# HTTP GET - Read Record

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
