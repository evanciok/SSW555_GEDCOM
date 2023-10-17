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

class Individual:
    _id = "XX"
    sex = "X"
    name = "XXXXXX /XXXX/"
    fname = "XXXX"
    given_lname = "XXXX"
    lname = "XXXX"
    bday = None
    dday = None
    cfam = None
    sfam = None

class Family:
    _id = "XX"
    married = None
    divorced = None
    wife = "XXX"
    husband = "XXX"
    children = None

Individuals = []
Families = []
curr_ind = None
curr_fam = None
readData = 0

def parseFile(input):
    global newIndividual
    global newFamily
    
    global curr_ind
    global curr_fam
    global readData
    
    fullLine = input.strip()
    lineSections = fullLine.split()
    level = int(lineSections[0])

    if level == 0 and len(lineSections) > 2:
        tag = lineSections[2]
        cleanup = 0
        #david's additions for sanity{
        while cleanup == 0:
            if curr_ind:
                Individuals.append(curr_ind)
            curr_ind = None

            if curr_fam:
                Families.append(curr_fam)
            curr_fam = None
            cleanup = 1
        #}
        
        if tag == 'INDI':
            readData = 1
            if newIndividual:
                allIndividuals.append(newIndividual)
            newIndividual = {} 
            newIndividual['INDI'] = lineSections[1]

            #david's additions for sanity{
            curr_ind = Individual()
            curr_ind._id = lineSections[1]
            #}
   
        elif tag == 'FAM':
            readData = 2
            if newFamily:
                allFamilies.append(newFamily)
            newFamily = {}
            newFamily['FAM'] = lineSections[1]

            #david's additions for sanity{
            curr_fam = Family()
            curr_fam.children = []
            curr_fam._id = lineSections[1]
            
        else:
            readData = 0
            #}
            
    elif level == 1:
        tag = lineSections[1] 
        if tag == 'NAME' and readData == 1:
            newIndividual['NAME'] = ' '.join(lineSections[2:])
            #---david's addition for sanity---
            curr_ind.name = ' '.join(lineSections[2:])
        elif tag == 'SEX' and readData == 1:
            newIndividual['SEX'] = lineSections[2]
            #---david's addition for sanity---
            curr_ind.sex =  lineSections[2]
        elif tag == 'BIRT' and readData == 1:
            newIndividual['BIRTH'] = {}
            #---david's addition for sanity---
            curr_ind.bday = "XXXXXX"
        elif tag == 'FAMS' and readData == 1:
            newIndividual['FAMS'] = lineSections[2]
            #---david's addition for sanity---
            curr_ind.sfam = lineSections[2]
        elif tag == 'FAMC' and readData == 1:
            newIndividual['FAMC'] = lineSections[2]
            #---david's addition for sanity---
            curr_ind.cfam = lineSections[2]
        elif tag == 'DEAT' and readData == 1:
            newIndividual['DEATH'] = {}
            #---david's addition for sanity---
            curr_ind.dday = "XXXXXX"
        elif tag == 'MARR' and readData == 2:
            newFamily['MARR'] = {}
            #---david's addition for sanity---
            curr_fam.married = "XXXXXX"
        elif tag == 'DIV' and readData == 2:
            newFamily['DIV'] = {}
            #---david's addition for sanity---
            curr_fam.divorced = "XXXXXX"
        elif tag == 'HUSB' and readData == 2:
            newFamily['HUSB'] = lineSections[2]
            #---david's addition for sanity---
            curr_fam.husband = lineSections[2]
        elif tag == 'WIFE' and readData == 2:
            newFamily['WIFE'] = lineSections[2]
            #---david's addition for sanity---
            curr_fam.wife = lineSections[2]
        elif tag == 'CHIL' and readData == 2:
            newFamily['CHIL'] = lineSections[2]
            #---david's addition for sanity---
            curr_fam.children.append(lineSections[2])
    elif level == 2:
        tag = lineSections[1]
        if 'DEATH' in newIndividual:
            if tag == 'DATE':
                newIndividual['DEATH']['DDATE'] = ' '.join(lineSections[2:])
        elif 'BIRTH' in newIndividual:
            if tag == 'DATE':
                newIndividual['BIRTH']['BDATE'] = ' '.join(lineSections[2:])
        if 'DIV' in newFamily:
            if tag == 'DATE':
                newFamily['DIV']['DIVDATE'] = ' '.join(lineSections[2:])
        elif 'MARR' in newFamily:
            if tag == 'DATE':
                newFamily['MARR']['MDATE'] = ' '.join(lineSections[2:])

        #david's additions for sanity{
        if readData == 1:
            if curr_ind.bday == "XXXXXX":
                if tag == 'DATE':
                    curr_ind.bday = ' '.join(lineSections[2:])
            elif curr_ind.dday == "XXXXXX":
                if tag == 'DATE':
                    curr_ind.dday = ' '.join(lineSections[2:])

        if readData == 2:
            if curr_fam.married == "XXXXXX":
                if tag == 'DATE':
                    curr_fam.married = ' '.join(lineSections[2:])
            elif curr_fam.divorced == "XXXXXX":
                if tag == 'DATE':
                    curr_fam.divorced = ' '.join(lineSections[2:])
        #}

