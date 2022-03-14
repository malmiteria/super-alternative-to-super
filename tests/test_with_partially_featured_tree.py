from parent import Parenting, ConcurentMethodResolutionError
import unittest

# one parent not parented, one is, order matters
# A(P,U)
# - A has it
#  - P does, U doesn't
#  - P does, U does
#  - P doesn't, U does
#  - P doesn't, U doesn't
# - A doesn't
#  - P does, U doesn't
#  - P does, U does
#  - P doesn't, U does
#  - P doesn't, U doesn't
# A(U,P)
# - A has it
#  - P does, U doesn't
#  - P does, U does
#  - P doesn't, U does
#  - P doesn't, U doesn't
# - A doesn't
#  - P does, U doesn't
#  - P does, U does
#  - P doesn't, U does
#  - P doesn't, U doesn't
# This was only direct resolution on parented
# Do the same for all features, with parented  and unparented presenting all different cases.
# combinatory is huge, gl

class StraightForwardParented(Parenting):
    attribute = 'straight_forward_parented'
    def method(self):
        return 'StraightForwardParented'

class StraightForwardUnparented:
    attribute = 'straight_forward_unparented'
    def method(self):
        return 'StraightForwardUnparented'

class NFP1(Parenting): pass
class NFP2(Parenting): pass
class NFP3(Parenting): pass
class NFP4(Parenting): pass
class NotFoundParented(NFP1,NFP2,NFP3,NFP4):
    pass

class NFU1: pass
class NFU2: pass
class NFU3: pass
class NFU4: pass
class NotFoundUnparented(NFU1,NFU2,NFU3,NFU4):
    pass

class O1PHIP(Parenting):
    attribute = 'only_one_parent_has_it_parented'
    def method(self):
        return 'OnlyOneParentHasItParented'
class O1PHIP1(Parenting): pass
class O1PHIP2(Parenting): pass
class O1PHIP3(Parenting): pass
class O1PHIP4(Parenting): pass
class OnlyOneParentHasItParented(O1PHIP,O1PHIP1,O1PHIP2,O1PHIP3,O1PHIP4):
    pass

class O1PHIU:
    attribute = 'only_one_parent_has_it_unparented'
    def method(self):
        return 'OnlyOneParentHasItUnparented'
class O1PHIU1: pass
class O1PHIU2: pass
class O1PHIU3: pass
class O1PHIU4: pass
class OnlyOneParentHasItUnparented(O1PHIU,O1PHIU1,O1PHIU2,O1PHIU3,O1PHIU4):
    pass

class MPHI1(Parenting):
    attribute = 'multiple_parent_have_it_parented_1'
    def method(self):
        return 'MultipleParentHaveItParented1'
class MPHI2(Parenting):
    attribute = 'multiple_parent_have_it_parented_2'
    def method(self):
        return 'MultipleParentHaveItParented2'
class MultipleParentHaveItParented(MPHI1,MPHI2):
    pass

class MPHI1:
    attribute = 'multiple_parent_have_it_unparented_1'
    def method(self):
        return 'MultipleParentHaveItUnparented1'
class MPHI2:
    attribute = 'multiple_parent_have_it_unparented_2'
    def method(self):
        return 'MultipleParentHaveItUnparented2'
class MultipleParentHaveItUnparented(MPHI1,MPHI2):
    pass

class DGP(Parenting):
    attribute = 'diamond_grandparent_has_it_parented'
    def method(self):
        return 'DiamondGrandparentHasItParented'
class DP1(DGP): pass
class DP2(DGP): pass
class DiamondParented(DP1,DP2):
    pass

class DGU:
    attribute = 'diamond_grandparent_has_it_unparented'
    def method(self):
        return 'DiamondGrandparentHasItUnparented'
class DU1(DGU): pass
class DU2(DGU): pass
class DiamondUnparented(DU1,DU2):
    pass

class_cases = {
    'P': {
        'SF': StraightForwardParented,
        'NF': NotFoundParented,
        'O1PHI': OnlyOneParentHasItParented,
        'MPHI': MultipleParentHaveItParented,
        'D': DiamondParented,
    },
    'U': {
        'SF': StraightForwardUnparented,
        'NF': NotFoundUnparented,
        'O1PHI': OnlyOneParentHasItUnparented,
        'MPHI': MultipleParentHaveItUnparented,
        'D': DiamondUnparented,
    }
}
ccp = class_cases['P']
ccu = class_cases['U']

