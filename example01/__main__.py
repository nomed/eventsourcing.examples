import os
#os.environ["PERSISTENCE_MODULE"] = "eventsourcing.sqlite"
#os.environ["SQLITE_DBNAME"] = ":memory:"
#os.environ["SQLITE_LOCK_TIMEOUT"] = "10"
import datetime
from eventsourcing.system import SingleThreadedRunner, MultiThreadedRunner
from . import system
from .utils import set_runner, get_runner, set_logger
from .customers.application import Customers
from .customers.domainmodel import CustomerLevelsIndex
from .levels.application import Levels
from .levels.domainmodel import LevelCustomersIndex
from .processor import ProcessApps


def get_ms(a, b):
    return (a - b).total_seconds() * 1000


leaders = system.leaders
assert leaders == ["Customers", "Levels", "ProcessApps"]
followers = system.followers
assert followers == ["ProcessApps"]
processors = system.processors
assert processors == ["ProcessApps"]

runner = set_runner(system)
logger = set_logger(system)
customers = runner.get(Customers)
from random import random

# Add level
levels = runner.get(Levels)
logger.info("Adding level")
level = levels.register_level(f"bronze {random}")
logger.info(f"Added level with id: {level.id}")

# Add customer1
suffix = str(random())
logger.info("Adding customer1")
customer1 = customers.register_customer(f"testme {random}")
logger.info(f"Added customer with id: {customer1.id}")

#

# Add level to customer1 index
logger.info(f"Adding {(customer1.id, level.id)} to CustomerLevelIndex")
customers.add_level_to_customer(customer1.id, level.id)
step01 = datetime.datetime.now()
while True:
    try:
        customer_levels_index = customers._get_customer_levels_index(
            customer1.id)
        break
    except:
        pass
step02 = datetime.datetime.now()
logger.info(f"Added {(customer1.id, level.id)} to CustomerLevelIndex")
logger.info(
    f"=====> {get_ms(step02,step01)}s to create {customer_levels_index}")
assert customer_levels_index.level_ids == [level.id]

#Check if also customer1 has been added to level index
logger.info(
    f"Checking {(level.id, customer1.id)} to LevelCustomersIndex has been added by process"
)
while True:
    try:
        level_customers_index = levels._get_level_customers_index(level.id)
        break
    except:
        pass
step03 = datetime.datetime.now()
logger.info(f"Adding {(customer1.id, level.id)} to CustomerLevelIndex")
logger.info(
    f"=====> {get_ms(step03,step01)}s to create {level_customers_index}")
assert level_customers_index.customer_ids == [customer1.id]

# Add customer2
suffix = str(random())
logger.info("Adding customer1")
customer2 = customers.register_customer(f"testme {random}")
logger.info(f"Added customer with id: {customer1.id}")

# Add level to customer1 index
logger.info(f"Adding {(customer2.id, level.id)} to CustomerLevelIndex")
customers.add_level_to_customer(customer2.id, level.id)
step01 = datetime.datetime.now()
while True:
    try:
        customer_levels_index = customers._get_customer_levels_index(
            customer2.id)
        break
    except:
        pass
step02 = datetime.datetime.now()
logger.info(f"Added {(customer2.id, level.id)} to CustomerLevelIndex")
logger.info(
    f"=====> {get_ms(step02,step01)}s to create {customer_levels_index}")
assert customer_levels_index.level_ids == [level.id]

#Check if also customer2 has been added to level index
logger.info(
    f"Checking {(level.id, customer2.id)} to LevelCustomersIndex has been added by process"
)
while True:
    try:
        levels = runner.get(Levels)
        level_customers_index = levels._get_level_customers_index(level.id)
        break
    except:
        pass
step03 = datetime.datetime.now()
logger.info(
    f"Checked {(customer2.id, level.id)} to LevelCustomersIndex has been added by process"
)
logger.info(
    f"=====> {get_ms(step03,step01)}s to create {level_customers_index}")
assert level_customers_index.customer_ids == [customer1.id, customer2.id]
level_bronze = levels._get_level_by_id(level.id)
assert level_bronze.customer_count == 2
#proceed = True
#while proceed:
#    for key, val in runner.processing_queues.items():
#        if not val.empty():
#            proceed = True
#        else:
#            proceed = False

print("END")