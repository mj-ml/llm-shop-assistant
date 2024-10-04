from db_ops import create_postgres_tables, init_elasticsearch, upload_knowledge_base
from grafana_init import grafana_init

if __name__ == '__main__':
    print('init postgres')
    create_postgres_tables()

    print('init elastic search')
    init_elasticsearch()

    print('upload knowledge base')
    upload_knowledge_base()

    print('init grafana')
    grafana_init()