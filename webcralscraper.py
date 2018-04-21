#!/usr/bin/python

# WebcralButool.py by Chandan Chainani
# Webcralscraper is designed for scraping data from bubhopal.nic.in site for result of student and save it to excel file.

from Tkinter import *
import ttk
from PIL import Image, ImageTk
import tkMessageBox
import tkFileDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select,WebDriverWait
#from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import re
import xlsxwriter

class WebCrawlScraper:

    def __init__(self, master):
        master.title('WebCralScraper')
        #master.iconbitmap('icon.ico')
        master.geometry('400x200+450+250')
        master.resizable(False, False)
        master.option_add('*tearOff', False)
	
        self.style = ttk.Style()
        self.style.configure('TFrame', background = '#42F020')
        self.style.configure('TButton', background = '#39C2F0')
        self.style.configure('TLabel', background = '#42F020', font = ('Arial', 9,"bold"))
        #self.style.configure('Header.TLabel', font = ('Arial', 18, 'bold'))
	
        images = Image.open('Webcralscraper.png')
        img = ImageTk.PhotoImage(images)
		
        self.frame_header = ttk.Frame(master)
        self.frame_header.pack()
        self.frame_header.config(height = 230, width= 500)
        self.LImages = ttk.Label(self.frame_header, image = img)
        self.LImages.image = img
        self.LImages.place(x= 285,y=1)

        ttk.Label(self.frame_header, text = 'Subject').place( x = 21, y = 18)
        ttk.Label(self.frame_header, text = 'Semester').place( x = 21, y = 45)
        ttk.Label(self.frame_header, text = 'StartRollNo').place( x = 21, y = 72)
        ttk.Label(self.frame_header, text = 'StopRollNo').place( x = 21, y = 99)
        self.Subjects = StringVar()
        self.subcombobox = ttk.Combobox(self.frame_header, textvariable = self.Subjects)
        self.subcombobox['values'] = ('Select Subject','B.A','B.Com Plain','B.SC','BCA','M.Com','M.Sc')
        self.subcombobox.current(0)
        self.Semester = StringVar()
        self.semspinbox = Spinbox(self.frame_header, from_ = 0, to = 6, textvariable = self.Semester)
        self.StartRoll = ttk.Entry(self.frame_header, width = 18)
        self.StopRoll = ttk.Entry(self.frame_header, width = 18)
        self.Start = ttk.Button(self.frame_header, text = "Start",command = self.startpoint)
        self.About = ttk.Button(self.frame_header,text = "About", command = self.About)
        self.progressbar = ttk.Progressbar(self.frame_header,orient = HORIZONTAL,length = 260,mode='determinate',value = 0.0)
	
        self.subcombobox.place(x=90,y=18)
        self.semspinbox.place(x=90,y=45)
        self.StartRoll.place(x=90, y=72)
        self.StopRoll.place(x=90, y=99)
        self.Start.place(x=75,y=126)
        self.About.place(x=180,y=126)
        self.progressbar.place(x=21, y=160)
    
    def excelfilesave(self):
        global resultuple
        global SubjName
        text2save = tkFileDialog.asksaveasfile(mode='w', defaultextension=".xlsx", initialdir = 'C:\\',initialfile='Result')
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(text2save)
        worksheet = workbook.add_worksheet()
		# Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        worksheet.set_column('A:F', 18)
		# Create a format to use in the merged range.
        merge_format = workbook.add_format({
        	'bold': 1,
        	'border': 1,
        	'align': 'center',
        	'valign': 'vcenter',
        	'font_size': 15,
        	'fg_color': 'blue'})

        worksheet.merge_range('A1:F1', SubjName, merge_format)
		# Write some data headers.
        worksheet.write('A3', 'Roll No.', bold)
        worksheet.write('B3', 'Student Name', bold)
        worksheet.write('C3', 'Marks Obtained.', bold)
        worksheet.write('D3', 'Result', bold)
        worksheet.write('E3', 'Subject1', bold)
        worksheet.write('F3', 'Subject2', bold)
		# Start from the first cell below the headers.
        row = 3
        col = 0
		# Iterate over the data and write it out row by row
        for subj1,subj2,rollno,studname,marks_obtained,result in (resultuple):
            worksheet.write(row, col,     rollno)
            worksheet.write(row, col + 1, studname)
            worksheet.write(row, col + 2, marks_obtained[0])
            worksheet.write(row, col + 3, result)
            worksheet.write(row, col + 4, subj1)
            worksheet.write(row, col + 5, subj2)
            row += 1

        workbook.close()
        tkMessageBox.showinfo(title = 'Result Saved', message = 'Result Saved in the File' )
        self.clear()
        
    def check_exists_by_element_name(self, elementname):
        try:
            self.browser.find_element_by_name(elementname)
        except NoSuchElementException:
            return False
        return True
	
    def websitescraping(self, Subject, semester, startroll, stoproll):
        global resultuple
        global resultvalue
        global SubjName
        global RPFS
        RPFS = ''
        Condition = False
        resultvalue = ()
        self.browser = webdriver.PhantomJS()
        self.browser.set_window_size(1024, 768)
        self.browser.get("http://www.bubhopal.nic.in/results/jun2014/semIV/defaultnew.htm")
        try:
                WebDriverWait(self.browser, 30).until(EC.presence_of_element_located((By.NAME,"ddlsem")))
                Condition = self.check_exists_by_element_name('ddlsem')
                if Condition:
                        select_options = Select(self.browser.find_element_by_name("ddlsem"))
                        select_options.select_by_index(semester-1)
                        elem = self.browser.find_element_by_name("rollno").send_keys(startroll, Keys.RETURN)
                        TotalMarks = re.compile('\d.*\d')
                        SubjName = self.browser.find_elements_by_tag_name('td')[8].text
                        
                        if Subject == 'BCA' or Subject == 'M.Sc':
                                if len(self.browser.find_elements_by_tag_name('td')) <= 13 :
                                        pass
                                else:
                                        studname = self.browser.find_elements_by_tag_name('td')[14].text
                                        rollno = self.browser.find_elements_by_tag_name('td')[10].text
                                        TMarks = TotalMarks.findall(self.browser.find_elements_by_tag_name('td')[143].text)
                                        RPFS = self.browser.find_elements_by_tag_name('td')[147].text
                                        sub1 = self.browser.find_elements_by_tag_name('td')[40].text
                                        sub2 = self.browser.find_elements_by_tag_name('td')[56].text
                                        sub3 = self.browser.find_elements_by_tag_name('td')[57].text
                                        sub4 = self.browser.find_elements_by_tag_name('td')[73].text
                                        sub5 = self.browser.find_elements_by_tag_name('td')[74].text
                                        sub6 = self.browser.find_elements_by_tag_name('td')[90].text
                                        sub7 = self.browser.find_elements_by_tag_name('td')[91].text
                                        sub8 = self.browser.find_elements_by_tag_name('td')[107].text
                                        sub9 = self.browser.find_elements_by_tag_name('td')[108].text
                                        sub10 = self.browser.find_elements_by_tag_name('td')[124].text
                                        sub11 = self.browser.find_elements_by_tag_name('td')[125].text
                                        sub12 = self.browser.find_elements_by_tag_name('td')[141].text
                                                
                                        if 'NC-1' in RPFS:
                                                if '*' in sub2:
                                                        resultvalue +=(sub1,)
                                                elif '*' in sub4:
                                                        resultvalue += (sub3,)
                                                elif '*' in sub6:
                                                        resultvalue += (sub5,)
                                                elif '*' in sub8:
                                                        resultvalue +=(sub7,)
                                                elif '*' in sub10:
                                                        resultvalue += (sub9,)
                                                elif '*' in sub12:
                                                        resultvalue +=(sub11,)
                                                resultvalue += (u' ',)
                                                
                                                
                                        if 'NC-2' in RPFS:
                                                if '*' in sub2:
                                                        resultvalue += (sub1,)
                                                if '*' in sub4:
                                                        resultvalue += (sub3,)
                                                if '*' in sub6:
                                                        resultvalue += (sub5,)
                                                if '*' in sub8:
                                                        resultvalue += (sub7,)
                                                if '*' in sub10:
                                                        resultvalue += (sub9,)
                                                if '*' in sub12:
                                                        resultvalue += (sub11,)
                                        
                        if Subject == 'B.SC' or Subject == 'B.Com' or Subject == 'B.A' or Subject == 'M.Com':
                                if len(self.browser.find_elements_by_tag_name('td')) <= 13 :
                                        pass
                                else:
                                        studname = self.browser.find_elements_by_tag_name('td')[14].text
                                        rollno = self.browser.find_elements_by_tag_name('td')[10].text
                                        TMarks = TotalMarks.findall(self.browser.find_elements_by_tag_name('td')[109].text)
                                        RPFS = self.browser.find_elements_by_tag_name('td')[113].text       
                                        sub1 = self.browser.find_elements_by_tag_name('td')[40].text
                                        sub2 = self.browser.find_elements_by_tag_name('td')[56].text
                                        sub3 = self.browser.find_elements_by_tag_name('td')[57].text
                                        sub4 = self.browser.find_elements_by_tag_name('td')[73].text
                                        sub5 = self.browser.find_elements_by_tag_name('td')[74].text
                                        sub6 = self.browser.find_elements_by_tag_name('td')[90].text
                                        sub7 = self.browser.find_elements_by_tag_name('td')[91].text
                                        sub8 = self.browser.find_elements_by_tag_name('td')[107].text
                                
                                        if 'NC-1' in RPFS:
                                                if '*' in sub2:
                                                        resultvalue += (sub1,)
                                                elif '*' in sub4:
                                                        resultvalue += (sub3,)
                                                elif '*' in sub6:
                                                        resultvalue += (sub5,)
                                                elif '*' in sub8:
                                                        resultvalue += (sub7,)
                                                resultvalue += (u' ',)
                                                
                                        if 'NC-2' in RPFS:
                                                if '*' in sub2:
                                                        resultvalue += (sub1,)
                                                if '*' in sub4:
                                                        resultvalue += (sub3,)
                                                if '*' in sub6:
                                                        resultvalue += (sub5,)
                                                if '*' in sub8:
                                                        resultvalue += (sub7,)
                        
                        self.browser.quit()
                        if 'PASS' in RPFS or 'FAIL' in RPFS:
                                resultvalue += (u' ',)
                                resultvalue += (u' ',)
                        
                        if SubjName == '' and RPFS == '':
                                rollno = ' '
                                studname = ' '
                                TMarks = ' '
                                resultvalue += (u' ',)
                                resultvalue += (u' ',)
                        
                        if 'PASS' in RPFS or 'FAIL' in RPFS or 'NC-1' in RPFS or 'NC-2' in RPFS or RPFS == '':
                                resultvalue += (rollno, studname, TMarks, RPFS)
                                resultuple.append(resultvalue)
                                self.progressbarincrease()
                        if SubjName == '' and startroll == stoproll:
                                                self.delclearMemory()
                        elif startroll != stoproll:
                                startroll += 1
                                self.websitescraping(Subject, semester, startroll, stoproll)
                        else:   
                                self.excelfilesave()
        except TimeoutException:
            self.browser.quit()
            tkMessageBox.showinfo(title = 'Result', message = "   Loading took too much time!\n\t      OR\nThe Internet Connection is Closed." )
            
    def progressbarincrease(self):
        global totalrollno
        self.progressbar['value'] += totalrollno/totalrollno
        self.progressbar.update()
    
    def delclearMemory(self):
        tkMessageBox.showinfo(title = 'Result', message = '           Check the Rollno\n\t      OR\nThere is no result for such number.' )
        self.clear()
   
    def About(self):
        tkMessageBox.showinfo(title = 'About WebcralScraper', message = 'WebCralScraper is designed for scraping data from bubhopal.nic.in site for result of students and save it to excel file.\nDesign and Developed By Chandan Chainani' )
                
    def clear(self):
        global resultuple
        global totalrollno
        self.Semester.set('0')
        self.Subjects.set('Select Subject')
        self.StartRoll.delete(0, END)
        self.StopRoll.delete(0, END)
        self.progressbar['value'] = 0.0
        self.progressbar['maximum'] = 0.0
        resultuple = []
        totalrollno = 0.0
    
    def startpoint(self):
        if self.Semester.get() == 0 or self.Subjects.get() == 'Select Subject':
            tkMessageBox.showinfo(title = 'Fill Roll Numbers', message = 'Please select the subject and semester.')
        
        elif self.StartRoll.get() == '' or self.StopRoll.get() == '':
            tkMessageBox.showinfo(title = 'Fill Roll Numbers', message = 'Please fill the start and stop Roll numbers.')
    
        elif self.Semester.get() != 0 or self.Subjects.get() != 'Select Subject' or self.StartRoll.get() != '' or self.StopRoll.get() != '':
            global totalrollno
            Subject = self.Subjects.get()
            semester = int(self.Semester.get())
            if len(self.StartRoll.get()) == 9 and len(self.StopRoll.get()) == 9:
                startroll = int(self.StartRoll.get()) 
                stoproll = int(self.StopRoll.get())
                totalrollno = (float(stoproll) - startroll) + 1.0
                self.progressbar.config(maximum = totalrollno)
                self.websitescraping(Subject, semester, startroll, stoproll)
            else:
                self.StartRoll.delete(0, END)
                self.StopRoll.delete(0, END)
                tkMessageBox.showinfo(title = 'Correct Roll Numbers and Limit', message = 'Please fill the Correct start and stop roll numbers.')
       
def main():
    global resultuple
    global totalrollno
    resultuple = []
    totalrollno = 0.0
    root = Tk()
    webcrawlscraper = WebCrawlScraper(root)
    root.mainloop()
    
if __name__ == "__main__": main()
