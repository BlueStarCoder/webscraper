import os
import sys
from PyQt5.QtWidgets import QApplication
#from PyQt5.QtGui import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKitWidgets import QWebPage
import bs4 as bs
import urllib
import urllib2
from mysql.connector import MySQLConnection, Error
# import urllib2.Request
#import urllib.request

class Client(QWebPage):
    def __init__(self, url):
         self.app = QApplication(sys.argv)
         QWebPage.__init__(self)
         self.loadFinished.connect(self.on_page_load)
         self.mainFrame().load(QUrl(url))
         self.app.exec_()
    
    def on_page_load(self):
           self.app.quit()

# database configurations
db_config = {
  'user': 'scrapeuser',
  'password': 'searchpass',
  'host': '127.0.0.1',
  'database': 'scraper',
  'raise_on_warnings': True,
}

# directory structure should contain a colleges folder and a recruiters inside the main folder:
# For Example :
# images
#      -colleges
#      -recruiters

# directory name here where you want to store college faculties and recruiters
imagesfolderpath = "images"

os.chdir(imagesfolderpath)

# create college directory or folder structure for saving images
def collegeDirectory(college):
    os.chdir("colleges")
    if not os.path.exists(college):
        os.mkdir(college)
        # create faculties folder inside college folder
        os.mkdir(os.path.join(college,"faculties"))
        # create recruiters folder inside college folder
        # os.mkdir(os.path.join(college,"recruiters"))
    os.chdir("..")


def downloadData(dataUrl, imgname):
    urllib.urlretrieve(dataUrl, imgname)

# old url
url = ''
collegenamefromurl = os.path.basename(url)
client_response = Client(url)
source = client_response.mainFrame().toHtml()
soup = bs.BeautifulSoup(source, 'lxml')

collegeName = soup.findAll('strong')[0].get_text().strip()
print "College Name : " + collegeName
coursename = soup.findAll('strong')[1].get_text().strip()
print "Degree Detail : " + coursename

# this get the percent from span tag.
courseperc = soup.find('span', class_='perc').get_text().strip()
print "Percent : " + courseperc

# Print the fees details.
coursefees = soup.findAll('p', class_='mg-0')[2].get_text().strip()
print coursefees

# print dir(soup.findAll('strong')[1])
yrstotalseats = soup.findAll('strong')[1].find_next().text.encode('utf-8').strip().split("\n")
courseperiod = yrstotalseats[0].strip()
try:
    coursetotalseats = yrstotalseats[1].strip()
except:
    coursetotalseats = " "
print "Years       : " + courseperiod 
print "Total Seats : " + coursetotalseats

# Download faculty details
facultyinfo = soup.findAll("div", {"class":"pd-btm10 pd-top10"})

# print facultyinfo[0].find('span', class_="font13 pd-top10").get_text().strip()
facultyName = facultyinfo[1].findAll('h5')
facultyImg = facultyinfo[1].findAll('img')
facultyPosition = facultyinfo[1].findAll('p')

for i in range(0,len(facultyinfo[1].findAll('h5'))):
    print "Faculty Name : " + facultyName[i].get_text().strip() + " Faculty Position : " + facultyPosition[i].get_text().strip() + "\nFaculty ImageUrl : " + facultyImg[i]['data-src']

collegeScoreDetails = soup.findAll("a", id="cs_score")[0].findNextSibling().findAll('span', class_='perc')

print "CollegeSearch Score"
overallscore = collegeScoreDetails[0].get_text().strip()
print "Overall Score : " + overallscore
placement = collegeScoreDetails[2].get_text().strip()
print "Placement     : " + placement
campus = collegeScoreDetails[4].get_text().strip()
print "Campus        : " + campus
faculty = collegeScoreDetails[6].get_text().strip()
print "Faculty       : " + faculty
reputation = collegeScoreDetails[8].get_text().strip()
print "Reputation    : " + reputation

otherCourses = soup.findAll('div', class_='pless')
for col in otherCourses:
    print "other course name : " + col.find('strong').get_text().strip()
    print "other course period : " + col.find(class_='mg-0').find('span').get_text().strip()
    print "other course fees : " + col.find(class_='font11').findPrevious().get_text().strip() + " (Total Fees)"
    print "other course perc : " + col.find('span', class_='perc').get_text().strip()

collegeaddress = soup.find('div', id='contactDiv').findNextSibling().find(class_='font12').get_text().strip()
collegeemail = soup.find('div', id='contactDiv').findAll('span')[2].get_text().strip()
print "College email : " + collegeemail
print "College Address : " + collegeaddress 
# facilities available
print "{:*^39}".format('text start')
facility = soup.find('div', id='facility').findAll('div', class_='category-title')
i = 0
for facilit in facility:
    print facility[i].get_text().strip()
    i += 1
