from eventsourcing.system import System
from .processor import ProcessApps
from .customers.application import Customers
from .levels.application import Levels
from eventsourcing.system import SingleThreadedRunner, MultiThreadedRunner

pipes = [[Customers, ProcessApps], [Levels, ProcessApps],
         [ProcessApps, ProcessApps]]
system = System(pipes=pipes)
