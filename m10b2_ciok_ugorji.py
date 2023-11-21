# auth: evan ciok & chibunnam ugorji
# course: ssw/css 555
# assignment: m8.b1

from datetime import datetime
import sys
##########---------------------Classes & Lists------------------------------------
class Individual:
    _id = "XX"
    sex = "X"
    name = "XXXXXX /XXXX/"
    fname = "XXXX"
    given_lname = "XXXX"
    lname = "XXXX"
    bday = None
    dday = ''
    cfam = ''
    sfam = ''

class Family:
    _id = "XX"
    married = ''
    divorced = ''
    wife = "XXX"
    husband = "XXX"
    children = None

Individuals = []
Families = []
curr_ind = None
curr_fam = None
readData = 0
indIDs = []
famIDs = []

##########--------------------------------------------------------------------------------

#parses through gedcom file
def parseFile(file):
    global curr_ind
    global curr_fam
    global readData
    
    for line in file:
        fullLine = line.strip()
        lineSections = fullLine.split()
        level = int(lineSections[0])

        #read tag level 0
        if level == 0 and len(lineSections) > 2:
            tag = lineSections[2]
            cleanup = 0
            while cleanup == 0:
                if curr_ind:
                    Individuals.append(curr_ind)
                curr_ind = None

                if curr_fam:
                    Families.append(curr_fam)
                curr_fam = None
                cleanup = 1
            if tag == 'INDI':
                readData = 1
                curr_ind = Individual()
                curr_ind._id = lineSections[1]
                indIDs.append(lineSections[1])
            elif tag == 'FAM':
                readData = 2
                curr_fam = Family()
                curr_fam.children = []
                curr_fam._id = lineSections[1]
                famIDs.append(lineSections[1])
            else:
                readData = 0
    
        #read tag level 1
        elif level == 1:
            tag = lineSections[1] 
            if tag == 'NAME' and readData == 1:
                curr_ind.name = ' '.join(lineSections[2:])
            elif tag == 'SEX' and readData == 1:
                curr_ind.sex =  lineSections[2]
            elif tag == 'BIRT' and readData == 1:
                curr_ind.bday = "XXXXXX"
            elif tag == 'FAMS' and readData == 1:
                curr_ind.sfam = lineSections[2]
            elif tag == 'FAMC' and readData == 1:
                curr_ind.cfam = lineSections[2]
            elif tag == 'DEAT' and readData == 1:
                curr_ind.dday = "XXXXXX"
            elif tag == 'MARR' and readData == 2:
                curr_fam.married = "XXXXXX"
            elif tag == 'DIV' and readData == 2:
                curr_fam.divorced = "XXXXXX"
            elif tag == 'HUSB' and readData == 2:
                curr_fam.husband = lineSections[2]
            elif tag == 'WIFE' and readData == 2:
                curr_fam.wife = lineSections[2]
            elif tag == 'CHIL' and readData == 2:
                curr_fam.children.append(lineSections[2])

        #read tag level 2
        elif level == 2:
            tag = lineSections[1]
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

  #Cleanup floating objects                
    if curr_ind:
        Individuals.append(curr_ind)
        curr_ind = None
    if curr_fam:
        Families.append(curr_fam)
        curr_fam = None
        

##########---------------------------Helper Functions---------------------------------------------

#searches given id and returns corresponding individual/family
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

#finds age based on given birth and death dates
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

#converts given object to a predetermined string format
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

#checks date for legitimacy
def checkDate(dateRaw):
    date = dateRaw.split(' ')
    month = date[1]
    day = int(date[0])
    if month == 'JAN':
        if day > 31:
            return False
        else:
            return True
    elif month == 'FEB':
        if day > 28:
            return False
        else:
            return True
    elif month == 'MAR':
        if day > 31:
            return False
        else:
            return True
    elif month == 'APR':
        if day > 30:
            return False
        else:
            return True
    elif month == 'MAY':
        if day > 31:
            return False
        else:
            return True
    elif month == 'JUN':
        if day > 30:
            return False
        else:
            return True
    if month == 'JUL':
        if day > 31:
            return False
        else:
            return True
    elif month == 'AUG':
        if day > 31:
            return False
        else:
            return True
    elif month == 'SEP':
        if day > 30:
            return False
        else:
            return True
    elif month == 'OCT':
        if day > 31:
            return False
        else:
            return True
    elif month == 'NOV':
        if day > 30:
            return False
        else:
            return True
    elif month == 'DEC':
        if day > 31:
            return False
        else:
            return True
    else:
        return False

