from models import db, Hero, HeroPower, Power

from faker import Faker

import random
from app import app


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

    HeroPower.query.delete()
    Hero.query.delete()
    Power.query.delete()

    heroes = []

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

    for _ in range(50):

        strengths = ['Strong', 'Weak', 'Average']

        new_hero_power = HeroPower(
            hero_id=random.randint(1, 50),
            power_id=random.randint(1, 50),
            strength=random.choice(strengths)
        )

        heroes_powers.append(new_hero_power)

    db.session.add_all(heroes_powers)
    db.session.commit()
    print("Hero Power successfully populated")
