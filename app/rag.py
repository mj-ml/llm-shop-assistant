import json
import os
import time

from mistralai import Mistral

from db_ops import query_elasticsearch
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("MISTRAL_KEY", "MISTRAL")
model = "mistral-small-2409"

def get_context(question):
    raw_context = query_elasticsearch(question)
    context = preprocess_context(raw_context)

    return context


def preprocess_context(raw_context):
    s = ""
    for c in raw_context:
        s += c["_source"]["answer"]

    return s


def generate_answer(question, context):
    client = Mistral(api_key=api_key)

    prompt = f"""

    You are a shop assistant. Reply briefly. Give a simple explanation. 
    Given the context information and not prior knowledge, answer the query. 
    Query: 
   ```
    {question}
   ```
    Context:     
    ```
    {context}
    ```
    Answer:
    """
    print(prompt)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    ans = chat_response.choices[0].message.content
    print(ans)
    return ans, chat_response


def evaluate_answer(question, answer):
    prompt_template = """
        You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
        Your task is to analyze the relevance of the generated answer to the given question.
        Based on the relevance of the generated answer, you will classify it
        as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

        Here is the data for evaluation:

        Question: {question}
        Generated Answer: {answer}

        Please analyze the content and context of the generated answer in relation to the question
        and provide your evaluation in parsable JSON without using code blocks:

        {{
          "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
          "Explanation": "[Provide a brief explanation for your evaluation]"
        }}
        """.strip()
    client = Mistral(api_key=api_key)

    prompt_eval = prompt_template.format(
        question=question, answer=answer
    )
    chat_response_eval = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt_eval,
            },
        ],
    )
    eval_ans = chat_response_eval.choices[0].message.content
    print(eval_ans)
    return json.loads(eval_ans), chat_response_eval


if __name__ == "__main__":
    question = "How much in shipping to France?"
    context = get_context(question)
    mistral_ans, raw_ans = generate_answer(
        question=question,
        context=context,
    )
    time.sleep(5)
    mistral_eval, raw_eval = evaluate_answer(
        question=question,
        answer=mistral_ans,
    )
