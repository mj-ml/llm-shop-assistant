import hashlib
import os
from datetime import datetime

import psycopg2
from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("multi-qa-distilbert-cos-v1")
ELASTIC_URL = os.getenv("ELASTIC_URL", "http://localhost:9200")
es_client = Elasticsearch(ELASTIC_URL)

index_name = "faq"


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        database=os.getenv("POSTGRES_DB", "assistant"),
        user=os.getenv("POSTGRES_USER", "your_username"),
        password=os.getenv("POSTGRES_PASSWORD", "your_password"),
    )


def create_postgres_tables():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE if not exists conversations (
                    id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    response_time FLOAT NOT NULL,
                    relevance TEXT NOT NULL,
                    relevance_explanation TEXT NOT NULL,
                    prompt_tokens INTEGER NOT NULL,
                    completion_tokens INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    eval_prompt_tokens INTEGER NOT NULL,
                    eval_completion_tokens INTEGER NOT NULL,
                    eval_total_tokens INTEGER NOT NULL,
                    openai_cost FLOAT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """
            )
            cur.execute(
                """
                CREATE TABLE if not exists feedback (
                    id SERIAL PRIMARY KEY,
                    conversation_id TEXT REFERENCES conversations(id),
                    feedback INTEGER NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE NOT NULL
                )
            """
            )
        conn.commit()
    finally:
        conn.close()


def save_feedback(conversation_id, feedback, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO feedback (conversation_id, feedback, timestamp) VALUES (%s, %s, COALESCE(%s, CURRENT_TIMESTAMP))",
                (conversation_id, feedback, timestamp),
            )
        conn.commit()
    finally:
        conn.close()


def save_conversation(
    conversation_id, question, answer_data, timestamp=None
):
    if timestamp is None:
        timestamp = datetime.now()

    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO conversations 
                (id, question, answer, model_used, response_time, relevance, 
                relevance_explanation, prompt_tokens, completion_tokens, total_tokens, 
                eval_prompt_tokens, eval_completion_tokens, eval_total_tokens, openai_cost, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    conversation_id,
                    question,
                    answer_data["answer"],
                    answer_data["model_used"],
                    answer_data["response_time"],
                    answer_data["relevance"],
                    answer_data["relevance_explanation"],
                    answer_data["prompt_tokens"],
                    answer_data["completion_tokens"],
                    answer_data["total_tokens"],
                    answer_data["eval_prompt_tokens"],
                    answer_data["eval_completion_tokens"],
                    answer_data["eval_total_tokens"],
                    answer_data["openai_cost"],
                    timestamp,
                ),
            )
        conn.commit()
    finally:
        conn.close()


def query_elasticsearch(search_term):
    vector_search_term = model.encode(search_term)

    query = {
        "field": "text_vector",
        "query_vector": vector_search_term,
        "k": 5,
        "num_candidates": 100,
    }

    res = es_client.search(
        index=index_name,
        knn=query,
        source=["answer", "question", "doc_id"],
    )
    return res["hits"]["hits"]


def init_elasticsearch():
    index_settings = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {
                "answer": {"type": "text"},
                "question": {"type": "text"},
                "doc_id": {"type": "text"},
                "text_vector": {
                    "type": "dense_vector",
                    "dims": 768,
                    "index": True,
                    "similarity": "cosine",
                },
            }
        },
    }

    es_client.indices.delete(
        index=index_name, ignore_unavailable=True
    )
    es_client.indices.create(index=index_name, body=index_settings)


def generate_document_id(doc):
    combined = f"{doc['question']}-{doc['answer'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id


def upload_knowledge_base():
    questions_path = "questions.json"
    import json

    with open(questions_path, "r") as file:
        questions = json.load(file)

    documents = []

    for question in questions["questions"]:
        question["text_vector"] = model.encode(
            question["answer"]
        ).tolist()
        question["doc_id"] = generate_document_id(question)
        documents.append(question)

    for doc in documents:
        try:
            es_client.index(index=index_name, document=doc)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    context = query_elasticsearch("shipping price to Albania?")
