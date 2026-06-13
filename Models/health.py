def calculate_health_assessment(
    bmi,
    total_calories,
    goal_progress
):

    # ==========================
    # HEALTH SCORE
    # ==========================

    health_score = 100

    score_breakdown = []

    # BMI Assessment

    if bmi >= 30:

        health_score -= 30

        score_breakdown.append(
            "Obese BMI: -30"
        )

    elif bmi >= 25:

        health_score -= 15

        score_breakdown.append(
            "Overweight BMI: -15"
        )

    elif bmi > 0:

        score_breakdown.append(
            "Healthy BMI: +0"
        )

    # Activity Assessment

    if total_calories < 500:

        health_score -= 15

        score_breakdown.append(
            "Low Activity: -15"
        )

    elif total_calories >= 1000:

        score_breakdown.append(
            "Active Lifestyle: +0"
        )

    # Goal Assessment

    if goal_progress < 50:

        health_score -= 10

        score_breakdown.append(
            "Goal Progress Below 50%: -10"
        )

    elif goal_progress >= 100:

        score_breakdown.append(
            "Goal Achieved: +0"
        )

    # Final Limits

    health_score = max(
        0,
        min(
            health_score,
            100
        )
    )

    # ==========================
    # RISK LEVEL
    # ==========================

    if health_score >= 85:

        health_risk = "Low Risk"

    elif health_score >= 60:

        health_risk = "Moderate Risk"

    else:

        health_risk = "High Risk"

    # ==========================
    # RECOMMENDATION
    # ==========================

    if bmi >= 30:

        recommendation = (
            "Your BMI is in the obese range. Focus on weight management through regular exercise, portion control and healthy nutrition."
        )

    elif bmi >= 25:

        recommendation = (
            "Your BMI is above the healthy range. Increase physical activity and maintain a balanced diet."
        )

    elif goal_progress < 50:

        recommendation = (
            "You are below 50% of your daily goal. Try increasing your activity level to improve overall fitness."
        )

    elif total_calories < 500:

        recommendation = (
            "Your activity level is low. Aim for more consistent exercise throughout the week."
        )

    else:

        recommendation = (
            "Excellent health status. Continue maintaining your current healthy habits and fitness routine."
        )

    return {
        "health_score": health_score,
        "health_risk": health_risk,
        "recommendation": recommendation,
        "score_breakdown": score_breakdown
    }