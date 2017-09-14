import requests
import xlsxwriter
import sqlite3
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup

#req = urllib.request.Request( 'http://python.org', data=None, 
             #headers={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36' } 
                                    #) 
#page = urllib.request.urlopen(req)
d=[]
words_list=[]
fileObject=open("stopwords.txt","r",encoding='utf-8')
#creating stopwords function
StopWords=fileObject.read().split()
StopWordsSet=set(StopWords)
fileObject.close()

workbook = xlsxwriter.Workbook('testdata2.xlsx')
with open('C:/Users/RAUMVASH/Documents/urls.txt') as inf:
    
    urls = (line.strip() for line in inf)
    for url in urls:
        site = urllib.request.urlopen(url)   
        soup = BeautifulSoup(site, "html.parser")
        for script in soup(["script","style"]):
            #remove all javascript and stylesheet code
            script.extract()
            #get text
            text=soup.get_text()
            #print(text)
            tot=len(text)

#with open("C:/Users/RAUMVASH/Documents/testscrap2.txt",'w+',encoding="utf-8") as f:
    #f.write(text)
    

            count={}

#skipping stop words
            for word in text.lower().split():
                if word not in StopWordsSet:
                    if word not in count:
                        count[word]=1
                    else: count[word]+=1
                    
#calculate density
            for i in count.keys():
                d.append((count[i]/tot)*100)
                words_list.append((i,(count[i]/tot)*100))

#with open("C:/Users/RAUMVASH/Documents/testscrap2.txt",'r',encoding="utf-8") as f:
   
    
    #text=f.read()
    #words=text.split()

            for i in text.split():
                if i in count:
                   count[i]=count[i]+1
        
                else:
                   count[i]=1
        
            #print(count)


            
        keylist=list(count.keys())
        

        vallist=list(count.values())

            

    
        worksheet = workbook.add_worksheet()
#insert keys and values in two coloumns
        worksheet.write_column('A1', keylist)
        worksheet.write_column('B1', vallist)
        worksheet.write_column('C1', d)

#specify type of chart
        chart = workbook.add_chart({'type': 'line'})
        

#create chart
        chart.add_series({'values': '=Sheet1!$B$1:$B$50'})
        chart.add_series({'values': '=Sheet2!$B$1:$B$50'})
        chart.add_series({'values': '=Sheet3!$B$1:$B$50'})
        

#specify the column in which chart is placed
        worksheet.insert_chart('E5',chart)
    

    
workbook.close()
#creates database
#db=sqlite3.connect("Data.db")
#c=db.cursor()
#c.execute('''
#    CREATE TABLE word_density(words TEXT,
 #                      density float)
#''')

#c.executemany(''' INSERT INTO word_density(words,density) VALUES(?,?)''', words_list)



#db.commit()
#print("record inserted successfully")
#print("Data from table")
#c.execute('''select * from word_density''')

#for i in c:
#   print(i)

#db.close()
