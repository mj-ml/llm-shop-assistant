import uuid
import time

import streamlit as st

from db_ops import save_feedback, save_conversation


def main():
    st.title("LLM e-shop assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is your question?"):
        query_id = str(uuid.uuid4())

        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history

        with st.spinner('Processing...'):
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = f"Echo: {prompt}"
                st.markdown(response)

                answer_data = {}
                answer_data["answer"] = response
                answer_data["model_used"] = 0
                answer_data["response_time"] = 0
                answer_data["relevance"] = "NONE"
                answer_data["relevance_explanation"] = "NONE"
                answer_data["prompt_tokens"] = 0
                answer_data["completion_tokens"] = 0
                answer_data["total_tokens"] = 0
                answer_data["eval_prompt_tokens"] = 0
                answer_data["eval_completion_tokens"] = 0
                answer_data["eval_total_tokens"] = 0
                answer_data["openai_cost"] = 0

                save_conversation(query_id, prompt, answer_data)
                save_feedback(query_id, 2)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.write("Was this response helpful?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes"):
                print("yes", flush=True)
                save_feedback(query_id, 1)

        with col2:
            if st.button("No"):
                save_feedback(query_id, 0)


def print_log(message):
    print(message, flush=True)


def main2():
    print_log("Starting the Course Assistant application")
    st.title("Course Assistant")

    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )
    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

    # Course selection
    # course = st.selectbox(
    #     "Select a course:",
    #     ["machine-learning-zoomcamp", "data-engineering-zoomcamp", "mlops-zoomcamp"],
    # )
    # print_log(f"User selected course: {course}")

    # Model selection
    # model_choice = st.selectbox(
    #     "Select a model:",
    #     ["ollama/phi3", "openai/gpt-3.5-turbo", "openai/gpt-4o", "openai/gpt-4o-mini"],
    # )
    # print_log(f"User selected model: {model_choice}")

    # Search type selection
    # search_type = st.radio("Select search type:", ["Text", "Vector"])
    # print_log(f"User selected search type: {search_type}")

    # User input
    user_input = st.text_input("Enter your question:")

    if st.button("Ask"):
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(f"User asked: '{user_input}'")
        with st.spinner("Processing..."):

            start_time = time.time()
            # answer_data = get_answer(user_input, course, model_choice, search_type)

            answer_data = {}
            answer_data["answer"] = user_input
            answer_data["model_used"] = 0
            answer_data["response_time"] = 0
            answer_data["relevance"] = "NONE"
            answer_data["relevance_explanation"] = "NONE"
            answer_data["prompt_tokens"] = 0
            answer_data["completion_tokens"] = 0
            answer_data["total_tokens"] = 0
            answer_data["eval_prompt_tokens"] = 0
            answer_data["eval_completion_tokens"] = 0
            answer_data["eval_total_tokens"] = 0
            answer_data["openai_cost"] = 0

            end_time = time.time()
            print_log(f"Answer received in {end_time - start_time:.2f} seconds")
            st.success("Completed!")
            st.write(answer_data["answer"])

            # Display monitoring information
            st.write(f"Response time: {answer_data['response_time']:.2f} seconds")
            st.write(f"Relevance: {answer_data['relevance']}")
            st.write(f"Model used: {answer_data['model_used']}")
            st.write(f"Total tokens: {answer_data['total_tokens']}")
            if answer_data["openai_cost"] > 0:
                st.write(f"OpenAI cost: ${answer_data['openai_cost']:.4f}")

            # Save conversation to database
            print_log("Saving conversation to database")
            save_conversation(
                st.session_state.conversation_id, user_input, answer_data,
            )
            print_log("Conversation saved successfully")
            # Generate a new conversation ID for next question

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1"):
            st.session_state.count += 1
            print_log(
                f"Positive feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, 1)
            print_log("Positive feedback saved to database")
    with col2:
        if st.button("-1"):
            st.session_state.count -= 1
            print_log(
                f"Negative feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, -1)
            print_log("Negative feedback saved to database")


if __name__ == "__main__":
    main2()
