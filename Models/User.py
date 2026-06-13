from database import users_collection
from bson import ObjectId


def get_user(user_id):

    return users_collection.find_one(
        {
            "_id": ObjectId(user_id)
        }
    )


def update_profile(
    user_id,
    age,
    height_feet,
    height_inches,
    weight
):

    users_collection.update_one(
        {
            "_id": ObjectId(user_id)
        },
        {
            "$set": {
                "age": age,
                "height_feet": height_feet,
                "height_inches": height_inches,
                "weight": weight
            }
        }
    )


def delete_user(user_id):

    users_collection.delete_one(
        {
            "_id": ObjectId(user_id)
        }
    )