# -*- coding: utf-8 -*-
from typing import Any, Dict, List, Optional, cast
from uuid import NAMESPACE_URL, UUID, uuid5
from eventsourcing.application import Application, AggregateNotFound
from eventsourcing.system import ProcessApplication
from eventsourcing.dispatch import singledispatchmethod
from .domainmodel import Customer, CustomerLevelsIndex
from ..levels.domainmodel import LevelCustomersIndex


class Customers(Application):
    def register_customer(self, login: str):
        customer = Customer(login)
        self.save(customer)
        return customer.id

    def add_level_to_customer(self, customer_id: UUID, level_id: UUID):
        try:
            customer_levels_index = self._get_customer_levels_index(
                customer_id)
        except AggregateNotFound:
            customer_levels_index = CustomerLevelsIndex(customer_id, [])
        if level_id not in customer_levels_index.ref:
            customer_levels_index.add_ref(customer_id, level_id)
            recordings = self.save(customer_levels_index)
        return customer_id

    def _get_customer_levels_index(self,
                                   customer_id: UUID) -> CustomerLevelsIndex:
        return cast(
            CustomerLevelsIndex,
            self.repository.get(CustomerLevelsIndex.create_id(customer_id)))


class ProcessCustomers(ProcessApplication):
    @singledispatchmethod
    def policy(self, domain_event, process_event):
        """Default policy"""

    @policy.register(CustomerLevelsIndex.CustomerLevelsRefAdded)
    def _(self, domain_event, process_event):
        """
        try:
            level_customers_index_id = LevelCustomersIndex.create_id(
                domain_event.ref)
            level_customers_index = self.repository.get(
                level_customers_index_id)
        except AggregateNotFound:
            level_customers_index = LevelCustomersIndex(domain_event.ref, )
        level_customers_index.add_ref(domain_event.ref,
                                      domain_event.customer_id)
        self.save(level_customers_index)
        """