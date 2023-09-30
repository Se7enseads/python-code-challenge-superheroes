"""
This is a Flask application that provides an API for managing Heroes and Powers.
"""

from models import db, Hero, Power, HeroPower
import os

from flask import Flask, request, render_template
from flask_migrate import Migrate
from flask_restful import Api, Resource

from dotenv import load_dotenv

load_dotenv()


app = Flask(
    __name__,
    static_url_path='',
    static_folder='../client/build',
    template_folder='../client/build'
)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)

CORS(app)

@app.errorhandler(404)
def not_found(e):
    return render_template("index.html")

class Heroes(Resource):
    """
    Resource for retrieving a list of heroes.
    """

    def get(self):
        """
        Get a list of all heroes.

        Returns:
            list: A list of hero data.
        """
        heroes = Hero.query.all()

        heroes_data = []
        for hero in heroes:
            hero_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            }
            heroes_data.append(hero_data)

        return heroes_data, 200


api.add_resource(Heroes, '/heroes')


class HeroesByID(Resource):
    """
    Resource for retrieving hero details by ID.
    """

    def get(self, num):
        """
        Get details of a hero by ID.

        Args:
            num (int): The ID of the hero to retrieve.

        Returns:
            dict: A dictionary containing hero details.
        """
        hero = Hero.query.filter(Hero.id == num).first()

        if hero:
            hero_body = {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name,
                "powers": [
                    {
                        "id": hero_power.power.id,
                        "name": hero_power.power.name,
                        "description": hero_power.power.description
                    }
                    for hero_power in hero.hero_powers
                ]
            }

            return hero_body

        return {
            "error": "Hero not found"
        }, 404


api.add_resource(HeroesByID, '/heroes/<int:num>')


class Powers(Resource):
    """
    Resource for retrieving a list of powers.
    """

    def get(self):
        """
        Get a list of all powers.

        Returns:
            list: A list of power data.
        """
        powers = Power.query.all()

        powers_data = []
        for power in powers:
            power_data = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
            powers_data.append(power_data)

        return powers_data, 200


api.add_resource(Powers, '/powers')


class PowersByID(Resource):
    """
    Resource for retrieving power details by ID and updating powers.
    """

    def get(self, num):
        """
        Get details of a power by ID.

        Args:
            num (int): The ID of the power to retrieve.

        Returns:
            dict: A dictionary containing power details.
        """
        power = Power.query.filter(Power.id == num).first()

        if power:
            power_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return power_body, 200

        return {
            "error": "Power not found"
        }, 404

    def patch(self, num):
        """
        Update power details by ID.

        Args:
            num (int): The ID of the power to update.

        Returns:
            dict: A dictionary containing updated power details.
        """
        power = Power.query.filter(Power.id == num).first()

        data = request.get_json()

        if power:
            for attr in data:
                setattr(power, attr, data[attr])

            db.session.add(power)
            db.session.commit()

            response_body = {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }

            return response_body, 201

        return {
            "error": "Power not found"
        }, 400


api.add_resource(PowersByID, '/powers/<int:num>')


class HeroPowers(Resource):
    """
    Resource for creating HeroPower relationships.
    """

    def post(self):
        """
        Create a new HeroPower relationship.

        Returns:
            dict: A dictionary containing hero details with the new HeroPower.
        """
        data = request.get_json()

        hero = Hero.query.filter(Hero.id == data['hero_id']).first()
        power = Power.query.filter(Power.id == data['power_id']).first()

        if not hero or not power:
            return {
                "errors": ["Hero or Power doesn't exist"]
            }, 404

        new_hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )

        db.session.add(new_hero_power)
        db.session.commit()

        hero_data = HeroesByID().get(hero.id)

        return hero_data, 201


api.add_resource(HeroPowers, '/hero_powers')


if __name__ == "__main__":
    app.run(port=8000, debug=True)
