#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  9 21:34:02 2023
@author: rufuslee
A tool for analyzing researchers' attention to query key words by analyzing the latest 200 results searched from https://arxiv.org
"""
print("\nThis is a tool for analyzing researchers' attention to query key words by analyzing the latest 200 results searched from https://arxiv.org\n")

from bs4 import BeautifulSoup
import urllib.request
import re
import matplotlib.pyplot as plt

###input query values
query = input("Please input what you want to search(replace' 'with '+'): ")
choice = input("Please choose the time unit(year/month): ")
if choice == 'month':
    query_year = input("Please input what year you want to search(eg.23 means 2023): ")


###open and clean the data
urlpage = 'https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=' + query + '&terms-0-field=all&classification-physics_archives=all&classification-include_cross_list=include&date-filter_by=all_dates&date-year=&date-from_date=&date-to_date=&date-date_type=submitted_date&abstracts=show&size=200&order=-announced_date_first'
page = urllib.request.urlopen(urlpage)
soup = BeautifulSoup(page,'html.parser')#analyze page
previous_list = soup.find_all('a',string="pdf")#find pdf elements
preserve = []#preserve cleaned data

for value in previous_list:
    clean_list1 = re.findall(r"[0-9]", str(value))#find time numbers
    preserve.append(clean_list1)
    #print(preserve)


###count the sum of each year and each month
time_dictionary = {}
for out_value in range(len(preserve)):
    year = preserve[out_value][0]+preserve[out_value][1]#year numbers
    if year not in time_dictionary:
        time_dictionary[year] = {}#save sum of the year and sum of each month of the year
        time_dictionary[year]["S" + year] = 1
    else:
        time_dictionary[year]["S" + year] += 1
           
    month = preserve[out_value][2]+preserve[out_value][3]#month numbers
    if month not in time_dictionary[year]:
        time_dictionary[year][month] = 1
    else:
        time_dictionary[year][month] += 1
#print(time_dictionary)


###define two visualize functions
#time unit: year
def year_count():
    for v in time_dictionary.keys():
        temp_list1 = time_dictionary[v].keys()
        temp_list2 = time_dictionary[v].values()
        a = plt.bar(x=list(temp_list1)[0],height=list(temp_list2)[0],width=0.8,align='center',alpha=0.5)
        plt.bar_label(a,padding=3)
    plt.show()

#time unit: month
def month_count():
    a = plt.bar(x=time_dictionary[query_year].keys(),height=time_dictionary[query_year].values(),width=0.8,align='center',alpha=0.5)
    plt.bar_label(a,padding=3)
    plt.show()


###visualize as request
if choice == 'month':
    month_count()
elif choice == 'year':
    year_count()
else:
    print("Please input the correct choice and try again.")