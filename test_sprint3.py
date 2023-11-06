import unittest
from m3b2_ciok_ugorji import Individual, Family, listMarried, listSingle, checkMarryDescendant

class testCheckBirthDeath(unittest.TestCase):
    def testListSingle(self):
        ind = Individual()
        ind.name = 'John Doe'
        ind.bday = '1 JAN 1980'
        ind.sfam = ''
        self.assertEqual(listSingle(ind),'John Doe is 43 years old and single.')

    def testListMarried(self):
        fam = Family() 
        fam.married = 'Y'
        fam.divorced = ''
        fam.husband = 'I1'
        fam.wife = 'I2'
        self.assertEqual(listMarried(fam),'XXXXXX /XXXX/ and XXXXXX /XXXX/ are married.')
        # placeholder names to show the list married functionality works without depending on the findByID function


if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()