print "{:*^39}".format('text end')

publicorprivate = soup.find('div', id='facility').findNextSibling().find('h5').get_text().strip()
publicorprivate = " ".join(publicorprivate.split())
print "public : " + publicorprivate

try:
    autonomousornot = soup.find('div', id='facility').findNextSibling().findNextSibling().find('h5').get_text().strip()
except:
    autonomousornot = " "
print "autonomous : " + autonomousornot

try:
    affiliedby = soup.find('div', id='facility').findNextSibling().findNextSibling().findNextSibling().find('h5').get_text().strip()
except:
    affiliedby = " "
print "affiliedby : " + affiliedby

salaryDetails = soup.findAll('h5', class_='course-heading')
highPay = soup.findAll('span', class_='placement-figures-count-high')
avgPay = soup.findAll('span', class_='placement-figures-count-average')

collegesalary = salaryDetails[0].get_text().strip()
collegeavgpay = avgPay[0].get_text().strip()
collegehighpay = highPay[0].get_text().strip()

industrysalary = salaryDetails[1].get_text().strip()
industryavgpay = avgPay[1].get_text().strip()
industryhighpay = highPay[1].get_text().strip()

print salaryDetails[0].get_text().strip() + "\nHighest Salary : " + highPay[0].get_text().strip() + "\nAverage Salary : " + avgPay[0].get_text().strip()
print salaryDetails[1].get_text().strip() + "\nHighest Salary : " + highPay[1].get_text().strip() + "\nAverage Salary : " + avgPay[1].get_text().strip()

print "{:=^39}".format('College Recruitment Images Url')
# Download images of college recruiters.
url = ''
html = urllib2.urlopen(url)
soup = bs.BeautifulSoup(html, 'lxml')

divimgs = soup.findAll("div", {"class":"recuitor-individual rec-block-a"})

def InsertIntoDatabase(query, args):
    try:
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

def CheckRow(args):
    query = "SELECT * from recruiters where name='{}'".format(args)
    rvalue = True
    try:
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query)

        cursor.fetchall()
        print "rowcount : " + str(cursor.rowcount)
 
        if cursor.rowcount == 0:
            rvalue = False

    except Error as error:
        print(error)
 
    finally:
        conn.close()
        return rvalue

def insertcollege(name, address, email, autonornot, puborpriv, affilied):
    query = "INSERT INTO colleges(name, address, email, autonomousornot, privateorpublicinstitute, affiliedby) " \
            "VALUES(%s,%s,%s,%s,%s,%s)"
    args = (name, address, email, autonornot, puborpriv, affilied)
    InsertIntoDatabase(query, args)

def insertcourses(collegename, name, perc, fees, period, totalseats):
    print "{:*^39}".format('insert course start')
    query = "INSERT INTO courses(college_id, name, perc, fees, period, totalseats) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s, %s, %s, %s, %s)"

    args = (collegename, name, perc, fees, period, totalseats)
    InsertIntoDatabase(query, args)
    print "{:*^39}".format('insert course end')

def insertothercourses(collegename, name, perc, fees, period):
    print "{:*^39}".format('insert othercourses start')
    query = "INSERT INTO othercourses(college_id, name, period, fees, perc) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s, %s, %s, %s)"

    args = (collegename, name, period, fees, perc)
    InsertIntoDatabase(query, args)
    print "{:*^39}".format('insert othercourses end')

def insertfacilities(collegename, facility):
    query = "INSERT INTO facilities(college_id, facility) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s)"

    args = (collegename, facility)
    InsertIntoDatabase(query, args)

def insertfaculties(collegename, name, position, imgurl):
    query = "INSERT INTO faculties(college_id, name, position, imgurl) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s, %s, %s)"

    args = (collegename, name, position, imgurl)
    InsertIntoDatabase(query, args)

def insertrecruiters(rname, rimgurl):
    if (CheckRow(rname) == False):
        rimgname = rname + os.path.splitext(os.path.basename(rimgurl))[1]
        downloadData(rimgurl, rimgname)
        rimgpath = os.path.join(imagesfolderpath, "recruiters", rimgname)
        query = "INSERT INTO recruiters(name, imgpath) VALUES (%s, %s)"

        args = (rname, rimgpath)
        InsertIntoDatabase(query, args)

