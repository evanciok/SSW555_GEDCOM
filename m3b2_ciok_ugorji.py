# auth: evan ciok & chibunnam ugorji
# course: ssw/css 555
# assignment: m3.b2

from datetime import datetime
def findAge(birthDay, deathDay):
    birthDay = datetime.strptime(birthDay, "%d %b %Y")
    reference = datetime.today()    
    if deathDay:
        deathDay = datetime.strptime(deathDay, "%d %b %Y")
        deathAge = deathDay.year - birthDay.year - ((deathDay.month, deathDay.day) < (birthDay.month, birthDay.day))
        return deathAge
    else:
        currentAge = reference.year - birthDay.year - ((reference.month, reference.day) < (birthDay.month, birthDay.day))
        return currentAge
    
allIndividuals = []
allFamilies = []
newIndividual = {}
newFamily = {}

def parseFile(input):
    global newIndividual
    global newFamily
    fullLine = input.strip()
    lineSections = fullLine.split()
    level = int(lineSections[0])

    if level == 0 and len(lineSections) > 2:
        tag = lineSections[2] 
        if tag == 'INDI':
            if newIndividual:
                allIndividuals.append(newIndividual)
            newIndividual = {} 
            newIndividual['INDI'] = lineSections[1]
        elif tag == 'FAM':
            if newFamily:
                allFamilies.append(newFamily)
            newFamily = {}
            newFamily['FAM'] = lineSections[1]
    elif level == 1:
        tag = lineSections[1] 
        if tag == 'NAME':
            newIndividual['NAME'] = ' '.join(lineSections[2:])
        elif tag == 'SEX':
            newIndividual['SEX'] = lineSections[2]
        elif tag == 'BIRT':
            newIndividual['BIRTH'] = {}
        elif tag == 'FAMS':
            newIndividual['FAMS'] = lineSections[2]
        elif tag == 'FAMC':
            newIndividual['FAMC'] = lineSections[2]
        elif tag == 'DEAT':
            newIndividual['DEATH'] = {}
        elif tag == 'MARR':
            newFamily['MARR'] = {}
        elif tag == 'DIV':
            newFamily['DIV'] = {}
        elif tag == 'HUSB':
            newFamily['HUSB'] = lineSections[2]
        elif tag == 'WIFE':
            newFamily['WIFE'] = lineSections[2]
        elif tag == 'CHIL':
            newFamily['CHIL'] = lineSections[2]
    elif level == 2:
        tag = lineSections[1]
        if 'DEATH' in newIndividual:
            if tag == 'DATE':
                newIndividual['DEATH']['DDATE'] = ' '.join(lineSections[2:])
        elif 'BIRTH' in newIndividual:
            if tag == 'DATE':
                newIndividual['BIRTH']['BDATE'] = ' '.join(lineSections[2:])
        if 'MARR' in newFamily:
            if tag == 'DATE':
                newFamily['MARR']['MDATE'] = ' '.join(lineSections[2:])
        elif 'DIV' in newFamily:
            if tag == 'DATE':
                newFamily['DIV']['DIVDATE'] = ' '.join(lineSections[2:])
    

with open('m3b2_test.ged') as gedcomFile:
    for line in gedcomFile:
        parseFile(line)

if newIndividual not in allIndividuals:
    allIndividuals.append(newIndividual) 

if newFamily not in allFamilies:
    allFamilies.append(newFamily)

print("{:<10} {:<20} {:<5} {:<15} {:<5} {:<10} {:<15} {:<10} {:<10}".format("ID", "Name", "Sex", "Birthday", "Age", "Status", "Death", "Child", "Spouse"))
for individual in allIndividuals:
    indID = individual.get('INDI', '')
    indString = ''.join(indID)
    indIDFiltered = indString[1:-1]

    name = individual.get('NAME', '')
   
    sex = individual.get('SEX', '')
   
    spouseOf = individual.get('FAMS', '')
    spouseOfString = ''.join(spouseOf)
    spouseOfIDFiltered = spouseOfString[1:-1]

    childOf = individual.get('FAMC', '')
    childOfString = ''.join(childOf)
    childOfIDFiltered = childOfString[1:-1]

    birthday = individual.get('BIRTH', {}).get('BDATE', '')
    death_date = individual.get('DEATH', {}).get('DDATE', '')
    age = findAge(birthday, death_date)
    status = "Alive" if not death_date else "Deceased"

    print("{:<10} {:<20} {:<5} {:<15} {:<5} {:<10} {:<15} {:<10} {:<10}".format(indIDFiltered, name, sex, birthday, age, status, death_date, childOfIDFiltered, spouseOfIDFiltered))

print("")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("")

print("{:<10} {:<20} {:<20} {:<15} {:<20} {:<10} {:<20} {:<10} ".format("ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"))
for family in allFamilies:
    famID = family.get('FAM', '')
    famIDString = ''.join(famID)
    famIDFiltered = famIDString[1:-1]
   
    marryDate = family.get('MARR', {}).get('MDATE', '')
   
    divorceDate = family.get('DIV', {}).get('DIVDATE', '')
   
    husbandID = family.get('HUSB', '')
    hLookupString = ''.join(husbandID)
    husbandIDFiltered = hLookupString[1:-1]
    hLookup = int(hLookupString[2:-1]) - 1
    husbandName = allIndividuals[hLookup].get('NAME','')
   
    wifeID = family.get('WIFE', '')
    wLookupString = ''.join(wifeID)
    wifeIDFiltered = wLookupString[1:-1]
    wLookup = int(wLookupString[2:-1]) - 1
    wifeName = allIndividuals[wLookup].get('NAME','')
    
    children = family.get('CHIL', '')
    childrenString = ''.join(children)
    childrenIDFiltered = childrenString[1:-1]

    print("{:<10} {:<20} {:<20} {:<15} {:<20} {:<10} {:<20} {:<10} ".format(famIDFiltered, marryDate, divorceDate, husbandIDFiltered, husbandName, wifeIDFiltered, wifeName, childrenIDFiltered))