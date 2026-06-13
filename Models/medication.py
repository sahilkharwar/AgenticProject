from datetime import datetime
from database import med_collection
from bson import ObjectId


def add_medication(
    user_id,
    medicine,
    dosage,
    time,
    frequency
):

    med_collection.insert_one(
        {
            "user_id": user_id,
            "medicine": medicine,
            "dosage": dosage,
            "time": time,
            "frequency": frequency,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_taken": False,
            "last_taken_date": None
        }
    )


def get_medications(user_id):

    return list(
        med_collection.find(
            {
                "user_id": user_id
            }
        )
    )


def delete_medication(medication_id):

    med_collection.delete_one(
        {
            "_id": ObjectId(medication_id)
        }
    )


def update_medication(
    medication_id,
    medicine,
    dosage,
    time,
    frequency
):

    med_collection.update_one(
        {
            "_id": ObjectId(medication_id)
        },
        {
            "$set": {
                "medicine": medicine,
                "dosage": dosage,
                "time": time,
                "frequency": frequency,
                "updated_at": datetime.now()
            }
        }
    )


# ==========================
# MARK MEDICATION TAKEN
# ==========================

def mark_medication_taken(
    medication_id
):

    med_collection.update_one(
        {
            "_id": ObjectId(medication_id)
        },
        {
            "$set": {
                "is_taken": True,
                "last_taken_date": (
                    datetime.now()
                    .date()
                    .isoformat()
                )
            }
        }
    )


# ==========================
# DAILY RESET
# ==========================

def reset_daily_medications(
    user_id
):

    today = (
        datetime.now()
        .date()
        .isoformat()
    )

    medications = list(
        med_collection.find(
            {
                "user_id": user_id
            }
        )
    )

    for med in medications:

        if (
            med.get(
                "last_taken_date"
            )
            !=
            today
        ):

            med_collection.update_one(
                {
                    "_id": med["_id"]
                },
                {
                    "$set": {
                        "is_taken": False
                    }
                }
            )