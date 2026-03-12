from database import med_collection

def add_medication(user_id, medicine, dosage, time):

    med = {
        "user_id": user_id,
        "medicine": medicine,
        "dosage": dosage,
        "time": time
    }

    med_collection.insert_one(med)