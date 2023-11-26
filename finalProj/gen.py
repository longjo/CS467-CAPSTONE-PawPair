from app import db, Pet
from faker import Faker
import random

fake = Faker()

def create_random_pet():
    name = fake.first_name()
    species = random.choice(['Dog', 'Cat'])
    breed = fake.word(ext_word_list=['Labrador', 'Bulldog', 'Siamese', 'Persian', 'Beagle', 'Maine Coon']) if species == 'Dog' else fake.word(ext_word_list=['Siamese', 'Persian', 'Maine Coon', 'Ragdoll', 'Bengal'])
    age = random.randint(1, 15)
    description = fake.sentence(nb_words=20)
    picture_url = 'images/placeholder.jpeg'  # Placeholder image path

    return Pet(name=name, species=species, breed=breed, age=age, description=description, picture_url=picture_url)

# Generate and add 30 pets
for _ in range(30):
    pet = create_random_pet()
    db.session.add(pet)

db.session.commit()
print("30 random dogs and cats added to the database.")
