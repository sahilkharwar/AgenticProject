from plyer import notification


def send_medication_notification(
    medicine,
    dosage
):

    notification.notify(
        title="Medication Reminder",
        message=f"Time to take {medicine} ({dosage})",
        timeout=10
    )