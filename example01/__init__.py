from eventsourcing.system import System
from .customers.application import Customers, ProcessCustomers
from .levels.application import Levels, ProcessLevels

pipes = [[Customers, ProcessCustomers], [Levels, ProcessLevels],
         [Customers, ProcessLevels], [Levels, ProcessCustomers],
         [ProcessLevels]]
system = System(pipes=pipes)
