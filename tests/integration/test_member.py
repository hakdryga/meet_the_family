from unittest import TestCase

from family_tree.member import Member, Gender


class TestMember(TestCase):
    def setUp(self) -> None:
        self.member = Member(1, "Zim", "Male")
        self.mother = Member(2, "Mother", "Female")
        self.father = Member(3, "Father", "Male")
        self.paternal_grandmother = Member(21, "PaternalGrandMother", "Female")
        self.maternal_grandmother = Member(21, "MaternalGrandMother", "Female")

        self.mother_sister_a = Member(4, "MaternalAuntA", "Female")
        self.mother_sister_b = Member(5, "MaternalAuntB", "Female")
        self.mother_brother_a = Member(6, "MaternalUncleA", "Male")
        self.mother_brother_b = Member(7, "MaternalUncleB", "Male")

        self.father_sister_a = Member(8, "PaternalAuntA", "Female")
        self.father_sister_b = Member(9, "PaternalAuntB", "Female")
        self.father_brother_a = Member(10, "PaternalUncleA", "Male")
        self.father_brother_b = Member(11, "PaternalUncleB", "Male")

        self.spouse = Member(12, "Wife", "Female")

        self.brother_a = Member(13, "BroA", "Male")
        self.brother_b = Member(13, "BroB", "Male")
        self.sister_a = Member(13, "SisA", "Female")
        self.sister_b = Member(13, "SisB", "Female")
        self.son_a = Member(13, "SonA", "Male")
        self.son_b = Member(13, "SonB", "Male")
        self.daughter_a = Member(13, "DaughterA", "Female")
        self.daughter_b = Member(13, "DaughterB", "Female")

        self.member.set_mother(self.mother)
        self.member.set_father(self.father)

        # adding siblings
        self.father.add_child(self.brother_a)
        self.father.add_child(self.brother_b)
        self.father.add_child(self.sister_a)
        self.father.add_child(self.sister_b)
        self.father.add_child(self.member)  # me
        self.mother.add_child(self.brother_a)
        self.mother.add_child(self.brother_b)
        self.mother.add_child(self.sister_a)
        self.mother.add_child(self.sister_b)
        self.mother.add_child(self.member)  # me

        self.member.set_spouse(self.spouse)
        self.spouse.set_spouse(self.member)

        self.paternal_grandmother.add_child(self.father_sister_a)
        self.paternal_grandmother.add_child(self.father_sister_b)
        self.paternal_grandmother.add_child(self.father_brother_a)
        self.paternal_grandmother.add_child(self.father_brother_b)
        self.paternal_grandmother.add_child(self.father)
        self.father.set_mother(self.paternal_grandmother)

        self.maternal_grandmother.add_child(self.mother_sister_a)
        self.maternal_grandmother.add_child(self.mother_sister_b)
        self.maternal_grandmother.add_child(self.mother_brother_a)
        self.maternal_grandmother.add_child(self.mother_brother_b)
        self.maternal_grandmother.add_child(self.mother)
        self.mother.set_mother(self.maternal_grandmother)

        self.member.add_child(self.son_a)
        self.member.add_child(self.son_b)
        self.member.add_child(self.daughter_a)
        self.member.add_child(self.daughter_b)

    def test_set_methods(self):
        self.assertEqual(self.mother.name, "Mother")
        self.assertEqual(self.father.name, "Father")
        self.assertEqual(self.member in self.member.father.children, True)
        self.assertEqual(self.member in self.member.mother.children, True)

        self.assertEqual(len(self.member.mother.children), 5)
        self.assertEqual(len(self.member.father.children), 5)
        self.assertEqual(self.brother_a in self.member.mother.children, True)
        self.assertEqual(self.brother_b in self.member.mother.children, True)
        self.assertEqual(self.sister_a in self.member.mother.children, True)
        self.assertEqual(self.sister_b in self.member.mother.children, True)
        self.assertEqual(self.brother_a in self.member.father.children, True)
        self.assertEqual(self.brother_b in self.member.father.children, True)
        self.assertEqual(self.sister_a in self.member.father.children, True)
        self.assertEqual(self.sister_b in self.member.father.children, True)

        self.assertEqual(self.member.spouse.name, "Wife")

        # test maternal/paternal aunts and uncles
        self.assertEqual(len(self.maternal_grandmother.children), 5)
        self.assertEqual(len(self.paternal_grandmother.children), 5)
        self.assertEqual(self.mother_sister_a in self.maternal_grandmother.children, True)
        self.assertEqual(self.mother_sister_b in self.maternal_grandmother.children, True)
        self.assertEqual(self.mother_brother_a in self.maternal_grandmother.children, True)
        self.assertEqual(self.mother_brother_b in self.maternal_grandmother.children, True)
        self.assertEqual(self.mother in self.maternal_grandmother.children, True)
        self.assertEqual(self.father_sister_a in self.paternal_grandmother.children, True)
        self.assertEqual(self.father_sister_b in self.paternal_grandmother.children, True)
        self.assertEqual(self.father_brother_a in self.paternal_grandmother.children, True)
        self.assertEqual(self.father_brother_b in self.paternal_grandmother.children, True)
        self.assertEqual(self.father in self.paternal_grandmother.children, True)

        # test children
        self.assertEqual(len(self.member.children), 4)
        self.assertEqual(self.son_a in self.member.children, True)
        self.assertEqual(self.son_b in self.member.children, True)
        self.assertEqual(self.daughter_a in self.member.children, True)
        self.assertEqual(self.daughter_b in self.member.children, True)

    def test_get_relationship_methods(self):
        self.assertEqual(len(self.member.get_relationship("paternal_aunt")), 2)
        self.assertEqual(len(self.member.get_relationship("paternal_uncle")), 2)
        self.assertEqual(len(self.member.get_relationship("maternal_aunt")), 2)
        self.assertEqual(len(self.member.get_relationship("maternal_uncle")), 2)
        self.assertEqual(len(self.member.spouse.get_relationship("brother_in_law")), 2)
        self.assertEqual(len(self.member.spouse.get_relationship("sister_in_law")), 2)
        self.assertEqual(len(self.member.get_relationship("son")), 2)
        self.assertEqual(len(self.member.get_relationship("daughter")), 2)
        self.assertEqual(len(self.member.get_relationship("siblings")), 4)
