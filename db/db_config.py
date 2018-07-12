import os


class DatabaseConfig:
    db_string_main = 'postgresql://{}:{}@{}:{}/{}'
    db_string = db_string_main.format(os.environ.get('PG_USER', None) or "postgres",
                                      os.environ.get('PG_PASS', None) or "ehsan1379",
                                      os.environ.get('PG_HOST', None) or "localhost",
                                      os.environ.get('PG_PORT', None) or "5432",
                                      os.environ.get('PG_DB_NAME', None) or "twitter")
