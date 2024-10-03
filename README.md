# llm-shop-assistant

# Project description

LLM based e-shop assistant providing help about the shop policies. Ask our shop assistant any question.

## How to run it?

Run docker compose up in the main directory. 

```
docker compose up -d
```

To swich it off

```
docker compose down
```


## Dataset

I adapted
https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset?resource=download
by adding some additional questions.

# Technical description

## Retrieval

An adapted FAQ is uploaded to elasticsearch in two formats:

- raw text
- vector using `SentenceTransformer("multi-qa-distilbert-cos-v1")`

Two attempts to the evaluation are done

- using text search
- using semantic search.

The semantic search is superior therefore selected for the rest of the project.
Results below.

```
+-----+-----------------------+-------------+------------------+----------+
|     |hit_rate_results_vector|hit_rate_text|mrr_results_vector|mrr_text  |
+-----+-----------------------+-------------+------------------+----------+
|count|400.000000             |400.000000   |400.000000        |400.000000|
|mean |0.940000               |0.847500     |0.832292          |0.709333  |
|std  |0.237784               |0.359955     |0.311742          |0.393253  |
+-----+-----------------------+-------------+------------------+----------+

```

## LLM

The chosen LLM is Mistral AI.
https://mistral.ai/

I included a token for the review. I will expire soon. Use responisibly :D 
The token is stored in .env - if for any reasons it does not work. 

## User interface

Streamlit - click below to chat with the assistant. 

http://localhost:8501/

## Metrics

Metrics are stored in Postgres and shown in grafana.

http://localhost:3000/

## Notebooks 

Notebooks 

## Evaluation Criteria

* Problem description
    * 0 points: The problem is not described
    * 1 point: The problem is described but briefly or unclearly
    * 2 points: The problem is well-described and it's clear what problem the project solves
* RAG flow
    * 0 points: No knowledge base or LLM is used
    * 1 point: No knowledge base is used, and the LLM is queried directly
    * 2 points: Both a knowledge base and an LLM are used in the RAG flow
* Retrieval evaluation
    * 0 points: No evaluation of retrieval is provided
    * 1 point: Only one retrieval approach is evaluated
    * 2 points: Multiple retrieval approaches are evaluated, and the best one is used
* RAG evaluation
    * 0 points: No evaluation of RAG is provided
    * 1 point: Only one RAG approach (e.g., one prompt) is evaluated
    * 2 points: Multiple RAG approaches are evaluated, and the best one is used
* Interface
    * 0 points: No way to interact with the application at all
    * 1 point: Command line interface, a script, or a Jupyter notebook
    * 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI)
* Ingestion pipeline
    * 0 points: No ingestion
    * 1 point: Semi-automated ingestion of the dataset into the knowledge base, e.g., with a Jupyter notebook
    * 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)
* Monitoring
    * 0 points: No monitoring
    * 1 point: User feedback is collected OR there's a monitoring dashboard
    * 2 points: User feedback is collected and there's a dashboard with at least 5 charts
* Containerization
    * 0 points: No containerization
    * 1 point: Dockerfile is provided for the main application OR there's a docker-compose for the dependencies only
    * 2 points: Everything is in docker-compose
* Reproducibility
    * 0 points: No instructions on how to run the code, the data is missing, or it's unclear how to access it
    * 1 point: Some instructions are provided but are incomplete, OR instructions are clear and complete, the code
      works, but the data is missing
    * 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions
      for all dependencies are specified.
* Best practices
    * [ ] Hybrid search: combining both text and vector search (at least evaluating it) (1 point)
    * [ ] Document re-ranking (1 point)
    * [ ] User query rewriting (1 point)
* Bonus points (not covered in the course)
    * [ ] Deployment to the cloud (2 points)
    * [ ] Up to 3 extra bonus points if you want to award for something extra (write in feedback for what)

