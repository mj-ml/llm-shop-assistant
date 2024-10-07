# llm-shop-assistant
![assistant.jpg](img%2Fassistant.jpg)
# Project description

LLM based e-shop assistant providing help about the shop policies. Ask our shop assistant any question.

Example questions

- How much is shipping to Albania and how long does it take?
- How much is shipping to London and how long does it take? reply in French.
- Can I return if I changed my mind? I tried the product and it's not great. 

The models work well with most of bigger European languages (tested on EN/ES/FR/PL/CZ)

## How to run it?

Run docker compose up in the main directory.

```
docker compose up -d
```

logs are available 
```
docker compose logs -f 
```

To switch it off

```
docker compose down
```

The DBs are initialised in init.dockerfile which is run in the main docker compose.



## Dataset

I adapted
https://www.kaggle.com/datasets/saadmakhdoom/ecommerce-faq-chatbot-dataset?resource=download
by adding some additional questions.

# Technical description

## Ingestion

The ingestion is automated, when starting the app. 
`app/app_init.py`

If you want to modify the questions/answers please refer to the file
`data/questions.json`

Data is uploaded to elasticsearch in two formats:

- raw text
- vector using `SentenceTransformer("multi-qa-distilbert-cos-v1")`

## Retrieval

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

The selected vector query is

```
query = {
  "field": "text_vector",
  "query_vector": vector_search_term,
  "k": 5,
  "num_candidates": 100
}
```

## LLM

The chosen LLM is Mistral AI.
https://mistral.ai/

I included a token for the review. I will expire soon. Use responsibly. 

The token is stored in .env - if you want to change it. 

## User interface

Streamlit - click below to chat with the assistant: 

http://localhost:8501/

Don't forget to submit your feedback after each answer! 


![img.png](img%2Fimg.png)
## Metrics

The RAG was evaluated - the figure below shows the cosine similarity of the original answer and the LLM generated answer. 

The rag is also constantly evaluated using LLM-as-judge - after each question asked by the user.  

![img_3.png](img%2Fimg_3.png)

Metrics are stored in Postgres and shown in grafana with (5 charts).

After each run of the model there is a LLM model as a judge which evaluates the correctness of the answer (stored in the
db and visible in the dashboards)

Dashboards are created in the init.dockerfile. 

To see the dashboards: 

http://localhost:3000/

user: admin, password: admin

![img_1.png](img%2Fimg_1.png)

## Notebooks

Notebooks are stored in the directory notebooks

- inside you can find the evaluations
- basic examples
- RAG evaluation 

## Evaluation Criteria

* Problem description
  * 2 points: The problem is well-described and it's clear what problem the project solves
* RAG flow
  * 2 points: Both a knowledge base and an LLM are used in the RAG flow
* Retrieval evaluation
  * 2 points: Multiple retrieval approaches are evaluated, and the best one is used
* RAG evaluation
  * 1 point: Only one RAG approach (e.g., one prompt) is evaluated
* Interface
  * 2 points: UI (e.g., Streamlit), web application (e.g., Django), or an API (e.g., built with FastAPI)
* Ingestion pipeline
  * 2 points: Automated ingestion with a Python script or a special tool (e.g., Mage, dlt, Airflow, Prefect)
* Monitoring
  * 2 points: User feedback is collected and there's a dashboard with at least 5 charts
* Containerization
  * 2 points: Everything is in docker-compose
* Reproducibility
  * 2 points: Instructions are clear, the dataset is accessible, it's easy to run the code, and it works. The versions
    for all dependencies are specified.

* Best practices
  * [ ] Hybrid search: combining both text and vector search (at least evaluating it) (1 point)
  * [ ] Document re-ranking (1 point)
  * [ ] User query rewriting (1 point)
* Bonus points (not covered in the course)
  * [ ] Deployment to the cloud (2 points)
  * [ ] Up to 3 extra bonus points if you want to award for something extra (write in feedback for what)

