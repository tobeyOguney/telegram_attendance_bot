# wsgi.py
from manage import app as application

import logging
    from logging import StreamHandler
    file_handler = StreamHandler()
    file_handler.setLevel(logging.WARNING)
    application.logger.addHandler(file_handler)

if __name__ == "__main__":
    application.run()
