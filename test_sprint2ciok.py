import unittest
from m3b2_ciok_ugorji import checkBirthDeath, checkMarriageDivorce

class testCheckBirthDeath(unittest.TestCase):
    def testInvalidDates(self):
        individual = {'INDI': '@I1@', 'NAME': 'Evan /Ciok/', 'SEX': 'M', 'BIRTH': {'BDATE': '22 JUL 2074'}, 'DEATH': {'DDATE': '13 SEP 2001'}, 'FAMC': '@F1@'} 
        self.assertEqual(checkBirthDeath(individual),'ERROR in I1: death of Evan /Ciok/ on 13 SEP 2001 is before their birth date.')

class testCheckMarriageDivorce(unittest.TestCase):
    def testValidDates(self):
        family = {'FAM': '@F1@', 'HUSB': '@I2@', 'WIFE': '@I3@', 'CHIL': '@I1@', 'MARR': {'MDATE': '17 JUN 2026'}, 'DIV': {'DIVDATE': '7 SEP 2028'}}
        self.assertEqual(checkMarriageDivorce(family),'None')

if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()