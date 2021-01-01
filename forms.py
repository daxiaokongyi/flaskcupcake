from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Optional, URL

class AddCupcakeForm(FlaskForm):
    flavor = StringField("Flavor", validators=[InputRequired(message="Flavor is required")])
    size = StringField("Size", validators=[InputRequired(message="Flavor is required")] )
    rating = FloatField("Rating", validators=[InputRequired(message="Flavor is required")] )
    image = StringField("Photo Link", validators=[Optional(), URL()])