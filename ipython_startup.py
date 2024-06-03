from IPython import get_ipython

from src.db.db_init import async_session
from src.server import startup_event  # noqa: F401

ipython = get_ipython()


session = async_session()
ipython.run_cell('await(startup_event())')
