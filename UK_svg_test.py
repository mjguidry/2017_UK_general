# -*- coding: utf-8 -*-
"""
Created on Fri May  5 20:37:59 2017

@author: mike

Color constituencies by country to see if all adjacent
"""

import csv, re
from PIL import Image,ImageColor, ImageDraw
import urllib2
from bs4 import BeautifulSoup
london=[
'Barking',
'Battersea',
'Beckenham',
'Bermondsey and Old Southwark',
'Bethnal Green and Bow',
'Bexleyheath and Crayford',
'Brent Central',
'Brent North',
'Brentford and Isleworth',
'Bromley and Chislehurst',
'Camberwell and Peckham',
'Carshalton and Wallington',
'Chelsea and Fulham',
'Chingford and Woodford Green',
'Chipping Barnet',
'Cities of London and Westminster',
'Croydon Central',
'Croydon North',
'Croydon South',
'Dagenham and Rainham',
'Dulwich and West Norwood',
'Ealing Central and Acton',
'Ealing North',
'Ealing, Southall',
'East Ham',
'Edmonton',
'Eltham',
'Enfield North',
'Enfield, Southgate',
'Erith and Thamesmead',
'Feltham and Heston',
'Finchley and Golders Green',
'Greenwich and Woolwich',
'Hackney North and Stoke Newington',
'Hackney South and Shoreditch',
'Hammersmith',
'Hampstead and Kilburn',
'Harrow East',
'Harrow West',
'Hayes and Harlington',
'Hendon',
'Holborn and St. Pancras',
'Hornchurch and Upminster',
'Hornsey and Wood Green',
'Ilford North',
'Ilford South',
'Islington North',
'Islington South and Finsbury',
'Kensington',
'Kingston and Surbiton',
'Lewisham, Deptford',
'Lewisham East',
'Lewisham West and Penge',
'Leyton and Wanstead',
'Mitcham and Morden',
'Old Bexley and Sidcup',
'Orpington',
'Poplar and Limehouse',
'Putney',
'Richmond Park',
'Romford',
'Ruislip, Northwood and Pinner',
'Streatham',
'Sutton and Cheam',
'Tooting',
'Tottenham',
'Twickenham',
'Uxbridge and South Ruislip',
'Vauxhall',
'Walthamstow',
'West Ham',
'Westminster North',
'Wimbledon']

# Grab coordinates for each constituency
constituency_xy=dict()
with open('UK_coords.csv','rb') as csvfile:
    reader=csv.reader(csvfile)
    for row in reader:
        s=row[1]
        s=re.sub('M ','',s)
        s=re.sub('L ','',s)
        s=re.sub(' z','',s)
        nums=[float(x) for x in s.split(' ')]
        xs=nums[0::2]
        ys=nums[1::2]
        constituency_xy[row[0]]=int(nums[0]+0.5),int(nums[1]+0.5)

im = Image.open("UK_BW.png")
img=im.copy() # Test image
img_eng=im.copy()
mode="RGB"

wales_color=ImageColor.getcolor('green',mode)
scotland_color=ImageColor.getcolor('blue',mode)
england_color=ImageColor.getcolor('red',mode)
ni_color=ImageColor.getcolor('orange',mode)
colors=dict()
colors['East Midlands']=ImageColor.getcolor('#cc5242',mode)
colors['Eastern']=ImageColor.getcolor('#5fb85b',mode)
colors['London']=ImageColor.getcolor('#b65cbf',mode)
colors['North East']=ImageColor.getcolor('#b2b143',mode)
colors['North West']=ImageColor.getcolor('#747bc8',mode)
colors['South East']=ImageColor.getcolor('#c58543',mode)
colors['South West']=ImageColor.getcolor('#4cb7b1',mode)
colors['West Midlands']=ImageColor.getcolor('#c75980',mode)
colors['Yorkshire and the Humber']=ImageColor.getcolor('#617c3a',mode)

with open('Westminster_Parliamentary_Constituencies_December_2016_Names_and_Codes_in_the_United_Kingdom.csv','rb') as csvfile:
    reader=csv.reader(csvfile)
    header=next(reader)
    for row in reader:
        code=row[0]
        constituency=row[1]
        constituency=re.sub('St ','St. ',constituency)
        constituency=re.sub('Môn','Mon',constituency)
        constituency=re.sub('\s+$','',constituency)
        if(constituency in constituency_xy):
            x=constituency_xy[constituency][0]
            y=constituency_xy[constituency][1]
            if(code[0]=='W'):
                ImageDraw.floodfill(img,(x,y),wales_color)
            elif(code[0]=='S'):
                ImageDraw.floodfill(img,(x,y),scotland_color)
            elif(code[0]=='E'):
                ImageDraw.floodfill(img,(x,y),england_color)
            else:
                ImageDraw.floodfill(img,(x,y),ni_color)
html=urllib2.urlopen('https://en.wikipedia.org/wiki/List_of_United_Kingdom_Parliament_constituencies')
soup=BeautifulSoup(html)
tables=soup.findAll("table")
table=tables[1]
trs=table.findAll('tr')
for tr in trs:
    tds=tr.findAll('td')
    if(len(tds)>6):
        const=tds[0].getText()
        region=tds[6].getText()
        region=re.sub('&','and',region)
        const=re.sub('St ','St. ',const)
        if(const not in constituency_xy):
            print const
        else:
            x=constituency_xy[const][0]
            y=constituency_xy[const][1]
            ImageDraw.floodfill(img_eng,(x,y),colors[region])
img.save('test.png')
img_eng.save('england.png')