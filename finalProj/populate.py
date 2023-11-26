from app import db, Pet, User
from werkzeug.security import generate_password_hash
import random

# Deleting existing data
db.drop_all()
db.create_all()

# Common breeds for cats and dogs
dog_breeds = ["Labrador Retriever", "German Shepherd", "Golden Retriever", "French Bulldog", "Bulldog"]
cat_breeds = ["Exotic Shorthair", "Ragdoll", "British Shorthair", "Persian", "Maine Coon"]

# Random names for pets
pet_names = ["Buddy", "Max", "Bella", "Charlie", "Lucy", "Molly", "Daisy", "Luna", "Cooper", "Rocky"]

# Random descriptions
descriptions = ["Loving and energetic", "Calm and affectionate", "Needs lots of exercise", 
                "Good with children", "Quiet and gentle"]

# Creating pets
for _ in range(30):
    species_choice = random.choice(["Dog", "Cat"])
    breed_choice = random.choice(dog_breeds if species_choice == "Dog" else cat_breeds)
    pet = Pet(
        name=random.choice(pet_names),
        species=species_choice,
        breed=breed_choice,
        age=random.randint(1, 10),
        description=random.choice(descriptions),
        status="Available",
        disposition="Good with children" if species_choice == "Dog" else "Needs a quiet home",
        availability="Available",
        picture_url=f"images/{'dog1' if species_choice == 'Dog' else 'cat1'}.jpg",  # Corrected image path
        news_item=f"A lovely {species_choice.lower()} looking for a home"
    )
    db.session.add(pet)

# Creating users
hashed_password_admin = generate_password_hash("admin123")
hashed_password_user = generate_password_hash("user123")

admin = User(username="admin", email="admin@example.com", 
             password=hashed_password_admin, contact_number="123-456-7890", is_admin=True)
user = User(username="user", email="user@example.com", 
            password=hashed_password_user, contact_number="098-765-4321", is_admin=False)

db.session.add(admin)
db.session.add(user)

db.session.commit()

print("Database populated!")
