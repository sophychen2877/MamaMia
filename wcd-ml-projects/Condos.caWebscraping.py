from bs4 import BeautifulSoup as bs # For HTML parsing
import requests as rq # Website connections
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter
import json
import pandas as pd
from progressbar import ProgressBar
import numpy as np
import matplotlib.pylab as plt
from gmplot import gmplot
import googlemaps
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages

now = datetime.now()
m=now.month
d=now.day
y=now.year
file_name=f'condo_data_{m}-{d}-{y}'


condo_data =[]


gmaps = googlemaps.Client(key='{YOUR-API-KEY-HERE}')


def get_soup(url):
    r = rq.get(url)
    r.encoding='latin1'
    soup = bs(r.text,'lxml')
    return soup
#scape data from the rental listing page
pbar = ProgressBar()
for i in pbar(range(1,11)):
    sleep (1)
    u = f'https://condos.ca/search?for=rent&page={i}'
    s = get_soup(u)
    ls=s.find('div',{'id':'listing-tab'})
    for s1 in ls.find_all('a',{'class':'no-decro','target':'_blank'}):
        row=[]
        link ='https://condos.ca/'+s1.get('href')
        title=s1.get('title')
        price=s1.find('span',{'class':'tag-price'}).get_text()
        bed_bath=list(filter(None,s1.find('div',{'class':'listing-bed-bath-div'}).get_text().strip(' ').splitlines()))
        bed=bed_bath[0]
        shower=bed_bath[1]
        parking_available=bed_bath[2]
        sq_ft=s1.find('div',{'class':'listing-size-div'}).get_text().replace('\n','').replace(' ','').replace('\t','')
        available_date=s1.find('li',{'class':'pull-right'}).get_text().replace('\n','').replace(' ','').replace('\t','').replace('DateAvailable', '')
        row.extend((title,price,sq_ft,bed,shower,parking_available,available_date,link))
        condo_data.append(row)

condos=pd.DataFrame(condo_data, columns=['title', 'price','sq_ft','bed','shower','parking_available','available_date','link']\
                    , index=range(1,len(condo_data)+1))

pbar_1 = ProgressBar()
address=[]
sub_area=[]
area=[]
city=[]

for i in pbar_1(range(0,condos.shape[0])):
    sleep (1)
    u = condos.iloc[i,7]
    s = get_soup(u)
    for s2 in s.find_all('h2',{'class':'slide-address'}):
        addr=s2.get_text().replace('\t','').replace('\n','')
        a=s2.find_all('a')
        sub_addr=a[0].get_text().replace('\t','').replace('\n','')
        sub_area.append(sub_addr)
        area_addr=a[1].get_text().replace('\t','').replace('\n','')
        area.append(area_addr)
        city.append(a[2].get_text().replace('\t','').replace('\n',''))
        addr=addr[:addr.index(' in ')]+addr[addr.index(','):]
        address.append(addr)

condos = condos.assign(address=pd.Series(data=address,index=range(1,len(condo_data)+1)))
condos = condos.assign(sub_area=pd.Series(data=sub_area,index=range(1,len(condo_data)+1)))
condos = condos.assign(area=pd.Series(data=area,index=range(1,len(condo_data)+1)))
condos = condos.assign(city=pd.Series(data=city,index=range(1,len(condo_data)+1)))
condos[['price']]=condos[['price']].replace('[\$,]', '', regex=True).astype(float)

condos.to_csv(path_or_buf=f'{file_name}.csv')

with PdfPages(f'{file_name}.pdf') as pdf:

    condos['area'].value_counts().plot(kind='pie',title='Count of listed Condos by Area',fontsize=5)
    pdf.savefig()
    plt.close()
    
    condos.groupby('area').agg({'price':['max','min','mean']}).\
    plot(kind='barh',title='MinMaxMean of RentalPrice by Area',grid=True,fontsize=5,mark_right=False)
    plt.legend(('Max','Min','Mean'),loc='best')
    pdf.savefig()
    plt.close()
    
    condos['bed'].value_counts().plot(title='BedroomTypes',kind='bar')
    pdf.savefig()
    plt.close()
    
    condos['shower'].value_counts().plot(title='BathroomTypes',kind='bar')
    pdf.savefig()
    plt.close()
    
    condos['sq_ft'].value_counts().plot(title='Condo_Size',kind='bar',fontsize=5)
    pdf.savefig()
    plt.close()

geo_address=[condos.iloc[i]['address'] for i in range(0,condos.shape[0])]
lat_long=[gmaps.geocode(geo_addr)[0]['geometry']['location'] for geo_addr in geo_address]
lats, lons = zip(*([(i['lat'],i['lng']) for i in lat_long]))

# Place map
map_plot = gmplot.GoogleMapPlotter(43.6543, -79.3860,10)
# Scatter points
map_plot.scatter(lats, lons, '#3B0B39', size=20, marker=False)
#heat_maps
map_plot.heatmap(lats, lons)
#draw map
map_plot.draw(f'{file_name}.html')