class TestChildHasIt(unittest.TestCase):
    def test_all_case_with_parented_first(self):
        for parented_case_name, ParentedCase in ccp.items():
            for unparented_case_name, UnparentedCase in ccu.items():
                class A(ParentedCase,UnparentedCase):
                    attribute = 'a'
                    def method(self):
                        return 'A'

                assert A().method() == 'A'
                assert A().attribute == 'a'

    def test_all_case_with_unparented_first(self):
        for unparented_case_name, UnparentedCase in ccu.items():
            for parented_case_name, ParentedCase in ccp.items():
                class A(UnparentedCase,ParentedCase):
                    attribute = 'a'
                    def method(self):
                        return 'A'

                assert A().method() == 'A'
                assert A().attribute == 'a'


class TestChildDoesntHaveIt_PUorder_UNF(unittest.TestCase):
    def test_PNF_UNF(self):
        class A(ccp['NF'],ccu['NF']):
            pass

        with self.assertRaises(AttributeError):
            assert A().method
        with self.assertRaises(AttributeError):
            assert A().attribute

    def test_PSF_UNF(self):
        class A(ccp['SF'],ccu['NF']):
            pass

        assert A().method() == 'StraightForwardParented'
        assert A().attribute == 'straight_forward_parented'

    def test_PO1PHI_UNF(self):
        class A(ccp['O1PHI'],ccu['NF']):
            pass

        assert A().method() == 'OnlyOneParentHasItParented'
        assert A().attribute == 'only_one_parent_has_it_parented'

    def test_PMPHI_UNF(self):
        class A(ccp['MPHI'],ccu['NF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PD_UNF(self):
        class A(ccp['D'],ccu['NF']):
            pass

        assert A().method() == 'DiamondGrandparentHasItParented'
        assert A().attribute == 'diamond_grandparent_has_it_parented'


class TestChildDoesntHaveIt_PUorder_USF(unittest.TestCase):
    def test_PNF_USF(self):
        class A(ccp['NF'],ccu['SF']):
            pass

        assert A().method() == 'StraightForwardUnparented'
        assert A().attribute == 'straight_forward_unparented'

    def test_PSF_USF(self):
        class A(ccp['SF'],ccu['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PO1PHI_USF(self):
        class A(ccp['O1PHI'],ccu['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PMPHI_USF(self):
        class A(ccp['MPHI'],ccu['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PD_USF(self):
        class A(ccp['D'],ccu['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_PUorder_UO1PHI(unittest.TestCase):
    def test_PNF_UO1PHI(self):
        class A(ccp['NF'],ccu['O1PHI']):
            pass

        assert A().method() == 'OnlyOneParentHasItUnparented'
        assert A().attribute == 'only_one_parent_has_it_unparented'

    def test_PSF_UO1PHI(self):
        class A(ccp['SF'],ccu['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PO1PHI_UO1PHI(self):
        class A(ccp['O1PHI'],ccu['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PMPHI_UO1PHI(self):
        class A(ccp['MPHI'],ccu['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PD_UO1PHI(self):
        class A(ccp['D'],ccu['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_PUorder_UMPHI(unittest.TestCase):
    def test_PNF_UMPHI(self):
        class A(ccp['NF'],ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PSF_UMPHI(self):
        class A(ccp['SF'],ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PO1PHI_UMPHI(self):
        class A(ccp['O1PHI'],ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PMPHI_UMPHI(self):
        class A(ccp['MPHI'],ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PD_UMPHI(self):
        class A(ccp['D'],ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_PUorder_UD(unittest.TestCase):
    def test_PNF_UD(self):
        class A(ccp['NF'],ccu['D']):
            pass

        assert A().method() == 'DiamondGrandparentHasItUnparented'
        assert A().attribute == 'diamond_grandparent_has_it_unparented'

    def test_PSF_UD(self):
        class A(ccp['SF'],ccu['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PO1PHI_UD(self):
        class A(ccp['O1PHI'],ccu['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PMPHI_UD(self):
        class A(ccp['MPHI'],ccu['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_PD_UD(self):
        class A(ccp['D'],ccu['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_UPorder_PNF(unittest.TestCase):
    def test_UNF_PNF(self):
        class A(ccu['NF'],ccp['NF']):
            pass

        with self.assertRaises(AttributeError):
            assert A().method
        with self.assertRaises(AttributeError):
            assert A().attribute

    def test_USF_PNF(self):
        class A(ccu['SF'],ccp['NF']):
            pass

        assert A().method() == 'StraightForwardUnparented'
        assert A().attribute == 'straight_forward_unparented'

    def test_UO1PHI_PNF(self):
        class A(ccu['O1PHI'],ccp['NF']):
            pass

        assert A().method() == 'OnlyOneParentHasItUnparented'
        assert A().attribute == 'only_one_parent_has_it_unparented'

    def test_UMPHI_PNF(self):
        class A(ccu['MPHI'],ccp['NF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_PNF(self):
        class A(ccu['D'],ccp['NF']):
            pass

        assert A().method() == 'DiamondGrandparentHasItUnparented'
        assert A().attribute == 'diamond_grandparent_has_it_unparented'


class TestChildDoesntHaveIt_UPorder_PSF(unittest.TestCase):
    def test_UNF_PSF(self):
        class A(ccu['NF'],ccp['SF']):
            pass

        assert A().method() == 'StraightForwardParented'
        assert A().attribute == 'straight_forward_parented'

    def test_USF_PSF(self):
        class A(ccu['SF'],ccp['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UO1PHI_PSF(self):
        class A(ccu['O1PHI'],ccp['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UMPHI_PSF(self):
        class A(ccu['MPHI'],ccp['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_PSF(self):
        class A(ccu['D'],ccp['SF']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_UPorder_PO1PHI(unittest.TestCase):
    def test_UNF_PO1PHI(self):
        class A(ccu['NF'],ccp['O1PHI']):
            pass

        assert A().method() == 'OnlyOneParentHasItParented'
        assert A().attribute == 'only_one_parent_has_it_parented'

    def test_USF_PO1PHI(self):
        class A(ccu['SF'],ccp['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UO1PHI_PO1PHI(self):
        class A(ccu['O1PHI'],ccp['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UMPHI_PO1PHI(self):
        class A(ccu['MPHI'],ccp['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_PO1PHI(self):
        class A(ccu['D'],ccp['O1PHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_UPorder_PMPHI(unittest.TestCase):
    def test_UNF_PMPHI(self):
        class A(ccu['NF'],ccp['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_USF_PMPHI(self):
        class A(ccu['SF'],ccp['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UO1PHI_PMPHI(self):
        class A(ccu['O1PHI'],ccp['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UMPHI_PMPHI(self):
        class A(ccu['MPHI'],ccp['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_PMPHI(self):
        class A(ccu['D'],ccp['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_UPorder_PD(unittest.TestCase):
    def test_UNF_PD(self):
        class A(ccu['NF'],ccp['D']):
            pass

        assert A().method() == 'DiamondGrandparentHasItParented'
        assert A().attribute == 'diamond_grandparent_has_it_parented'

    def test_USF_PD(self):
        class A(ccu['SF'],ccp['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UO1PHI_PD(self):
        class A(ccu['O1PHI'],ccp['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UMPHI_PD(self):
        class A(ccu['MPHI'],ccp['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_PD(self):
        class A(ccu['D'],ccp['D']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute


class TestChildDoesntHaveIt_Unparented_Parenting(unittest.TestCase):
    def test_UNF_Parenting(self):
        class A(ccu['NF'],Parenting):
            pass

        with self.assertRaises(AttributeError):
            assert A().method
        with self.assertRaises(AttributeError):
            assert A().attribute

    def test_USF_Parenting(self):
        class A(ccu['SF'],Parenting):
            pass

        assert A().method() == 'StraightForwardUnparented'
        assert A().attribute == 'straight_forward_unparented'

    def test_UO1PHI_Parenting(self):
        class A(ccu['O1PHI'],Parenting):
            pass

        assert A().method() == 'OnlyOneParentHasItUnparented'
        assert A().attribute == 'only_one_parent_has_it_unparented'

    def test_UMPHI_Parenting(self):
        class A(ccu['MPHI'],Parenting):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_UD_Parenting(self):
        class A(ccu['D'],Parenting):
            pass

        assert A().method() == 'DiamondGrandparentHasItUnparented'
        assert A().attribute == 'diamond_grandparent_has_it_unparented'


class TestChildDoesntHaveIt_Parenting_Unparented(unittest.TestCase):
    def test_Parenting_UNF(self):
        class A(Parenting,ccu['NF']):
            pass

        with self.assertRaises(AttributeError):
            assert A().method
        with self.assertRaises(AttributeError):
            assert A().attribute

    def test_Parenting_USF(self):
        class A(Parenting,ccu['SF']):
            pass

        assert A().method() == 'StraightForwardUnparented'
        assert A().attribute == 'straight_forward_unparented'

    def test_Parenting_UO1PHI(self):
        class A(Parenting,ccu['O1PHI']):
            pass

        assert A().method() == 'OnlyOneParentHasItUnparented'
        assert A().attribute == 'only_one_parent_has_it_unparented'

    def test_Parenting_UMPHI(self):
        class A(Parenting,ccu['MPHI']):
            pass

        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().method
        with self.assertRaises(ConcurentMethodResolutionError):
            assert A().attribute

    def test_Parenting_UD(self):
        class A(Parenting,ccu['D']):
            pass

        assert A().method() == 'DiamondGrandparentHasItUnparented'
        assert A().attribute == 'diamond_grandparent_has_it_unparented'
