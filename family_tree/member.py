from enum import Enum


class Gender(Enum):
    male = "Male"
    female = "Female"


class Member:
    def __init__(self, id, name, gender):
        self.id = id
        self.name = name
        self.gender = Gender(gender)
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = []

    def set_mother(self, mother):
        if not isinstance(mother, Member):
            raise ValueError("Invalid value for mother")
        # import pdb; pdb.set_trace()
        if mother.gender != Gender.female:
            raise ValueError("Mother should be a female!")

        self.mother = mother

    def set_father(self, father):
        if not isinstance(father, Member):
            raise ValueError("Invalid value for father")
        # import pdb; pdb.set_trace()
        if father.gender != Gender.male:
            raise ValueError("father should be a male!")

        self.father = father

    def set_spouse(self, spouse):
        if not isinstance(spouse, Member):
            raise ValueError("Invalid value for spouse")
        import pdb; pdb.set_trace()
        if self.gender == spouse.gender:
            raise ValueError("Invalid gender for spouse")

        self.spouse = spouse

    def add_child(self, child):
        if not isinstance(child, Member):
            raise ValueError('Invalid value for child')
        self.children.append(child)