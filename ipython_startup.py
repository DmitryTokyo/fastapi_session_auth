from IPython import get_ipython

from src.db.db_init import async_session

ipython = get_ipython()


session = async_session()
ipython.run_cell('await(startup_event())')
