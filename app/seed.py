"""
Populate the database with random superhero data and their powers.

This script clears existing data and populates the database with random heroes,
powers, and their associations.
"""

import random
from faker import Faker
from models import db, Hero, HeroPower, Power
from app import app

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
    for _ in range(20):
        # Generate random name and superhero name using Faker
        new_hero = Hero(
            name=fake.name(),
            super_name=fake.first_name(),
        )
        heroes.append(new_hero)

    # Add heroes to the database
    db.session.add_all(heroes)
    db.session.commit()
    print("🦸 Seeding heroes...")

    powers_list = []

    # Populate Powers
    for power_name in powers:
        # Generate a description between 6 and 9 words for powers
        num_words = random.randint(6, 9)
        new_power = Power(
            name=power_name,
            description=fake.sentence(nb_words=num_words)
        )
        powers_list.append(new_power)

    # Add powers to the database
    db.session.add_all(powers_list)
    db.session.commit()
    print("🦸 Adding powers to heroes...")

    hero_powers = []

    for hero in heroes:
        # Randomly choose the number of powers (between 1 and 5)
        num_powers = random.randint(1, 5)

        # Randomly select powers from the list
        selected_powers = powers[:num_powers]

        strengths = ['Strong', 'Weak', 'Average']

        for power_name in selected_powers:
            # Find the power ID by name
            power = Power.query.filter(Power.name == power_name).first()

            new_hero_power = HeroPower(
                hero_id=hero.id,
                power_id=power.id,
                strength=random.choice(strengths)
            )
            hero_powers.append(new_hero_power)

    # Add HeroPower relationships to the database
    db.session.add_all(hero_powers)
    db.session.commit()
    print("🦸 Done seeding!")
