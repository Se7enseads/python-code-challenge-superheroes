"""
Populates the database with random Hero, Power, and HeroPower data.
"""

import random
from faker import Faker
from models import db, Hero, HeroPower, Power

from app import app

# List of hero names and powers
hero_names = [
    "Superhero1",
    "Superhero2",
    "Superhero3",
    "Superhero4",
    "Superhero5",
]

powers = [
    "Flight",
    "Super Strength",
    "Telekinesis",
    "Invisibility",
    "Teleportation",
]

with app.app_context():
    fake = Faker()

    # Clear existing data
    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

    heroes = []

    # Populate Heroes
    for _ in range(50):
        new_hero = Hero(
            name=fake.name(),
            super_name=fake.first_name(),
        )
        heroes.append(new_hero)

    db.session.add_all(heroes)
    db.session.commit()
    print("Hero successfully populated")

    powers_list = []

    # Populate Powers
    for power_name in powers:
        new_power = Power(
            name=power_name,
            description=fake.sentence()
        )
        powers_list.append(new_power)

    db.session.add_all(powers_list)
    db.session.commit()
    print("Power successfully populated")

    heroes_powers = []

    # Populate HeroPower relationships
    for _ in range(50):
        strengths = ['Strong', 'Weak', 'Average']

        new_hero_power = HeroPower(
            hero_id=random.randint(1, 50),
            power_id=random.randint(1, 5),
            strength=random.choice(strengths)
        )

        heroes_powers.append(new_hero_power)

    db.session.add_all(heroes_powers)
    db.session.commit()
    print("Hero Power successfully populated")
