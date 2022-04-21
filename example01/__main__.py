from eventsourcing.system import SingleThreadedRunner
from .customers.application import Customers
from .levels.application import Levels
from . import system

runner = SingleThreadedRunner(system)
runner.start()

customers = runner.get(Customers)
customer_id = customers.register_customer("testme")
levels = runner.get(Levels)
level_id = levels.register_level("bronze")

customers.add_level_to_customer(customer_id, level_id)