#takes in a list of tuples. Finds pivot
def sortPairs(data):
    if(len(data) < 2):
        return data
    pivot = data[-1][1]
    ldata = []
    rdata = []
    for pair in data:
        if (pair[1] < pivot):
            ldata.append(pair)
        if (pair[1] > pivot):
            rdata.append(pair)
    ldata = sortPairs(ldata)
    rdata = sortPairs(rdata)
    return [*ldata, pair, *rdata]

#sorts ids by age (using a quicksort helper)
def sortByAge(group):
    listed = []
    counter = 0
    for individual in group:
        ind = individual
        if not type(individual) is Individual:
            ind = findById(individual, "ind")
        listed.append((ind._id, findAge(ind.bday, ind.dday)))
        counter += 1
    sys.setrecursionlimit(3000)
    sortedList = sortPairs(listed)
    return sortedList

##########----------------------------------------------------------------------------------------

#opens specified gedcom file
with open('p3_test.ged') as gedcomFile:
    parseFile(gedcomFile)

print("{:<10} {:<20} {:<5} {:<15} {:<5} {:<10} {:<15} {:<10} {:<10}".format("ID", "Name", "Sex", "Birthday", "Age", "Status", "Death", "Child", "Spouse"))
for ind in Individuals:
    age = findAge(ind.bday, ind.dday)
    status = "Alive" if not ind.dday else "Deceased"

    string = "{:<10} {:<20} {:<5} {:<15} {:<5} {:<10} {:<15} {:<10} {:<10}"
    string = string.format(str(ind._id.replace('@', '')), str(ind.name), str(ind.sex), str(ind.bday), age, status, str(ind.dday), str(ind.cfam.replace('@', '')), str(ind.sfam.replace('@', '')))
    print(string)
          
print("")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("")

print("{:<10} {:<20} {:<20} {:<15} {:<20} {:<10} {:<20} {:<10} ".format("ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"))
for fam in Families:
    childrenIDs = toString(findById(fam._id, "fam").children).replace('@', '')
    
    string = "{:<10} {:<20} {:<20} {:<15} {:<20} {:<10} {:<20} {:<10} "
    string = string.format(str(fam._id.replace('@', '')), str(fam.married), str(fam.divorced), str(fam.husband.replace('@', '')), str(findById(fam.husband, "ind").name), str(fam.wife.replace('@', '')), str(findById(fam.wife, "ind").name), childrenIDs)     

    print(string)

print("")
print("----------------------------------------------------------------------------------------------------------------------------------")
print("")

def checkDates():
    # create a standardized reference for current date
    reference = datetime.today()
    for individual in Individuals:
        # format date information and compare with current date
        birthDay = datetime.strptime(individual.bday, "%d %b %Y")
        if (reference < birthDay):
            print("ERROR in " + individual._id[1:-1]  + ": birth of " + individual.name + " on " + individual.bday + " is after current date.")
        if individual.dday:
            deathDay = datetime.strptime(individual.dday, "%d %b %Y")
            if (reference < deathDay):
                print("ERROR in " + individual._id[1:-1]  + ": death of " + individual.name + " on " + individual.dday + " is after current date.")

    for family in Families:
        # get relevant individual information
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")
        
        # format date information and compare with current date
        if family.married:
            marryDay = datetime.strptime(family.married, "%d %b %Y")
            if (reference < marryDay):
                print("ERROR in " + family._id[1:-1] + ": marriage of " + husband.name + " and " + wife.name + " on " + family.married + " is after current date.")
        if family.divorced:
            divorceDay = datetime.strptime(family.divorced, "%d %b %Y")
            if (reference < divorceDay):
                print("ERROR in " + family._id[1:-1] + ": divorce of " + husband.name + " and " + wife.name + " on " + family.divorced + " is after current date.")
    
