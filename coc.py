from dice import dice_pool, dice_roll, d6_pool, Die
from functools import reduce
from math import ceil
import csv


class Skill(object):
    def __init__(self, name, score, check=False, rules=None, important=False):
        self.name = name
        self.score = score
        self.check = check
        self.rules = rules
        self.important = important

    def points(self):
        return self.score

    def check(self, roll):
        if check == True:
            if roll > score:
                self.score += Die(6).result

    def roll(self):
        result = Die(100).result
        outcome = True if (result <= self.score) else False
        if outcome is True:
            self.check = True
        return {"outcome": outcome, "result": result}

    def add_points(self, points):
        self.score += points

    def __repr__(self):
        box = "\u25a1"
        checked = "\u2611"
        msg = f"{self.name}: {self.score}"
        return msg

    def __str__(self):
        box = "\u25a1"
        checked = "\u2611"
        msg = f"{box if self.check is False else checked} {self.name.title()}: {self.score}"
        return msg


class HumanCharacter(object):
    
    @staticmethod
    def read_skill_dict(filename="skills.csv"):
        skill_dict = {}
        with open(filename,newline='\n') as csvfile:
            skill_reader = csv.reader(csvfile,delimiter=',',quotechar='|')
            for row in skill_reader:
                name = row[0]
                skill = Skill(name,int(row[1]),rules=row[2])
                skill_dict.update({name : skill})
        return skill_dict

    def stat_dictionary(self):
        return {
            "STR": self.strength,
            "CON": self.constitution,
            "POW": self.power,
            "DEX": self.dexterity,
            "CHA": self.charisma,
            "INT": self.intelligence,
            "SIZ": self.size,
            "EDU": self.education,
        }

    def raise_skill(self, skill_name, points):
        self.skill_dict[skill_name].add_points(points)

    def get_points(self, skill_name):
        ret = self.skill_dict[skill_name].points()
        return ret

    @classmethod
    def generate_random(cls, name,skill_dict):
        # STR, CON, POW, DEX, CHA are all 3d6
        strength = dice_roll(d6_pool(3))
        constitution = dice_roll(d6_pool(3))
        power = dice_roll(d6_pool(3))
        dexterity = dice_roll(d6_pool(3))
        charisma = dice_roll(d6_pool(3))

        # INT and SIZ are 2d6 + 6
        intelligence = dice_roll(d6_pool(2), 6)
        size = dice_roll(d6_pool(2), 6)

        # EDU is 3d6+3
        education = dice_roll(d6_pool(3), 3)
        # Age is 17+2d6, but has a minimum of EDU + 5
        age = dice_roll(d6_pool(2), 17)
        age = age if age >= (education + 5) else (education + 5)

        character = cls(
            name,
            strength,
            constitution,
            power,
            dexterity,
            charisma,
            intelligence,
            size,
            education,
            age,
            skill_dict,
        )
        return character


    def __init__(
        self,
        name,
        strength,
        constitution,
        power,
        dexterity,
        charisma,
        intelligence,
        size,
        education,
        age,
        skill_dict,
    ):
        self.name = name
        # STR, CON, POW, DEX, CHA are all 3d6
        self.strength = strength
        self.constitution = constitution
        self.power = power
        self.dexterity = dexterity
        self.charisma = charisma

        # INT and SIZ are 2d6 + 6
        self.intelligence = intelligence
        self.size = size

        # EDU is 3d6+3
        self.education = education
        # Age is 17+2d6, but has a minimum of EDU + 5
        self.age = age

        # Derived stats
        self.damage_bonus = self.damage_bonus_table()
        self.max_hp = ceil((self.constitution + self.size) / 2)
        self.current_hp = self.max_hp
        self.wound_threshold = ceil(self.max_hp / 2)
        self.xp_bonus = ceil(self.intelligence / 2)

        # Skills
        self.skill_dict = skill_dict

    def damage_bonus_table(self):
        key = self.strength + self.size
        if key >= 41:
            return "+2d6"
        elif key >= 33:
            return "+1d6"
        elif key >= 25:
            return "+1d4"
        elif key >= 17:
            return "None"
        elif key >= 13:
            return "-1d4"
        else:
            return "-1d6"

    def damage_roll(self, weapon_damage):
        key = self.strength + self.size
        damage_bonus = 0
        if key >= 41:
            damage_bonus = dice_roll(dice_pool(2, 6))
        elif key >= 33:
            damage_bonus = dice_roll(dice_pool(1, 6))
        elif key >= 25:
            damage_bonus = dice_roll(dice_pool(1, 4))
        elif key >= 17:
            pass
        elif key >= 13:
            damage_bonus = -(dice_roll(dice_pool(1, 4)))
        else:
            damage_bonus = -(dice_roll(dice_pool(1, 6)))
        return weapon_damage + damage_bonus

    def __repr__(self):
        msg = (
            f"Name: {self.name}\n Age: {self.age:>2}\n"
            f" STR: {self.strength:>2} | INT: {self.intelligence:>2}\n"
            f" CON: {self.constitution:>2} | POW: {self.power:>2}\n"
            f" DEX: {self.dexterity:>2} | CHA: {self.charisma:>2}\n"
            f" SIZ: {self.size:>2} | EDU: {self.education:>2}\n"
            f"  HP: {self.current_hp}/{self.max_hp}"
        )
        for key in self.skill_dict:
            msg += "\n" + str(self.skill_dict[key])
        return msg

    def skill_roll(self, skill_name):
        skill = self.skill_dict[skill_name]
        return skill.roll()


if __name__ == "__main__":
    print("Welcome to the Call of Cthulhu character generator.")
    name = input("Please provide a name for your character: ")
    skill_dict = HumanCharacter.read_skill_dict()
    player = HumanCharacter.generate_random(name,skill_dict)
    print(f"Here is your character, {name}: \n{player}")
    library_roll = player.skill_roll("library use")
    print(
        f"Let's go to the library! You rolled a {library_roll['result']}, which compared to your skill of {player.get_points('library use')} makes it a {'success' if library_roll['outcome'] is True else 'failure'}."
    )