def insertcollegerecruiters(collegename, recruitersimgname):
    query = "INSERT INTO collegerecruiters(college_id, recruiters_id) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), (SELECT recruiters.id FROM recruiters WHERE name=%s))"

    args = (collegename, recruitersimgname)
    InsertIntoDatabase(query, args)

def insertsalarydetails(collegename, name, avgsalary, highsalary):
    query = "INSERT INTO salarydetails(college_id, name, avgsalary, highsalary) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s, %s, %s)"

    args = (collegename, name, avgsalary, highsalary)
    InsertIntoDatabase(query, args)

def insertscores(collegename, oscore, plment, camp, facul, reputat):
    query = "INSERT INTO scores(college_id, overallscore, placement, campus, faculty, reputation) VALUES ((SELECT colleges.id FROM colleges WHERE name=%s), %s, %s, %s, %s, %s)"

    args = (collegename, oscore, plment, camp, facul, reputat)
    InsertIntoDatabase(query, args)

insertcollege(collegeName, collegeaddress, collegeemail, autonomousornot, publicorprivate, affiliedby)

# print "college name : {} course name : {} course perc : {} course fees : {} course period : {} course total seats : {}".format(collegeName, coursename, courseperc, coursefees, courseperiod, coursetotalseats)
# print "college name : {} course name : {} course perc : {} course fees : {} course period : {} course total seats : {}".format(type(collegeName), type(coursename), type(courseperc), type(coursefees), type(courseperiod), type(coursetotalseats))
insertcourses(collegeName, coursename, courseperc, coursefees, courseperiod, coursetotalseats)

for col in otherCourses:
    cname = col.find('strong').get_text().strip()
    cperc = col.find('span', class_='perc').get_text().strip()
    cfeestxt = col.find(class_='font11').findPrevious().get_text().strip() + " (Total Fees)"
    cperiod = col.find(class_='mg-0').find('span').get_text().strip()
    # print "OtherCourseName : {}\nOtherCoursePeriod : {}\nOtherCoursefees : {}\nOtherCoursePerc : {}\n".format(cname, cperiod, cfeestxt, cperc)
    # print "college name : {} course name : {} course perc : {} course feestxt : {} course period : {}".format(collegeName, cname, cperc, cfeestxt, cperiod)
    # print "college name : {} course name : {} course perc : {} course feestxt : {} course period : {}".format(type(collegeName), type(cname), type(cperc), type(cfeestxt), type(cperiod))
    # print "college name : {} course name : {} course perc : {} course feestxt : {} course period : {}".format(len(collegeName), len(cname), len(cperc), len(cfeestxt), len(cperiod))
    insertothercourses(collegeName, cname, cperc, cfeestxt, cperiod)

i = 0
for facilit in facility:
    insertfacilities(collegeName, facility[i].get_text().strip())
    i += 1

collegeDirectory(collegenamefromurl)
# change to colleges/collegenamefolder/faculty folder and save images inside
os.chdir(os.path.join("colleges", collegenamefromurl, "faculties"))
print os.path.abspath(__file__)
# path format to save in database
# images/colleges/college-directory/faculties/image-name

i = 0
for facilit in facultyName:
    facultyimgurl = facultyImg[i]['data-src']
    facultyimgname = facultyName[i].get_text().strip()
    facultyimgnameext = facultyName[i].get_text().strip() + os.path.splitext(os.path.basename(facultyimgurl))[1]
    downloadData(facultyimgurl, facultyimgnameext)
    facultyimgpath = os.path.join(imagesfolderpath, "colleges", collegenamefromurl, "faculties", facultyimgnameext)
    insertfaculties(collegeName, facultyimgname, facultyPosition[i].get_text().strip(), facultyimgpath)
    i += 1

i = 0
for sal in salaryDetails:
    insertsalarydetails(collegeName, salaryDetails[i].get_text().strip(), avgPay[i].get_text().strip(), highPay[i].get_text().strip())
    i += 1

insertscores(collegeName, overallscore, placement, campus, faculty, campus)

# change to images/recruiters folder and save images inside
os.chdir(os.path.join("..", "..", "..", "recruiters"))
print os.path.abspath(__file__)
# path format to save in database
# images/recruiters/image-name

for img in divimgs:
    recruitersimgtag = img.find('img')
    recruitersimgUrl = recruitersimgtag['src']
    recruitersimgname = recruitersimgtag['title']
    insertrecruiters(recruitersimgname, recruitersimgUrl)
    insertcollegerecruiters(collegeName, recruitersimgname)
    # print recruitersimgUrl

# change back to images directory/folder
# print collegenamefromurl
os.chdir("..")
print os.path.abspath(__file__)
