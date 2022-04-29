# igloo portal timetable scraper
a headless selenium bot to scrape the timetable of the civica igloo portal  
displays content in JSON format  
<img src="src/timetable.png" height="300"/><img src="src/json.png" height="300"/>

# documentation
### prerequisites
- [google chrome](https://www.google.com/intl/en_au/chrome/) installed
- [chromedriver](https://chromedriver.chromium.org/downloads) downloaded as the same version as your google chrome
- [python3](https://www.python.org/downloads/) or later downloaded

### installing required packages
```
$ pip install -r requirements.txt
```

### loading options
to load options ```INFO = [<username>, <password>, <directory>]```  
or alternatively create a file called **info.py** in the same directory with these contents  
```python
def creds():
   return [
           '<username>',
           '<password>',
           '<directory_to_chromedriver>',
          ]
```
and change your code to 
```python
import info  
INFO = [info.creds()[0], info.creds()[1], info.creds()[2]]
```
this is to store your credentials

### running scraper
to scrape the website ```igloo.scrape(*INFO,[igloo.<element_name>])```  
as it is a list you can put in as many elements as you want, this includes
- ```igloo.TIMETABLE```
- ```igloo.HOMEWORK```
- ```igloo.ASSESSMENT```
 
then optionally convert the raw html into json ```igloo.<element_name>(raw_html)```

## example code
```python
#load credentials from info.py file
INFO = [info.creds()[0], info.creds()[1], info.creds()[2]]

#or load credentials directly
#INFO = [<username>, <password>, <directory>]

#igloo the data from igloo
raw_html = igloo.scrape(*INFO,[igloo.TIMETABLE,igloo.HOMEWORK,igloo.ASSESSMENT])

#convert to json

#convert timetable
timetable = igloo.timetable(raw_html[0])
print(timetable)

#convert homework
homework = igloo.homework(raw_html[1])
print(homework)

#convert assessment
assessment = igloo.assessment(raw_html[2])
print(assessment)
```