#david's additions for sanity{
def findById(given_id, id_type):
    if id_type == 'fam':
        for fam in Families:
            if (fam._id == given_id):
                return fam
        return Family()
    elif id_type == 'ind':
        for ind in Individuals:
            if (ind._id == given_id):
                return ind
        return Individual()

def toString(obj):
    if isinstance(obj, Individual):
        return ("\n id: " + str(obj._id) + "\n name: " + str(obj.name) + "\n bday: " + str(obj.bday))
    elif isinstance(obj, Family):
        children = ""
        for child in obj.children:
            children = children + "\n  " + str(findById(child, "ind").name)
            concat = ("\n id: " + str(obj._id) + "\n married: " + str(obj.married) + "\n divorced: " + str(obj.divorced) + "\n husband: " + str(findById(obj.husband, "ind").name))
            concat = (concat + "\n wife: " + str(findById(obj.wife, "ind").name) + "\n [" + children[3:] + "]")
        return concat
        for ind in Individuals:
            if (ind._id == given_id):
                return ind
    elif isinstance(obj, list):
        string = ""
        for l in obj:
            string = string + ", " + toString(l)
        return ("[" + string[2:] + "]")
    return str(obj)
#}


with open('m5b1_test.ged') as gedcomFile:
    for line in gedcomFile:
        parseFile(line)
    if curr_ind:
        Individuals.append(curr_ind)
        curr_ind = None
    if curr_fam:
        Families.append(curr_fam)
        curr_fam = None

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
    #childrenIDFiltered = childrenString[1:-1]
    childrenIDFiltered = toString(findById(famIDString, "fam").children).replace('@', '')

    print("{:<10} {:<20} {:<20} {:<15} {:<20} {:<10} {:<20} {:<10} ".format(famIDFiltered, marryDate, divorceDate, husbandIDFiltered, husbandName, wifeIDFiltered, wifeName, childrenIDFiltered))

print("")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("")

def checkDates():
    # create a standardized reference for current date
    reference = datetime.today()
    for individual in allIndividuals:
        # get descriptive information needed for output
        indID = individual.get('INDI', '')
        indString = ''.join(indID)
        indIDFiltered = indString[1:-1]
        name = individual.get('NAME', '')

        # get date information and compare with current date
        birth_date = individual.get('BIRTH', {}).get('BDATE', '')
        death_date = individual.get('DEATH', {}).get('DDATE', '')
        birthDay = datetime.strptime(birth_date, "%d %b %Y")
        if ((reference.year < birthDay.year) or (reference.year == birthDay.year and reference.month < birthDay.month) or (reference.year == birthDay.year and reference.month == birthDay.month and reference.day < birthDay.day)):
            print("ERROR in " + indIDFiltered + ": birth of " + name + " on " + birth_date + " is after current date.")
        if death_date:
            deathDay = datetime.strptime(death_date, "%d %b %Y")
            if ((reference.year < deathDay.year) or (reference.year == deathDay.year and reference.month < deathDay.month) or (reference.year == deathDay.year and reference.month == deathDay.month and reference.day < deathDay.day)):
                print("ERROR in " + indIDFiltered + ": death of " + name + " on " + death_date + " is after current date.")

    for family in allFamilies:
        # get descriptive information needed for output
        famID = family.get('FAM', '')
        famIDString = ''.join(famID)
        famIDFiltered = famIDString[1:-1]
        husbandID = family.get('HUSB', '')
        hLookupString = ''.join(husbandID)
        hLookup = int(hLookupString[2:-1]) - 1
        husbandName = allIndividuals[hLookup].get('NAME','')
        wifeID = family.get('WIFE', '')
        wLookupString = ''.join(wifeID)
        wLookup = int(wLookupString[2:-1]) - 1
        wifeName = allIndividuals[wLookup].get('NAME','')
        
        # get date information and compare with current date
        marryDate = family.get('MARR', {}).get('MDATE', '')
        divorceDate = family.get('DIV', {}).get('DIVDATE', '')
        if marryDate:
            marryDay = datetime.strptime(marryDate, "%d %b %Y")
            if ((reference.year < marryDay.year) or (reference.year == marryDay.year and reference.month < marryDay.month) or (reference.year == marryDay.year and reference.month == marryDay.month and reference.day < marryDay.day)):
                print("ERROR in " + famIDFiltered + ": marriage of " + husbandName + " and " + wifeName + " on " + marryDate + " is after current date.")
        if divorceDate:
            divorceDay = datetime.strptime(divorceDate, "%d %b %Y")
            if ((reference.year < divorceDay.year) or (reference.year == divorceDay.year and reference.month < divorceDay.month) or (reference.year == divorceDay.year and reference.month == divorceDay.month and reference.day < divorceDay.day)):
                print("ERROR in " + famIDFiltered + ": divorce of " + husbandName + " and " + wifeName + " on " + divorceDate + " is after current date.")
    