def checkBirthMarriage():
    for family in Families:
         # get relevant individual information
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")

        # format date information and compare
        hBirthDay = datetime.strptime(husband.bday, "%d %b %Y")
        wBirthDay = datetime.strptime(wife.bday, "%d %b %Y")
        if family.married:
            marryDay = datetime.strptime(family.married, "%d %b %Y")
            if (marryDay < hBirthDay):
                print("ERROR in " + family._id[1:-1] + ": marriage of " + husband.name + " and " + wife.name + " on " + family.married + " is before husband's birth date.")
            elif (marryDay < wBirthDay):
                print("ERROR in " + family._id[1:-1] + ": marriage of " + husband.name + " and " + wife.name + " on " + family.married + " is before wife's birth date.")

def checkRelationshipDeath():
    for family in Families:
        # get relevant individual information
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")

        # format date information and compare
        if husband.dday and family.married:
            hDeathDay = datetime.strptime(husband.dday, "%d %b %Y")
            marryDay = datetime.strptime(family.married, "%d %b %Y")
            if (hDeathDay < marryDay):
                print("ERROR in " + family._id[1:-1] + ": marriage of " + husband.name + " and " + wife.name + " on " + family.married + " is after husband's death.")
            if family.divorced:
                divorceDay = datetime.strptime(family.divorced, "%d %b %Y")
                if (hDeathDay < divorceDay):
                    print("ERROR in " + family._id[1:-1] + ": divorce of " + husband.name + " and " + wife.name + " on " + family.divorced + " is after husband's death.")
        elif wife.dday and family.married:
            wDeathDay = datetime.strptime(wife.dday, "%d %b %Y")
            marryDay = datetime.strptime(family.married, "%d %b %Y")
            if (wDeathDay < marryDay):
                print("ERROR in " + family._id[1:-1] + ": marriage of " + husband.name + " and " + wife.name + " on " + family.married + " is after wife's death.")
            if family.divorced:
                divorceDay = datetime.strptime(family.divorced, "%d %b %Y")
                if (wDeathDay < divorceDay):
                    print("ERROR in " + family._id[1:-1] + ": divorce of " + husband.name + " and " + wife.name + " on " + family.divorced + " is after wife's death.")

def checkMarriageDivorce(family):
    # get relevant individual information
    husband = findById(family.husband, "ind")
    wife = findById(family.wife, "ind")

    # format date information and compare
    if family.married and family.divorced:
        marryDay = datetime.strptime(family.married, "%d %b %Y")
        divorceDay = datetime.strptime(family.divorced, "%d %b %Y")
        if (marryDay > divorceDay):
            return "ERROR in " + family._id[1:-1] + ": divorce of " + husband.name + " and " + wife.name + " on " + family.divorced + " is before their marriage date."
        else:
            return 'None'
    else: 
        return 'None'


def checkBirthDeath(individual):
    # format date information and compare
    if individual.bday and individual.dday:
        birthDay = datetime.strptime(individual.bday, "%d %b %Y")
        deathDay = datetime.strptime(individual.dday, "%d %b %Y")
        if (birthDay > deathDay):
            return "ERROR in " + individual._id[1:-1]  + ": death of " + individual.name + " on " + individual.dday + " is before their birth date on " + individual.bday + "." 
        else:
            return 'None'
    else:
        return 'None'

def checkBigamy():
    # init marriage pair list
    seenPairs = {}
    for family in Families:
        # get relevant individual information
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")

        # format relevant date information and compare
        if family.divorced:
            pass
        elif family.married:
            marryDay = datetime.strptime(family.married, "%d %b %Y")
             
            # check husband for bigamy
            if seenPairs.get(husband._id):
                err = "ERROR in " + family._id[1:-1] + ": " + husband.name + " was/is married to " + wife.name + " when already married to " + seenPairs.get(husband._id)[0].name + "."
                if seenPairs.get(husband._id)[0].dday:
                    hDeathDay = datetime.strptime((seenPairs.get(husband._id)[0]).dday, "%d %b %Y")
                    if hDeathDay > marryDay:
                      print(err)
                if husband.dday:
                    hDeathDay = datetime.strptime(wife.dday, "%d %b %Y")
                    if hDeathDay > seenPairs.get(husband._id)[1]:
                      print(err) 
                else:
                    print(err)

            # check wife for biandry
            if seenPairs.get(wife._id):
                err = "ERROR in " + family._id[1:-1] + ": " + wife.name + " was/is married to " + husband.name + " when already married to " + seenPairs.get(wife._id)[0].name + "."
                if seenPairs.get(wife._id)[0].dday:
                    hDeathDay = datetime.strptime((seenPairs.get(wife._id)[0]).dday, "%d %b %Y")
                    if hDeathDay > marryDay:
                      print(err)
                if husband.dday:
                    hDeathDay = datetime.strptime(husband.dday, "%d %b %Y")
                    if hDeathDay > seenPairs.get(wife._id)[1]:
                      print(err) 
                else:
                    print(err)

            # update marriage pair list
            seenPairs[husband._id] = [wife, marryDay]
            seenPairs[wife._id] = [husband, marryDay]
    seenPairs = ''

