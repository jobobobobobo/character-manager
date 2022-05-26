from dice import dice_pool, dice_roll, d6_pool, Die
from functools import reduce
from interfaces import Rollable
# import math
from random import sample
# import csv

class Characteristic(Rollable):
    def __init__(self, name, short_name=None, score=0, rules=None):
        if short_name == None:
           self.short_name = name[0:3]
        super().__init__(name, score)
        self.short_name = short_name.upper()

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}
    
    def __str__(self):
        msg = f"{self.short_name}: {self.score:>2}"
        return msg
    def __repr__(self):
        msg = f"{self.short_name}: {self.score:>2}"
        return msg

if __name__ == "__main__":
    stat_block = (
        Characteristic("Strength", "STR", dice_roll(d6_pool(3)) * 5),
        Characteristic("Constitution", "CON", dice_roll(d6_pool(3)) * 5),
        Characteristic("Size", "SIZ", dice_roll(d6_pool(2),6) * 5),
        Characteristic("Dexterity", "DEX", dice_roll(d6_pool(3)) * 5),
        Characteristic("Appearance", "APP", dice_roll(d6_pool(3)) * 5),
        Characteristic("Intelligence", "INT", dice_roll(d6_pool(2),6) * 5),
        Characteristic("Power", "POW", dice_roll(d6_pool(3)) * 5),
        Characteristic("Education", "EDU", dice_roll(d6_pool(2),6) * 5),
        Characteristic("Luck", "LUK", dice_roll(d6_pool(3)) * 5)
    )
    for attribute in stat_block:
        print(attribute)