from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask_health_assistant(
    profile,
    fitness_data,
    medications,
    chat_history,
    question,
    health_score=0,
    streak=0,
    daily_goal=0,
    goal_progress=0,
    today_steps=0,
    achievements=None,
    health_risk="Unknown",
    recommendation="",
    score_breakdown=None
):

    if achievements is None:

        achievements = []

    if score_breakdown is None:

        score_breakdown = []

    # ==========================
    # CHAT CONTEXT
    # ==========================

    conversation_context = ""

    for message in chat_history:

        role = message.get(
            "role",
            "user"
        )

        content = message.get(
            "content",
            ""
        )

        conversation_context += (
            f"{role}: {content}\n"
        )

    # ==========================
    # BMI CALCULATION
    # ==========================

    height_feet = profile.get(
        "height_feet",
        0
    )

    height_inches = profile.get(
        "height_inches",
        0
    )

    weight = profile.get(
        "weight",
        0
    )

    total_inches = (
        height_feet * 12
    ) + height_inches

    height_meters = (
        total_inches * 2.54
    ) / 100

    bmi = None

    if (
        height_meters > 0
        and
        weight > 0
    ):

        bmi = round(
            weight /
            (
                height_meters ** 2
            ),
            1
        )

    # ==========================
    # REDUCE TOKEN USAGE
    # ==========================

    fitness_summary = (
        fitness_data[-20:]
        if len(fitness_data) > 20
        else fitness_data
    )

    medication_summary = (
        medications[:20]
        if len(medications) > 20
        else medications
    )

    # ==========================
    # SYSTEM PROMPT
    # ==========================

    system_prompt = """
You are an advanced AI Health Assistant.

Responsibilities:

- Analyze BMI, fitness records, medications and health trends.
- Analyze goals, streaks and achievements.
- Provide personalized recommendations.
- Explain information clearly.
- Motivate users to maintain healthy habits.
- Use previous conversation context.
- Be concise but informative.
- Use bullet points whenever useful.

Medical Safety Rules:

- Never diagnose diseases.
- Never prescribe medications.
- Never claim to be a licensed doctor.
- Recommend consulting a healthcare professional for medical concerns.
- Use the user's health score, risk level and goals when giving advice.
- If goal progress is low, encourage improvement.
- If BMI is high, suggest weight-management strategies.
- If BMI is low, suggest healthy nutrition and strength-building activities.
- Focus on wellness, consistency and healthy habits.
"""

    # ==========================
    # USER PROMPT
    # ==========================

    user_prompt = f"""
User Profile

Username:
{profile.get("username")}

Age:
{profile.get("age")}

Height:
{height_feet} feet {height_inches} inches

Weight:
{weight} kg

BMI:
{bmi}

Health Score:
{health_score}/100

Health Score Breakdown:
{score_breakdown}

Health Risk:
{health_risk}

Current Streak:
{streak} days

Daily Goal:
{daily_goal}

Today's Steps:
{today_steps}

Goal Progress:
{goal_progress}%

Achievements:
{achievements}

Recommendation:
{recommendation}

Recent Fitness Records:
{fitness_summary}

Medication Records:
{medication_summary}

Previous Conversation:
{conversation_context}

Current Question:
{question}
"""

    # ==========================
    # GROQ REQUEST
    # ==========================

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0.4,
        max_tokens=1200
    )

    return (
        response
        .choices[0]
        .message.content
    )


# ==========================
# MEDICATION INTERACTION CHECKER
# ==========================

def check_medication_interactions(
    medications
):

    if not medications:

        return (
            "No medications available to analyze."
        )

    medicine_list = []

    for med in medications:

        medicine_list.append(
            med.get(
                "medicine",
                ""
            )
        )

    prompt = f"""
You are a medication interaction checker.

Medications:

{medicine_list}

Analyze:

1. Possible drug interactions
2. Risk Level (Low / Moderate / High)
3. Common side effects
4. Important precautions
5. Recommendations

Keep the response simple and easy to understand.

Always mention that users should consult a healthcare professional before making medication decisions.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
        max_tokens=700
    )

    return (
        response
        .choices[0]
        .message.content
    )