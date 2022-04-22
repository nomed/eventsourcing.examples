import os

#os.environ["PERSISTENCE_MODULE"] = "eventsourcing.sqlite"
#os.environ["SQLITE_DBNAME"] = ":memory:"
#os.environ["SQLITE_LOCK_TIMEOUT"] = "10"

from eventsourcing.system import SingleThreadedRunner, MultiThreadedRunner
from . import system
from .utils import set_runner, get_runner, set_logger
from .customers.application import Customers
from .levels.application import Levels

leaders = system.leaders
#assert leaders == ["Customers", "ProcessCustomers", "Levels", "ProcessLevels"]
followers = system.followers
#assert followers == ["ProcessCustomers", "ProcessLevels"]
processors = system.processors
#assert processors == ["ProcessCustomers", "ProcessLevels"]
#runner = MultiThreadedRunner(system)
#runner.start()
runner = set_runner(system)
logger = set_logger(system)
customers = runner.get(Customers)
from random import random

suffix = str(random())
logger.info("Adding customer")
customer = customers.register_customer(f"testme {random}")
logger.info(f"Added customer with customer_id: {customer.id}")

levels = runner.get(Levels)
logger.info("Adding level")
level = levels.register_level(f"bronze {random}")
logger.info(f"Added level with level_id: {level.id}")

logger.info(f"Adding {(customer.id, level.id)} to CustomerLevelIndex")
customers.add_level_to_customer(customer.id, level.id)
customer_levels_index = customers._get_customer_levels_index(customer.id)
assert customer_levels_index.level_ids == [level.id]
logger.info(
    f"Added customer to level with level_customer_index._id: {customer_levels_index.id}"
)
"""
print("START"+"="*60+"Add Customer to Level")
levels.add_customer_to_level(level_id, customer_id)
level_bronze = levels._get_level_by_id(level_id)
level_customers_index = levels._get_level_customers_index(level_id)
assert level_customers_index.customer_ids == [customer_id]
print("END"+"="*60+"Add Customer to Level")

customer_id2 = customers.register_customer(f"testme2 {random}")
customers.add_level_to_customer(customer_id2, level_id)
customer_levels_index = customers._get_customer_levels_index(customer_id2)
assert customer_levels_index.level_ids == [level_id]
level_bronze = levels._get_level_by_id(level_id)
levels.add_customer_to_level(level_id, customer_id2)
level_customers_index = levels._get_level_customers_index(level_id)
assert level_customers_index.customer_ids == [customer_id, customer_id2]
level_bronze = levels._get_level_by_id(level_id)
"""
proceed = True
while proceed:

    for key, val in runner.processing_queues.items():
        if not val.empty():
            proceed = True
        else:
            proceed = False

print("END")