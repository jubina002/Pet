# type:ignore[Any]
import sqlite3
from pet import DATABASE


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()
iamge_name="poodle.jpg"
fake_dogs = [
    (
        "Buddy",
        "Golden Retriever",
        "3 years",
        "24 inches",
        "65 lbs",
        f"static/img/{iamge_name}.png",
        "Friendly and energetic, loves to play fetch.",
    ),
    (
        "Max",
        "German Shepherd",
        "4 years",
        "26 inches",
        "75 lbs",
        f"static/img/{iamge_name}.png",
        "Loyal and protective, great with families.",
    ),
    (
        "Bella",
        "Labrador Retriever",
        "2 years",
        "22 inches",
        "60 lbs",
        f"static/img/{iamge_name}.png",
        "Gentle and affectionate, enjoys swimming.",
    ),
    (
        "Charlie",
        "Beagle",
        "5 years",
        "15 inches",
        "30 lbs",
        f"static/img/{iamge_name}.png",
        "Curious and playful, loves to explore.",
    ),
    (
        "Lucy",
        "Bulldog",
        "6 years",
        "14 inches",
        "50 lbs",
        f"static/img/{iamge_name}.png",
        "Calm and loving, great with children.",
    ),
    (
        "Rocky",
        "Boxer",
        "3 years",
        "23 inches",
        "70 lbs",
        f"static/img/{iamge_name}.png",
        "Energetic and strong, needs plenty of exercise.",
    ),
    (
        "Daisy",
        "Poodle",
        "4 years",
        "18 inches",
        "40 lbs",
        f"static/img/{iamge_name}.png",
        "Intelligent and friendly, easy to train.",
    ),
    (
        "Molly",
        "Chihuahua",
        "2 years",
        "8 inches",
        "6 lbs",
        f"static/img/{iamge_name}.png",
        "Small and sassy, loves to cuddle.",
    ),
    (
        "Bailey",
        "Dachshund",
        "5 years",
        "9 inches",
        "16 lbs",
        f"static/img/{iamge_name}.png",
        "Curious and lively, loves to dig.",
    ),
    (
        "Zoe",
        "Rottweiler",
        "3 years",
        "25 inches",
        "85 lbs",
        f"static/img/{iamge_name}.png",
        "Protective and confident, great guard dog.",
    ),
    (
        "Oscar",
        "Shih Tzu",
        "4 years",
        "11 inches",
        "12 lbs",
        f"static/img/{iamge_name}.png",
        "Affectionate and alert, loves attention.",
    ),
    (
        "Luna",
        "Siberian Husky",
        "3 years",
        "22 inches",
        "55 lbs",
        f"static/img/{iamge_name}.png",
        "Energetic and mischievous, loves to run.",
    ),
]

cursor.executemany(
    """
INSERT INTO dog (name, breed, age, height, weight, image, description) 
VALUES (?, ?, ?, ?, ?, ?, ?)
""",
    fake_dogs,
)

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Fake data inserted successfully.")