def checkBirthMarriage():
    for family in allFamilies:
        # get descriptive information needed for output
        famID = family.get('FAM', '')
        famIDString = ''.join(famID)
        famIDFiltered = famIDString[1:-1]
        husbandID = family.get('HUSB', '')
        hLookupString = ''.join(husbandID)
        hLookup = int(hLookupString[2:-1]) - 1
        husbandName = allIndividuals[hLookup].get('NAME','')
        wifeID = family.get('WIFE', '')
        wLookupString = ''.join(wifeID)
        wLookup = int(wLookupString[2:-1]) - 1
        wifeName = allIndividuals[wLookup].get('NAME','')

        # get date information and compare
        husbandBirth = allIndividuals[hLookup].get('BIRTH', {}).get('BDATE', '')
        hBirthDay = datetime.strptime(husbandBirth, "%d %b %Y")
        wifeBirth = allIndividuals[wLookup].get('BIRTH', {}).get('BDATE', '')
        wBirthDay = datetime.strptime(wifeBirth, "%d %b %Y")
        marryDate = family.get('MARR', {}).get('MDATE', '')
        if marryDate:
            marryDay = datetime.strptime(marryDate, "%d %b %Y")
            if ((marryDay.year < hBirthDay.year) or (marryDay.year == hBirthDay.year and marryDay.month < hBirthDay.month) or (marryDay.year == hBirthDay.year and marryDay.month == hBirthDay.month and marryDay.day < hBirthDay.day)):
                print("ERROR in " + famIDFiltered + ": marriage of " + husbandName + " and " + wifeName + " on " + marryDate + " is before husband's birth date.")
            elif ((marryDay.year < wBirthDay.year) or (marryDay.year == wBirthDay.year and marryDay.month < wBirthDay.month) or (marryDay.year == wBirthDay.year and marryDay.month == wBirthDay.month and marryDay.day < wBirthDay.day)):
                print("ERROR in " + famIDFiltered + ": marriage of " + husbandName + " and " + wifeName + " on " + marryDate + " is before wife's birth date.")

def checkRelationshipDeath():
    for family in allFamilies:
        # get descriptive information needed for output
        famID = family.get('FAM', '')
        famIDString = ''.join(famID)
        famIDFiltered = famIDString[1:-1]
        husbandID = family.get('HUSB', '')
        hLookupString = ''.join(husbandID)
        hLookup = int(hLookupString[2:-1]) - 1
        husbandName = allIndividuals[hLookup].get('NAME','')
        wifeID = family.get('WIFE', '')
        wLookupString = ''.join(wifeID)
        wLookup = int(wLookupString[2:-1]) - 1
        wifeName = allIndividuals[wLookup].get('NAME','')

        # get date information and compare
        husbandDeath = allIndividuals[hLookup].get('DEATH', {}).get('DDATE', '')
        wifeDeath = allIndividuals[wLookup].get('DEATH', {}).get('DDATE', '')
        marryDate = family.get('MARR', {}).get('MDATE', '')
        divorceDate = family.get('DIV', {}).get('DIVDATE', '')
        if husbandDeath and marryDate:
            hDeathDay = datetime.strptime(husbandDeath, "%d %b %Y")
            marryDay = datetime.strptime(marryDate, "%d %b %Y")
            if ((hDeathDay.year < marryDay.year) or (hDeathDay.year == marryDay.year and hDeathDay.month < marryDay.month) or (hDeathDay.year == marryDay.year and hDeathDay.month == marryDay.month and hDeathDay.day < marryDay.day)):
                print("ERROR in " + famIDFiltered + ": marriage of " + husbandName + " and " + wifeName + " on " + marryDate + " is after husband's death.")
            if divorceDate:
                divorceDay = datetime.strptime(divorceDate, "%d %b %Y")
                if ((hDeathDay.year < divorceDay.year) or (hDeathDay.year == divorceDay.year and hDeathDay.month < divorceDay.month) or (hDeathDay.year == divorceDay.year and hDeathDay.month == divorceDay.month and hDeathDay.day < divorceDay.day)):
                    print("ERROR in " + famIDFiltered + ": divorce of " + husbandName + " and " + wifeName + " on " + divorceDate + " is after husband's death.")
        elif wifeDeath and marryDate:
            wDeathDay = datetime.strptime(wifeDeath, "%d %b %Y")
            marryDay = datetime.strptime(marryDate, "%d %b %Y")
            if ((wDeathDay.year < marryDay.year) or (wDeathDay.year == marryDay.year and wDeathDay.month < marryDay.month) or (wDeathDay.year == marryDay.year and wDeathDay.month == marryDay.month and wDeathDay.day < marryDay.day)):
                print("ERROR in " + famIDFiltered + ": marriage of " + husbandName + " and " + wifeName + " on " + marryDate + " is after wife's death.")
            if divorceDate:
                divorceDay = datetime.strptime(divorceDate, "%d %b %Y")
                if ((wDeathDay.year < divorceDay.year) or (wDeathDay.year == divorceDay.year and wDeathDay.month < divorceDay.month) or (wDeathDay.year == divorceDay.year and wDeathDay.month == divorceDay.month and wDeathDay.day < divorceDay.day)):
                    print("ERROR in " + famIDFiltered + ": divorce of " + husbandName + " and " + wifeName + " on " + divorceDate + " is after wife's death.")

