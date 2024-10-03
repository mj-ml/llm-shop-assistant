import time
import uuid

import streamlit as st


def log(message):
    print(message, flush=True)


def main():
    st.title("E-shop LLM Assistant")

    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )

    # User input
    user_question = st.text_input("Enter your question:")

    if st.button("Ask"):
        st.session_state.conversation_id = str(uuid.uuid4())
        log(f"User asked: '{user_question}'")
        with st.spinner("Processing..."):
            start_time = time.time()

            answer_data = {}
            answer_data["answer"] = user_question
            answer_data["model_used"] = "mistral-small-2409"
            answer_data["response_time"] = 0
            answer_data["relevance"] = None
            answer_data["relevance_explanation"] = None
            answer_data["prompt_tokens"] = 0
            answer_data["completion_tokens"] = 0
            answer_data["total_tokens"] = 0
            answer_data["eval_prompt_tokens"] = 0
            answer_data["eval_completion_tokens"] = 0
            answer_data["eval_total_tokens"] = 0
            answer_data["openai_cost"] = 0

            end_time = time.time()
            log(
                f"Answer received in {end_time - start_time:.2f} seconds"
            )
            st.success("Completed!")
            st.write(answer_data["answer"])

            # Display monitoring information
            st.write(
                f"Response time: {answer_data['response_time']:.2f} seconds"
            )
            st.write(f"Relevance: {answer_data['relevance']}")
            st.write(f"Model used: {answer_data['model_used']}")
            st.write(f"Total tokens: {answer_data['total_tokens']}")
            if answer_data["openai_cost"] > 0:
                st.write(
                    f"OpenAI cost: ${answer_data['openai_cost']:.4f}"
                )

            # Save conversation to database
            log("Saving conversation to database")

            log("Conversation saved successfully")

    # Feedback buttons
    col1, col2, _ = st.columns([1, 1, 8])
    with col1:
        if st.button("👍 Yes"):
            log("Positive feedback received.")
            log("Positive feedback saved to database")
    with col2:
        if st.button("👎 No"):
            log("Negative feedback received")


if __name__ == "__main__":
    main()
