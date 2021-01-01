"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake, GENERAL_IMAGE
from flask_cors import CORS

from forms import AddCupcakeForm


app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'thisissecretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

def serialize_cupcake(cupcake):
    """convert cupcake instance into json format"""
    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/", methods=["GET", "POST"])
def home_page():
    """Add a cupcake into the list"""
    form = AddCupcakeForm()
    if form.validate_on_submit():
        data = {k: v for k,v in form.data.items() if k != 'csrf_token'}
        new_cupcake = Cupcake(**data)

        new_cupcake.image = new_cupcake.image_url()

        db.session.add(new_cupcake)
        db.session.commit()
        flash(f'{new_cupcake.flavor} was added.')
        return redirect('/')
    else:
        return render_template('home.html', form = form)

@app.route('/api/cupcakes', methods=['GET'])
def list_cupcakes():
    """Get all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [serialize_cupcake(c) for c in cupcakes]

    return jsonify(cupcakes = serialized)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    """Get cupcake's detail"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = serialize_cupcake(cupcake)

    return jsonify(cupcake = serialized)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """Create a cupcake"""
    flavor = request.json['flavor']
    image = request.json['image']
    rating = request.json['rating']
    size = request.json['size']
    
    new_cupcake = Cupcake(flavor = flavor, image = image, rating = rating, size = size)
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = serialize_cupcake(new_cupcake)
    return (jsonify(cupcake = serialized),201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def edit_cupcake(cupcake_id):
    """Update a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)    
    cupcake.image = request.json.get('image', cupcake.image)   
    cupcake.rating = request.json.get('rating', cupcake.rating)

    db.session.commit()

    serialized = serialize_cupcake(cupcake)
    return jsonify(serialized) 

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    """Delete a cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake) 
    db.session.commit()
    return jsonify(messege = "Deleted")

