from database import users_collection
import bcrypt


def register_user(username, email, password):

    existing_user = users_collection.find_one(
        {"email": email}
    )

    if existing_user:
        return False

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    users_collection.insert_one({
        "username": username,
        "email": email,
        "password": hashed_password
    })

    return True


def login_user(email, password):

    user = users_collection.find_one(
        {"email": email}
    )

    if not user:
        return None

    if bcrypt.checkpw(
        password.encode("utf-8"),
        user["password"]
    ):
        return user

    return None