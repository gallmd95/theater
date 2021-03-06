from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import WebDriverException
import csv
import os
import glob
import nltk
import re
from nameparser.parser import HumanName

DRIVER_PATH = os.getcwd()+'/chromedriver'

def getLinks(driver, school):
    driver.get("https://google.com")
    sleep(2)
    driver.find_element_by_id('lst-ib').send_keys(school + ' theater people', Keys.RETURN)
    sleep(2)
    result = driver.find_elements_by_xpath("//div[@class='rc']")[0]
    result.find_element_by_xpath("./h3/a").click()
    sleep(3)
    return driver.current_url.encode('utf-8')

def sel2(driver, url):
    driver.get(url)
    sleep(3)
    return driver.page_source.encode('utf-8')

schools = []
s = ['University of California, Berkeley',
    'Princeton University',
    'California Institute of Technology',
    'Columbia University',
    'University of California, Los Angeles',
    'Cornell University',
    'University of California, San Diego',
    'Michigan State University',
    'Baylor College of Medicine',
    'Case Western Reserve University',
    'Emory University',
    'Georgia Institute of Technology',
    'Icahn School of Medicine at Mount Sinai',
    'The University of Texas M. D. Anderson Cancer Center',
    'Tufts University',
    'University of Rochester',
    'University of Virginia',
    'George Mason University',
    'Iowa State University',
    'Oregon Health and Science University',]

"""
def getData():
    with open('lyssdata.csv', 'r') as data:
        reader = csv.reader(data, delimiter=',')
        for row in reader:
            schools.append(row[2])

    driver = webdriver.Chrome(DRIVER_PATH)
    try:
        for school in schools:
            with open(school+'.txt', 'wb') as emailfile:
                try:
                    #emailfile.write(sel2(driver, school))
                except WebDriverException as e:
                    print school
                    print e
    finally:
        driver.close()
"""

def get_human_names(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []

    return (person_list)

def getEmails():
    emails = {}
    for filename in glob.glob('*.txt'):
        with open(filename, 'r') as tempfile:
            name = filename[:-4]
            emails[name] = {}
            emails[name]['count'] = 0
            emails[name]['emails'] = []
            for line in tempfile:
                if 'mailto:' in line:
                    start = line.index('mailto:') + 7
                    firstend = line.find('"',start)
                    secondend = line.find("'",start)
                    end = firstend if firstend > start and (firstend < secondend or secondend < 0) else secondend
                    if (end - start) < 100 and (end - start) > 0:
                        email = line[start:end]
                        if(' ' in  email):
                            email = email[:email.index(' ')]
                        emails[name]['count']+=1
                        emails[name]['emails'].append(email)
    return emails

def getNames():
    forbidden = [
        'Google',
        'Facebook',
        'Twitter',
        'View',
        'See',
        'Picture',
        'Opportun',
        'College',
        'University',
        'Accept',
        'Student',
        'Affair',
        'Alum',
        'Content',
        'Public',
        'Settings',
        'Associat',
        'Program',
        'Slide',
        'Instit',
        'Icon',
        'Naviga',
        'Museu',
        'Info',
        'Incom',
        'Mounta',
        'Stateme',
        'Mech',
        'Fellow',
        'Boston',
        'Prod',
        'Arts',
        'History',
        'Math',
        'Langua',
        'Theater',
        'Menu',
        'Play',
        'Button'
    ]
    transforms = [
        [],
        [],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@case.edu'],
        [],
        [],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@duke.edu'],
        [],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@gmu.edu'],
        [],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@fas.harvard.edu'],
        [],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@indiana.edu'],
        [],
        [],
        [],
        [],
        [],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@nyu.edu'],
        [],
        [lambda x: x.split(' ')[0][0].lower()+'-'+x.split(' ')[-1].lower()+'@northwestern.edu',lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@northwestern.edu',lambda x: x.split(' ')[0].lower()+'-'+x.split(' ')[-1].lower()+'@northwestern.edu',lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@northwestern.edu'],
        [],
        [],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@stanford.edu',lambda x: x.split(' ')[-1].lower()+'@stanford.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@tamu.edu',lambda x: x.split(' ')[-1].lower()+'@tamu.edu'],
        [],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@tufts.edu'],
        [lambda x: x.split(' ')[0].lower()+x.split(' ')[-1].lower()+'@berkeley.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@ucla.edu'],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@ucr.edu',lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@ucr.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@ucsd.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@usfca.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@uchicago.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@illinois.edu'],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@theater.umass.edu'],
        [],
        [],
        [],
        [lambda x: x.split(' ')[0][0].lower()+'.'+x.split(' ')[-1].lower()+'@sas.upenn.edu'],
        [lambda x: x.split(' ')[0][0].lower()+'.'+x.split(' ')[-1].lower()+'@rochester.edu'],
        [],
        [],
        [],
        [lambda x: x.split(' ')[0][0].lower()+x.split(' ')[-1].lower()+'@wisc.edu'],
        [lambda x: x.split(' ')[0][0].lower()+'.'+x.split(' ')[-1].lower()+'@wustl.edu'],
        [lambda x: x.split(' ')[0].lower()+'.'+x.split(' ')[-1].lower()+'@yale.edu']
    ]
    names = {}
    ind = 0
    for filename in sorted(glob.glob('*.txt')):
        name = filename[:-4]
        with open(filename, 'r') as tempfile:
            names[name] = {}
            names[name]['count'] = 0
            names[name]['names'] = []
            names[name]['emails'] = []
            if len(transforms[ind]) > 0:
                for line in [re.sub(r'[^\x00-\x7F]+',' ', x) for x in tempfile.readlines()]:
                    for each in get_human_names(line):
                        if all(x not in each for x in forbidden):
                            names[name]['count'] +=1
                            names[name]['names'].append(each)
                            for f in transforms[ind]:
                                names[name]['emails'].append(f(each))
        ind +=1
    return names
                        
