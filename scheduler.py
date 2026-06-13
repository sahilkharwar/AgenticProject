from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, date
from bson import ObjectId

from database import (
    med_collection,
    users_collection
)

from Utils.email_sender import (
    send_medication_email
)


def check_medications():

    current_time = datetime.now().strftime(
        "%H:%M"
    )

    today = str(
        date.today()
    )

    medications = list(
        med_collection.find()
    )

    for med in medications:

        try:

            if med.get(
                "time"
            ) != current_time:

                continue

            # Prevent duplicate emails
            if (
                med.get(
                    "last_reminded"
                )
                ==
                today
            ):

                continue

            user_id = med.get(
                "user_id"
            )

            # Handle string ObjectId
            try:

                user = users_collection.find_one(
                    {
                        "_id": ObjectId(
                            user_id
                        )
                    }
                )

            except:

                user = users_collection.find_one(
                    {
                        "_id": user_id
                    }
                )

            if not user:

                continue

            if not user.get(
                "email"
            ):

                continue

            send_medication_email(
                user["email"],
                med["medicine"],
                med["dosage"]
            )

            # Save reminder date
            med_collection.update_one(
                {
                    "_id": med["_id"]
                },
                {
                    "$set": {
                        "last_reminded": today
                    }
                }
            )

            print(
                f"Reminder sent for {med['medicine']}"
            )

        except Exception as e:

            print(
                f"Reminder Error: {e}"
            )


scheduler = BackgroundScheduler()

scheduler.add_job(
    check_medications,
    "interval",
    minutes=1,
    id="medication_reminder"
)

scheduler.start()

print(
    "Medication Scheduler Started"
)