def checkBirths():
    births = 5
    for family in Families:
        if len(family.children) > births:
            print("ERROR in " + family._id[1:-1] + ": this family has more than " + str(births) + " births")

def listMarried(family):
    if family.divorced:
        return 'None'
    elif family.married:
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")
        if husband.dday or wife.dday:
            return 'None'
        else:
            return husband.name + " and " + wife.name + " are married."
    else:
        return 'None'
    
def listSingle(individual):
    age = findAge(individual.bday, individual.dday)
    if individual.sfam:
        return 'None'
    elif age >= 30:
        return individual.name + " is " + str(age) + " years old and single."
    else:
        return 'None'

def checkMarryDescendant(family):
    husband = findById(family.husband, "ind")
    wife = findById(family.wife, "ind")
    if husband.cfam == wife.sfam or husband.sfam == wife.cfam:
        return 'Error in ' + family._id + ': invalid marriage to descendant.'
    else:
        return 'None'

def checkDuplicateInd(individual):
    count = 0
    for id in indIDs:
        if id == individual._id:
            count+=1
    if count >= 2:
        return 'Error: duplicate individual ID ' + individual._id[1:-1]
    else:
        return 'None'
    
def checkDuplicateFam(family):
    countfam = 0
    for id in famIDs:
        if id == family._id:
            countfam+=1
    if countfam >= 2:
        return 'Error: duplicate family ID ' + family._id[1:-1]
    else:
        return 'None'

def listSiblings(family):
    last = len((family.children))-1

    if (last == 0):
        print(findById(family.children[0], "ind").name + " is an only child.")
        return 0
    sortedList = sortByAge(family.children)
    string = ""
    counter = 0
    sortedList.reverse()
    for pair in sortedList:
        sib = findById(pair[0], "ind")
        if (counter == last):
            string += "and " + sib.name + "(age " + str(pair[1]) + ")"
        else:
            string += sib.name + "(age " + str(pair[1])  + ")"
            if (last > 1):
                string += ","
            string += " "
            counter += 1
    print(string + " are siblings.")

def listOrphans():
    string = ""
    counter = 0
    for family in Families:
        husband = findById(family.husband, "ind")
        wife = findById(family.wife, "ind")
        if(husband.dday != '' and wife.dday != ''):
            for unit in family.children:
                child = findById(unit, "ind")
                if(findAge(child.bday, child.dday) < 18):
                    string = string.replace('+', ',') + "+ " + child.name
                    counter += 1

    if counter > 1:
        string = string[2:].replace('+', ', and') + " are orphans."
    if counter == 1:
        string = string[2:] + " is an orphan."

    print(string)
###---------------Calls-----------------
checkBirths()
checkBigamy()
checkDates()
checkBirthMarriage()
checkRelationshipDeath()
listOrphans()

for individual in Individuals:
    err = checkBirthDeath(individual)
    if (err !='None'):
        print(err)
    err2 = listSingle(individual)
    if (err2 != 'None'):
        print(err2)
    err3 = checkDuplicateInd(individual)
    if (err3 != 'None'):
        print(err3)
for family in Families:
    err = checkMarriageDivorce(family)
    if (err !='None'):
        print(err)
    err2 = listMarried(family)
    if (err2 !='None'):
        print(err2)
    err3 = checkMarryDescendant(family)
    if (err3 !='None'):
        print(err3)
    err4 = checkDuplicateFam(family)
    if (err4 !='None'):
        print(err4)

    try:    
        listSiblings(family)
    except Exception as e:
        print(str(e))

