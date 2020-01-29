import os

# uncomment the line below for postgres database url from environment variable
postgres_local_base = 'postgres://pmugszllgbknve:63a9d53d96975aaf26dabd40910ecd7e01cccd2d3bb21217b33ce3f9be2e663b@ec2-3-214-53-225.compute-1.amazonaws.com:5432/dd7v111bie2hh9'

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = True

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config_by_name = dict(
    dev=DevelopmentConfig
)

key = Config.SECRET_KEY