def getUrls():
    links = [
        ('Johns Hopkins University','http://krieger.jhu.edu/theatre-arts/people/'),
        #('University of Michigan-Ann Arbor','http://smtd.umich.edu/faculty_staff/index_dept.php'),
        ('Michigan State University','http://theatre.msu.edu/people/faculty-staff/'),
        ('Yale University','https://theaterstudies.yale.edu/people'),
        ('University of Minnesota, Twin Cities','https://cla.umn.edu/theatre/people/staff'),
        ('University of Minnesota, Twin Cities','https://cla.umn.edu/theatre/people/faculty'),
        ('University of Virginia','http://drama.virginia.edu/staff'),
        ('University of Virginia','http://drama.virginia.edu/grad-ta'),
        ('University of Virginia','http://drama.virginia.edu/emeritus-faculty'),
        ('University of Virginia','http://drama.virginia.edu/faculty'),
    ]

    driver = webdriver.Chrome(DRIVER_PATH)
    try:
        for link in links:
            with open(link[0]+'.txt', 'ab') as emailfile:
                try:
                    emailfile.write(sel2(driver, link[1]))
                except WebDriverException as e:
                    print link[0]
                    print e

    finally:
        driver.close()

    emails = {}
    for link in links:
        with open(link[0]+'.txt', 'r') as tempfile:
            name = link[0]
            emails[name] = {}
            emails[name]['count'] = 0
            emails[name]['emails'] = []
            for line in tempfile:
                if 'mailto:' in line:
                    start = line.index('mailto:') + 7
                    end = line.index('"',start)
                    if (end - start) < 100 and (end - start) > 0:
                        email = line[start:end]
                        if(' ' in  email):
                            email = email[:email.index(' ')]
                        emails[name]['count']+=1
                        emails[name]['emails'].append(email)
    return emails

def getPrint():
    emails = getNames()
    print emails
    for key in emails.keys():
        print key
        for each in list(set(emails[key]['emails'])):
            print each

def fillFiles(driver, urls):
    driver = webdriver.Chrome(DRIVER_PATH)
    urls = [
        ('Johns Hopkins University','http://krieger.jhu.edu/theatre-arts/people/'),
        ('Michigan State University','http://theatre.msu.edu/people/faculty-staff/'),
        ('Yale University','https://theaterstudies.yale.edu/people'),
        ('University of Minnesota, Twin Cities','https://cla.umn.edu/theatre/people/staff'),
        ('University of Minnesota, Twin Cities','https://cla.umn.edu/theatre/people/faculty'),
        ('University of Virginia','http://drama.virginia.edu/staff'),
        ('University of Virginia','http://drama.virginia.edu/grad-ta'),
        ('University of Virginia','http://drama.virginia.edu/emeritus-faculty'),
        ('University of Virginia','http://drama.virginia.edu/faculty'),
        ('University of Washington','https://drama.washington.edu/people/faculty'),
    ]
    schools = []
    with open('lyssdata.csv', 'r') as data:
            reader = csv.reader(data, delimiter=',')
            for row in reader:
                schools.append(row[2])

    for each in schools:
        urls.append((each, getLinks(driver, each)))

    for each in urls:
        with open(each[0]+'.txt', 'ab') as emailfile:
                    try:
                        driver.get(each[1])
                        sleep(4)
                        emailfile.write(driver.page_source.encode('utf-8'))
                    except WebDriverException as e:
                        print each
                        print e

    driver.close()   

def doIt():
    for each in names.keys():
        emails[each]['guesses'] = []
        for guess in names[each]['emails']:
            emails[each]['guesses'].append(guess)

    with open(os.getcwd()+"/results/results.txt", "wb") as file:
        for each in emails.keys():
            print each
            file.write(each+'\n')
            print '100%'
            file.write('100%\n')
            emails[each]['emails'] = list(set(emails[each]['emails']))
            emails[each]['guesses'] = list(set(emails[each]['guesses']))
            numberreal = len(emails[each]['emails'])
            for count in xrange(50):
                if count < numberreal:
                    print emails[each]['emails'][count]
                    file.write(emails[each]['emails'][count]+'\n')
                elif count >= numberreal:
                    if count == numberreal:
                        print "50-50"
                        file.write("50-50\n")
                    if count - numberreal < len(emails[each]['guesses']):
                        print emails[each]['guesses'][count-numberreal]
                        file.write(emails[each]['guesses'][count-numberreal]+"\n")
                    else:
                        break

emails = getEmails() 

names = getNames()

doIt()

                    
