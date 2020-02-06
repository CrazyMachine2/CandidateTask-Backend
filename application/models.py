from application import db
from application import ma

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    temp_celsius = db.Column(db.Integer, nullable=False)
    temp_fahrenheit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'City({self.name}, {self.temp_celsius}, {self.temp_fahrenheit})'
        
class CitySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'temp_celsius', 'temp_fahrenheit')
        