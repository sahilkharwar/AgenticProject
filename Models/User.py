from database import users_collection

def create_user(name, age, weight, height):

    user = {
        "name": name,
        "age": age,
        "weight": weight,
        "height": height
    }

    users_collection.insert_one(user)