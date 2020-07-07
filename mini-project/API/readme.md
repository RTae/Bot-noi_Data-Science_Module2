# API Thairath Document

## Intoduction

API นี้เป็น Mini project ที่เป็นส่วนหนึ่งของ Botnoi Data Science module 2 โดยเนื้อหาเกี่ยวข้องกับการ Scraping Data, Data base และ API โดยหัวข้อของ Mini project นี้คือ API สำหรับดึงข่าวจากไทยรัฐมา

## How to use

- /getNews [GET]

>Get the news with the specific category.
>>Arg :

>>   - date : Date of the news that you are interseting, input as an string example "3/7/2020". Default is None.

>>    - tag : Tag of the news that you are interseting, input as an string example "COVID-19". Default is None.

>>    - limit : The number of news that will query and maxinum is 20 record, input as an integer example "20". Default is 1.

>>    - category : Category of the news, input as an string example "business". Default is foreign.

>>        - royal, local, business, foreign, society, crime

>>Return :

>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;list of news document

<br />

- /lastestNews [GET]

>Get the lastest news from each category.
>>Arg :

>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;None

>>Return :

>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;list of news document

<br />

- /randomNews [GET]

>Get random news from each category.
>>Arg :

>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;None

>>Return :

>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;list of news document

## Example

>#### /getNews
>> ![Example getNews](https://github.com/RTae/Bot-noi_Data-Science_Module2/blob/master/Example.gif?raw=true)

>#### /lastestNews
>> ![Example lastestNews](https://github.com/RTae/Bot-noi_Data-Science_Module2/blob/master/lastestNews.gif?raw=true)

>#### /randomNews
>> ![Example randomNews](https://github.com/RTae/Bot-noi_Data-Science_Module2/blob/master/randomNews.gif?raw=true)

## Appendix
โดยความรู้ทั้งหมดนี้ผมอยากจะขอบคุณทีม Botnoi ที่ให้โอกาศผมได้มีส่วนร่วมในการได้เรียน Module ดีๆแบบนี้ ทั้งได้ความรู้ใหม่ๆ และ รู้จักพี่ๆที่ได้เรียนอยู่ใน Class นี้ด้วยกัน ซึ่งความรู้ที่ Botnoi ให้ผมนั้นเป็นความรู้ที่ผมต้องการมาก มันทำให้ผมได้เข้าใจถึงแนวทางการหาข้อมูลมา หรือ การเตรียมข้อมูลมาใช้สำหรับในการ Train machine learning ของเราว่าข้อมูลนั้นมันมายังไงและควรมีแนวทางการเตรียมอย่างไร โดยผมยังใหม่มากในวงการของ Data Science การที่ได้มาเข้า Module นี้ทำให้ผมได้เห็นภาพรวมว่าผมยังมีอะไรที่ต้องเรียนรู้อีกเยอะ ในเส้นทางการเป็น Data Scientist ของผม โดยถ้าทาง Botnoi ได้เปิด Module หัวข้อใหม่ถัดไป ผมก็อยากได้โอกาศที่จะได้เป็นส่วนหนึ่งของ Module ต่อไปด้วยนะครับ ขอบคุณครับ

**เต้ ณัฐนันท์**
**[Github](https://github.com/RTae)**