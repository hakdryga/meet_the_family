from unittest import TestCase
from family_tree.member import Member, Gender


class TestMember(TestCase):

    def setUp(self) -> None:
        self.member = Member(1, "Zim", "Male")

    def test_init(self):
        # check instance
        self.assertEqual(isinstance(self.member, Member), True)

        # check properties
        self.assertEqual(self.member.id, 1)
        self.assertEqual(self.member.name, "Zim")
        # self.assertEqual(self.member.gender.value, "Male")
        self.assertEqual(self.member.gender, Gender.male)
        self.assertEqual(self.member.mother, None)
        self.assertEqual(self.member.father, None)
        self.assertEqual(self.member.spouse, None)
        self.assertEqual(self.member.children, [])

        # edge case for gender (only male or female)
        self.assertRaises(ValueError, Member, 2, "Petra", "WrongValue")

    def test_set_mother(self):
        mother_a = "mother_a"                       # ValueError --> no Member object
        mother_b = Member(2, "MotherA", "Male")     # ValueError --> male
        mother_c = Member(3, "MotherB", "Female")
        # failure cases
        self.assertRaises(ValueError, self.member.set_mother, mother_a)
        self.assertRaises(ValueError, self.member.set_mother, mother_b)
        # success case
        self.member.set_mother(mother_c)
        self.assertEqual(self.member.mother.name, "MotherB")
        # self.assertEqual(self.member.mother.gender.value, "Female")
        self.assertEqual(self.member.mother.gender, Gender.female)

    def test_set_father(self):
        father_a = "father_a"                       # ValueError --> no Member object
        father_b = Member(2, "FatherA", "Male")     # success
        father_c = Member(3, "FatherB", "Female")   # ValueError --> female
        # failure cases
        self.assertRaises(ValueError, self.member.set_father, father_a)
        self.assertRaises(ValueError, self.member.set_father, father_c)
        # success case
        self.member.set_father(father_b)
        self.assertEqual(self.member.father.name, "FatherA")
        # self.assertEqual(self.member.father.gender.value, "Male")
        self.assertEqual(self.member.father.gender, Gender.male)

    def test_set_spouse(self):
        spouse_a = "spouse_a"
        spouse_b = Member(2, "SpouseB", "Male")
        spouse_c = Member(3, "SpouseC", "Female")
        # failure cases
        self.assertRaises(ValueError, self.member.set_spouse, spouse_a)
        self.assertRaises(ValueError, self.member.set_spouse, spouse_b)
        # success case
        self.member.set_spouse(spouse_c)
        self.assertEqual(self.member.spouse.name, "SpouseC")
        # self.assertEqual(self.member.father.gender.value, "Male")
        self.assertEqual(self.member.spouse.gender, Gender.female)

    def test_add_child(self):
        child_a = "child_a"
        child_b = Member(4, "Daughter", "Female")
        # failure case
        self.assertRaises(ValueError, self.member.add_child, child_a)
        # success case
        self.member.add_child(child_b)
        self.assertEqual(len(self.member.children), 1)
        self.assertEqual(self.member.children[0].name, "Daughter")
        self.assertEqual(self.member.children[0].gender, Gender.female)

