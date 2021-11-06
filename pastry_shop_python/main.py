# Four Pilars of Object-Oriented Programming
# 1) Abstraction
# 2) Inheritance
# 3) Encapsulation 
# 4) Polymorphism  

from __future__ import annotations
from abc import ABC, abstractmethod, abstractproperty
from typing import Dict, List

class Item(ABC):
    @abstractmethod
    def get_cost():
        pass

class Pastry(Item):
    def __init__(self, name:str, weight:int = 0, cost: float = 0.0) -> None:
        self.name = name
        self.cost = cost
        self.weight = weight

    def get_cost(self) -> float:
        return self.cost

    def __str__(self) -> str:
        return f'{self.name} weighting {self.weight}g and costing ${self.cost} to bake.'

class Beverage(Item):
    def __init__(self, name:str, capacity: int = 0, cost:float = 0) -> None:
        self.name = name
        self.cost = cost
        self.capacity = capacity

    def get_cost(self) -> float:
        return self.cost

    def __str__(self) -> str:
        return f'{self.name} with capacity of {self.capacity}ml costing ${self.cost} to brew.'

    def __add__(self, other: Beverage) -> Beverage:
        return Beverage(self.name + '_with_' + other.name, self.capacity + other.capacity, self.cost + other.cost)
 
class PastryShop():
    def __init__(self, funds:float=0.0, margin:float=0.2) -> None:
        self.items: Dict[str,List[Item]] = {}
        self.funds = funds
        self.margin = margin

    def get_funds(self) -> float:
        return self.funds

    def get_items(self):
        return self.items

    def bake_or_brew(self, i: Item) -> None:
        if self.funds >= i.cost:
            if i.name in self.items:
                self.items[i.name].append(i)
                self.funds -= i.cost
            else:
                self.items[i.name] = [i]  
                self.funds -= i.cost

    def sell(self, item_name: str) -> None:
        if item_name in self.items:
            if len(self.items[item_name]) > 0:
                item = self.items[item_name].pop()
                self.funds += (1 + self.margin)*item.get_cost()

#i: Item = Item()
croissant: Pastry = Pastry("Croissant", weight=100, cost=1.0)
coffee: Beverage  = Beverage("Coffee", capacity=10, cost =0.5)
milk: Beverage = Beverage("Milk", capacity=20, cost=0.5)
c_w_m: Beverage = coffee + milk

items: List[Item] = [croissant, coffee, milk, c_w_m]

for p in items:
    print(p)

myShop = PastryShop(100,0.2)
print(myShop.get_funds())
myShop.bake_or_brew(Pastry("Croissant", weight=100, cost=1.0))
myShop.bake_or_brew(Beverage("Coffee", capacity=10, cost=0.5))
print(myShop.get_funds())
myShop.sell("Croissant")
myShop.sell("Coffee")
print(myShop.get_funds())