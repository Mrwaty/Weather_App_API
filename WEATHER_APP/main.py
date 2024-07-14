import sys
import psycopg2
import requests
from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem
from PyQt5.QtGui import QPixmap, QCursor

from weather_design import Ui_Dialog


class Main(QDialog, Ui_Dialog):
    def __init__(self):
        super(Main,self).__init__()
        self.setupUi(self)
        
        #buttons clicked to functions
        self.button_weather.clicked.connect(self.weather_click)
        self.button_NL.clicked.connect(self.NL_click)
        self.button_USA.clicked.connect(self.USA_click)
        self.button_DE.clicked.connect(self.DE_click)
        
        #finger button  
        self.button_weather.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_NL.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_USA.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.button_DE.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        
        #For column selection in a table     
        self.tableWidget.cellClicked.connect(self.tableWidget_clicked)
        self.name=' '
        
        #Database connect
        self.conn= psycopg2.connect("dbname=Weather_App user=postgres password=0000")
        self.cur=self.conn.cursor()
    
    def weather_click(self):
        
        country=['nl', 'de', 'usa']
        description=' ' 
        self.urgent='False'
        
        for i in range(3):
            
            self.cur.execute(f'SELECT * FROM {country[i]}')
            self.country_list=self.cur.fetchall()
            
            for j in self.country_list:
                if j[0]==self.lineEdit.text().title() or j[0]==self.name:
                    self.urgent='inside'
                    self.label_sel_city.setText('{}'.format(j[0]))
                    self.label_sel_province.setText('{}'.format(j[1]))
                    self.label_sel_population.setText('{}'.format(j[2]))
                    
                    api_key='cdac62c12a56eb8beb0cc4de54b23a97'
                    response= requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={j[0]},{country[i].upper}&limit=5&appid={api_key}')
                    data=response.json()
                    lat=str(data[0]['lat']).split('.')[0]
                    #print(lat)
                    lon=str(data[0]['lon']).split('.')[0]
                    #print(lon)
                    
                    response1= requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric')
                    data1=response1.json()
                    description= data1['weather'][0]['description']
                    print(description)
                    temperature= data1['main']['temp']
                    self.label_population_3.setText(str(description).upper())
                    self.label_temp.setText(str(temperature).split('.')[0]+'°C')

                    #icon description
                    self.pixmap=description
                    self.pixmap=QPixmap('C:\\Users\\merve\\VSCODE INFOTECHACADEMY\\WEATHER\\icons\\{}.png'.format(description)) 
                    #print('C:\\Users\\merve\\VSCODE INFOTECHACADEMY\\WEATHER\\icons\\{}.png'.format(description))
                    self.label_icon.setPixmap(self.pixmap)
                    
                    #background description 
                    if description=='broken clouds' or description=='overcast clouds' or description=='scattered clouds':
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/4.jpg)")                        
        
                    elif description=='clear sky' :
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/sunn.jpg)")                                                
        
                    elif description=='few clouds' :
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/18.jpg)")                                                
        
                    elif description=='light intensity shower rain' or description=='light rain' or description=='moderate rain' or description=='rain' or description=='shower rain':
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/12.jpg)")                                                
    
                    elif description=='snow' :
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/snoww.jpg)") 
        
                    elif description=='thunderstorm with rain' or description=='thunderstorm' :
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/14.jpg)")                        
    
                    elif description=='mist' :
                        self.label_background.setStyleSheet("background-image: url(C:/Users/merve/VSCODE INFOTECHACADEMY/WEATHER/background/xx.jpg)")                                                   
                
                else:
                    pass
                
        if self.urgent=='inside':
            pass
        else:
            self.label_population_3.setText(' ')
    
            self.label_temp.setText('PLEASE ENTER A VALID CITY')
            self.label_temp.setStyleSheet("font: 63 16pt \"Yu Gothic UI Semibold\";")
            self.label_sel_city.setText(' ')
            self.label_sel_province.setText(' ')
            self.label_sel_population.setText(' ')
            self.label_background.setStyleSheet("background-image: url(background/x.jpg)")
            self.pixmap=description
            self.pixmap=QPixmap('multiply.png')    
            self.label_icon.setPixmap(self.pixmap)
            
    
    
    
        self.lineEdit.clear()                      
    
    def NL_click(self):
        
        self.cur.execute("SELECT * FROM nl ORDER BY NULLIF(regexp_replace(population, '\D', '', 'g'), '')::int desc")
        self.nl_list=self.cur.fetchall()
        self.tableWidget.setRowCount(len(self.nl_list))
        for i in range(len(self.nl_list)):
            self.tableWidget.setItem(i,0,QTableWidgetItem("{}".format(self.nl_list[i][0])))
            self.tableWidget.setItem(i,1,QTableWidgetItem("{}".format(self.nl_list[i][1])))
            self.tableWidget.setItem(i,2,QTableWidgetItem("{}".format(self.nl_list[i][2])))
        self.cnt=self.nl_list
    
    def USA_click(self):
        
        self.cur.execute("SELECT * FROM usa ORDER BY NULLIF(regexp_replace(population, '\D', '', 'g'), '')::int desc")
        self.usa_list=self.cur.fetchall()
        self.tableWidget.setRowCount(len(self.usa_list))
        for i in range(len(self.usa_list)):
            self.tableWidget.setItem(i,0,QTableWidgetItem("{}".format(self.usa_list[i][0])))
            self.tableWidget.setItem(i,1,QTableWidgetItem("{}".format(self.usa_list[i][1])))
            self.tableWidget.setItem(i,2,QTableWidgetItem("{}".format(self.usa_list[i][2])))
        self.cnt=self.usa_list
    
    def DE_click(self):
        
        self.cur.execute("SELECT * FROM de ORDER BY NULLIF(regexp_replace(population, '\D', '', 'g'), '')::int desc")
        self.de_list=self.cur.fetchall()
        self.tableWidget.setRowCount(len(self.de_list))
        for i in range(len(self.de_list)):
            self.tableWidget.setItem(i,0,QTableWidgetItem("{}".format(self.de_list[i][0])))
            self.tableWidget.setItem(i,1,QTableWidgetItem("{}".format(self.de_list[i][1])))
            self.tableWidget.setItem(i,2,QTableWidgetItem("{}".format(self.de_list[i][2])))
        self.cnt=self.de_list
    
    def tableWidget_clicked(self,row,col): 
        #print(str(row),str(col))      
        #print(self.cnt[row][0])       
        self.name=self.cnt[row][0]     
        self.weather_click()
        self.name=' '


app=QApplication(sys.argv)
Main=Main()
Main.show()
sys.exit(app.exec_())