def checkMarriageDivorce(family):
    famID = family.get('FAM', '')
    famIDString = ''.join(famID)
    famIDFiltered = famIDString[1:-1]
    husbandID = family.get('HUSB', '')
    hLookupString = ''.join(husbandID)
    hLookup = int(hLookupString[2:-1]) - 1
    husbandName = allIndividuals[hLookup].get('NAME','')
    wifeID = family.get('WIFE', '')
    wLookupString = ''.join(wifeID)
    wLookup = int(wLookupString[2:-1]) - 1
    wifeName = allIndividuals[wLookup].get('NAME','')    
    marryDate = family.get('MARR', {}).get('MDATE', '')
    divorceDate = family.get('DIV', {}).get('DIVDATE', '')
    if marryDate and divorceDate:
        marryDay = datetime.strptime(marryDate, "%d %b %Y")
        divorceDay = datetime.strptime(divorceDate, "%d %b %Y")
        if (marryDay > divorceDay):
            return "ERROR in " + famIDFiltered + ": divorce of " + husbandName + " and " + wifeName + " on " + divorceDate + " is before their marriage date."
        else:
            return 'None'
    else: 
        return 'None'


def checkBirthDeath(individual):
    indID = individual.get('INDI', '')
    indString = ''.join(indID)
    indIDFiltered = indString[1:-1]
    name = individual.get('NAME', '')
    birthDate = individual.get('BIRTH', {}).get('BDATE', '')
    deathDate = individual.get('DEATH', {}).get('DDATE', '')
    if birthDate and deathDate:
        birthDay = datetime.strptime(birthDate, "%d %b %Y")
        deathDay = datetime.strptime(deathDate, "%d %b %Y")
        if (birthDay > deathDay):
            return "ERROR in " + indIDFiltered + ": death of " + name + " on " + deathDate + " is before their birth date."
        else:
            return 'None'
    else:
        return 'None'

def checkBigamy():
    seenIds = []
    for fam in Families:
        if fam.divorced:
            pass
        else:
            try:
                if (seenIds.index(fam.husband) > -1):
                    print("ERROR in " + fam._id[1:-1] + ": " + findById(fam.husband, 'ind').name + " is married to both " + findById(fam.wife, 'ind').name + " and another individual")
            except ValueError:
                seenIds.append(fam.husband)

            try:
                if (seenIds.index(fam.wife) > -1):
                    print("ERROR in " + fam._id[1:-1] + ": " + findById(fam.wife, 'ind').name + " is married to both " + findById(fam.husband, 'ind').name + " and another individual")
            except ValueError:
                seenIds.append(fam.wife)


def checkBirths():
    seenIds = []
    births = 5
    for fam in Families:
        if len(fam.children) > births:
            print("ERROR in " + fam._id[1:-1] + ": this family has more than " + str(births) + " births")

checkBirths()
checkBigamy()
checkDates()
checkBirthMarriage()
checkRelationshipDeath()

for individual in allIndividuals:
    if (checkBirthDeath(individual)!='None'):
        print(checkBirthDeath(individual))
for family in allFamilies:
    if (checkMarriageDivorce(family)!='None'):
        print(checkBirthDeath(family))
