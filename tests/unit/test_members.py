from unittest import TestCase
from unittest.mock import patch, Mock
from family_tree.member import Member, Gender


def create_fake_member(id=None, name=None, gender=None, mother=None,
                       spouse=None, father=None, children=None):
    member = Mock()
    member.id = id
    member.name = name
    member.gender = gender
    member.mother = mother
    member.spouse = spouse
    member.father = father
    member.children = children
    return member


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
        mother_a = "mother_a"  # ValueError --> no Member object
        mother_b = Member(2, "MotherA", "Male")  # ValueError --> male
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
        father_a = "father_a"  # ValueError --> no Member object
        father_b = Member(2, "FatherA", "Male")  # success
        father_c = Member(3, "FatherB", "Female")  # ValueError --> female
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

    def test_get_paternal_grandmother(self):
        member = Member(9, "NewMember", "Male")
        father = Member(10, "NewMember_father", "Male")
        grand_mother = Member(11, "NewMember_grandMother", "Female")

        # failure cases
        self.assertEqual(member.get_paternal_grandmother(), None)
        member.father = father
        self.assertEqual(member.get_paternal_grandmother(), None)
        member.father.mother = grand_mother
        self.assertEqual(member.get_paternal_grandmother(), grand_mother)

    def test_get_maternal_grandmother(self):
        member = Member(9, "NewMember", "Male")
        mother = Member(10, "NewMember_mother", "Female")
        grand_mother = Member(11, "NewMember_grandMother", "Female")

        # failure cases
        self.assertEqual(member.get_maternal_grandmother(), None)
        member.mother = mother
        self.assertEqual(member.get_maternal_grandmother(), None)
        member.mother.mother = grand_mother
        self.assertEqual(member.get_maternal_grandmother(), grand_mother)

    def test_get_spouse_mother(self):
        member = Member(9, "NewMember", "Male")
        spouse = Member(10, "NewMember_spouse", "Female")
        spouse_mother = Member(11, "NewMember_spouse_mother", "Female")

        # failure cases
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse = spouse
        self.assertEqual(member.get_spouse_mother(), None)

        member.spouse.mother = spouse_mother
        self.assertEqual(member.get_spouse_mother(), spouse_mother)

    # mock with one return value
    # @patch("family_tree.member.Member.get_paternal_grandmother", return_value=None)
    # side effects - return many values from mock
    @patch("family_tree.member.Member.get_paternal_grandmother", side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Dad", "Male")]),
        create_fake_member(children=[
            Member(3, "Dad", "Male"),
            Member(4, "Uncle", "Male")
        ]),
        create_fake_member(children=[
            Member(3, "Dad", "Male"),
            Member(4, "Uncle", "Male"),
            Member(5, "Aunt", "Female")
        ])

    ])
    def test_get_paternal_aunt(self, mock_get_paternal_grandmother):
        # check get_paternal_grandmother has been replaced by a mock
        self.assertEqual(isinstance(self.member.get_paternal_grandmother, Mock), True)

        self.assertEqual(self.member.get_paternal_aunt(), [])  # first param from side_effect
        self.assertEqual(self.member.get_paternal_aunt(), [])  # second param from side_effect
        self.assertEqual(self.member.get_paternal_aunt(), [])  # third param from side_effect
        self.assertEqual(self.member.get_paternal_aunt(), [])  # fourth param from side_effect

        paternal_aunts = self.member.get_paternal_aunt()
        self.assertEqual(paternal_aunts[0].name, "Aunt")  # fifth param from side_effect
        self.assertEqual(paternal_aunts[0].gender, Gender.female)
        self.assertEqual(len(paternal_aunts), 1)

    @patch("family_tree.member.Member.get_paternal_grandmother", side_effect=[
        None,
        create_fake_member(),
        create_fake_member(children=[Member(3, "Dad", "Male")]),
        create_fake_member(children=[
            Member(3, "Aunt", "Female"),
            Member(4, "Dad", "Male")
        ]),
        create_fake_member(children=[
            Member(3, "Dad", "Male"),
            Member(4, "Uncle", "Male"),
            Member(5, "Aunt", "Female")
        ])

    ])
    def test_get_paternal_uncle(self, mock_get_paternal_grandmother):
        self.member.father = Member(3, "Dad", "Male")
        self.assertEqual(self.member.get_paternal_uncle(), [])  # first param from side_effect
        self.assertEqual(self.member.get_paternal_uncle(), [])  # second param from side_effect
        self.assertEqual(self.member.get_paternal_uncle(), [])  # third param from side_effect
        self.assertEqual(self.member.get_paternal_uncle(), [])  # fourth param from side_effect

        paternal_uncle = self.member.get_paternal_uncle()
        self.assertEqual(paternal_uncle[0].name, "Uncle")  # fifth param from side_effect
        self.assertEqual(paternal_uncle[0].gender, Gender.male)
        self.assertEqual(len(paternal_uncle), 1)
