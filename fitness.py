from database import fitness_collection

def add_fitness_data(user_id, steps, calories):

    data = {
        "user_id": user_id,
        "steps": steps,
        "calories": calories
    }

    fitness_collection.insert_one(data)