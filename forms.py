from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from app import app, db
from models import Account_Recovery

@app.route('/security_questions', methods=['GET', 'POST'])
def security_questions():
    # List of available questions (same as in the form)
    question_list = [
        "What was the name of your first pet?",
        "What is your mother’s maiden name?",
        "What was the model of your first car?",
        "What city were you born in?",
        "What is your favorite teacher’s name?"
    ]

    if request.method == 'POST':
        user_email = session.get('user_email')  # assuming the user is logged in
        if not user_email:
            flash("You must be logged in to set up recovery questions.", "warning")
            return redirect(url_for('login'))

        selected_questions = []
        answers = []

        # Loop through all 5 possible form fields
        for i in range(1, 6):
            q_text = request.form.get(f'question{i}')
            ans = request.form.get(f'answer{i}')

            # Only include filled ones
            if q_text and ans:
                selected_questions.append(q_text)
                answers.append(ans)

        # Must have exactly 3 selected questions
        if len(selected_questions) != 3:
            flash("Please select and answer exactly 3 security questions.", "danger")
            return redirect(url_for('security_questions'))

        # Store questions and hashed answers
        for q_text, ans in zip(selected_questions, answers):
            entry = Account_Recovery(
                UserEmail=user_email,
                QuestionText=q_text,
                AnswerHash=generate_password_hash(ans)
            )
            db.session.add(entry)

        db.session.commit()
        flash("Your security questions have been saved successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('security_questions.html', question_list=question_list)
