from database import (
    fitness_collection,
    goal_collection
)
from bson import ObjectId
from datetime import datetime


def add_fitness_data(
    user_id,
    value,
    calories,
    category,
    unit,
    activity_date
):

    fitness_collection.insert_one(
        {
            "user_id": user_id,
            "value": value,
            "unit": unit,
            "calories": calories,
            "category": category,
            "date": activity_date
        }
    )


def get_fitness_data(user_id):

    return list(
        fitness_collection.find(
            {
                "user_id": user_id
            }
        )
    )


def delete_fitness_record(record_id):

    fitness_collection.delete_one(
        {
            "_id": ObjectId(record_id)
        }
    )


def get_fitness_by_category(
    user_id,
    category
):

    return list(
        fitness_collection.find(
            {
                "user_id": user_id,
                "category": category
            }
        )
    )


def update_fitness_record(
    record_id,
    value,
    calories
):

    fitness_collection.update_one(
        {
            "_id": ObjectId(record_id)
        },
        {
            "$set": {
                "value": value,
                "calories": calories
            }
        }
    )


# ==========================
# FITNESS STREAK
# ==========================

def get_fitness_streak(user_id):

    records = list(
        fitness_collection.find(
            {
                "user_id": user_id
            }
        ).sort(
            "date",
            1
        )
    )

    if not records:

        return 0

    unique_dates = sorted(
        {
            record["date"].date()
            for record in records
        }
    )

    today = datetime.now().date()

    # If no activity today or yesterday,
    # streak is considered broken

    if (
        today - unique_dates[-1]
    ).days > 1:

        return 0

    current_streak = 1

    for i in range(
        len(unique_dates) - 1,
        0,
        -1
    ):

        difference = (
            unique_dates[i]
            -
            unique_dates[i - 1]
        ).days

        if difference == 1:

            current_streak += 1

        else:

            break

    return current_streak


# ==========================
# FITNESS GOALS
# ==========================

def set_daily_goal(
    user_id,
    goal
):

    goal_collection.update_one(
        {
            "user_id": user_id
        },
        {
            "$set": {
                "goal": goal
            }
        },
        upsert=True
    )


def get_daily_goal(
    user_id
):

    goal = goal_collection.find_one(
        {
            "user_id": user_id
        }
    )

    if goal:

        return goal.get(
            "goal",
            10000
        )

    return 10000