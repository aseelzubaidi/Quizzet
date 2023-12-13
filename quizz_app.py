import openai
import langchain
import streamlit as st

openai.api_key = "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"

def generate_quiz_data(topic, num_questions):
    quiz_data = []

    for _ in range(num_questions):
        prompt = f"Generate a quiz question and answer options about {topic}"
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question, options = extract_question_and_options(response.choices[0].text.strip())

        quiz_data.append({"question": question, "options": options})

    return quiz_data

def extract_question_and_options(response_text):

    lines = response_text.split("\n")
    
    question = lines[0]
    
    options = [option for option in lines[1:] if option.strip() and '?' not in option]

    return question, options

def main():
    st.set_page_config(
        page_title="MCQ Quiz App",
        page_icon=":bulb:",
        layout="wide",
        initial_sidebar_state="collapsed",
    )

    st.markdown(
        """
        <style>
        body {
            color: #333;
            background-color: #f0f0f0;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.image("logo.png", width=150)  # Replace "your_logo.png" with your logo image file
    st.title("MCQ Quiz Application")

    topic = st.text_input("Enter your preferred quiz topic:")

    if topic:
        num_questions = st.number_input("Number of questions:", min_value=1, step=1, value=2)

        @st.cache(allow_output_mutation=True)
        def load_quiz_data():
            return generate_quiz_data(topic, num_questions)

        quiz_data = load_quiz_data()

        st.write(f"Quiz for {topic}")
        user_answers = []

        for i, question_data in enumerate(quiz_data):
            question = question_data["question"]
            options = question_data["options"]

            st.write(f"\n**Question {i + 1}:** {question}")
            user_answer = st.radio(f"Select Your Answer {i + 1}:", options, key=f"question_{i}")
            user_answers.append(user_answer)

        submit_button = st.button("Submit Quiz")

        if submit_button:
            score = 0
            for i, question_data in enumerate(quiz_data):
                correct_answer = question_data["options"][0]
                if user_answers[i] == correct_answer:
                    score += 1

            st.write(f"Final Score: {score}/{len(quiz_data)}")

            st.write("Correct Answers:")
            for i, question_data in enumerate(quiz_data):
                st.write(f"Question {i + 1}: {question_data['options'][0]}")
    else:
        st.write("Enter Topic Name To Generate Quiz Questions")

if __name__ == "__main__":
    main()
