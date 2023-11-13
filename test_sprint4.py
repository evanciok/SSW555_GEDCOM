import unittest
from m3b2_ciok_ugorji import Individual, Family, checkDate, checkDuplicateInd, checkDuplicateFam

class testCheckBirthDeath(unittest.TestCase):
    def testCheckDate(self):
        self.assertEqual(checkDate('13 SEP 2001'),True)
        self.assertEqual(checkDate('30 FEB 2005'),False)

    def testCheckDuplicateInd(self):
        indIDs = ['@I1@', '@I1', '@I2@']
        ind = Individual()
        ind._id = '@I1@'
        self.assertEqual(checkDuplicateInd(ind), "Error: duplicate individual ID I1")

    def testCheckDuplicateFam(self):
        famIDs = ['@F1@', '@F1', '@F2@']
        fam = Family()
        fam._id = '@F1@'
        self.assertEqual(checkDuplicateFam(fam), "Error: duplicate family ID F1")


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()