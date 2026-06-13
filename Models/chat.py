from database import chat_collection
from bson import ObjectId
from datetime import datetime


# ==========================
# CREATE NEW CHAT
# ==========================

def create_chat(
    user_id,
    title="New Chat"
):

    result = chat_collection.insert_one(
        {
            "user_id": user_id,
            "title": title,
            "messages": [],
            "created_at": datetime.now()
        }
    )

    return str(result.inserted_id)


# ==========================
# SAVE MESSAGE
# ==========================

def save_message(
    chat_id,
    role,
    content
):

    chat_collection.update_one(
        {
            "_id": ObjectId(chat_id)
        },
        {
            "$push": {
                "messages": {
                    "role": role,
                    "content": content
                }
            }
        }
    )


# ==========================
# GET USER CHATS
# ==========================

def get_user_chats(user_id):

    return list(
        chat_collection.find(
            {
                "user_id": user_id
            }
        ).sort(
            "created_at",
            -1
        )
    )


# ==========================
# GET SINGLE CHAT
# ==========================

def get_chat(chat_id):

    return chat_collection.find_one(
        {
            "_id": ObjectId(chat_id)
        }
    )


# ==========================
# DELETE CHAT
# ==========================

def delete_chat(chat_id):

    chat_collection.delete_one(
        {
            "_id": ObjectId(chat_id)
        }
    )


# ==========================
# UPDATE CHAT TITLE
# ==========================

def update_chat_title(
    chat_id,
    title
):

    chat_collection.update_one(
        {
            "_id": ObjectId(chat_id)
        },
        {
            "$set": {
                "title": title
            }
        }
    )


# ==========================
# GET CHAT MESSAGES
# ==========================

def get_chat_messages(
    chat_id
):

    chat = get_chat(chat_id)

    if chat:

        return chat.get(
            "messages",
            []
        )

    return []