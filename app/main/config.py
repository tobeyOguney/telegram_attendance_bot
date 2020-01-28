import os


# postgres_params = {
#     'NAME': os.environ['RDS_DB_NAME'],
#     'USER': os.environ['RDS_USERNAME'],
#     'PASSWORD': os.environ['RDS_PASSWORD'],
#     'HOST': os.environ['RDS_HOSTNAME'],
#     'PORT': os.environ['RDS_PORT'],
# }

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = "postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}".format(**postgres_params)

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = True

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_main.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT=8080

    import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)


config_by_name = dict(
    dev=DevelopmentConfig
)

key = Config.SECRET_KEY
