import os
from os import path
from itertools import izip
import shutil
from multiprocessing import Pool
from math import pi
import math
import csv
import operator
import pickle
import time

import numpy as np
from scipy.optimize import leastsq

#import pyfits
#from pywcs import WCS
#from ephem import Equatorial, Ecliptic

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plot


import urllib2 as urllib

def make_meetings_vs_time_plots_like_a_boss(title,start_date,end_date,keyword,location,year):
    year_plot = []
    number_of_meetings = []
    #Meetings over years
    for i in range(1996,2014):
        year_plot.append(i)
        number_to_find = 0
        for j in range(len(year)):
            if i == year[j]:
                number_to_find = number_to_find+1
        number_of_meetings.append(number_to_find)
    year_plot = np.array([float(a) for a in year_plot])
    number_of_meetings = np.array([float(a) for a in number_of_meetings])

    figure_star = plot.figure()
    ax_star = figure_star.add_subplot(111)
    filename = 'Meetings_per_Year.eps'
    ax_star.plot(year_plot,number_of_meetings,'og',markersize=10)
    ax_star.set_xlabel('Year')
    ax_star.set_ylabel('Number of Meetings')
    figure_star.savefig(filename,format='eps')
    figure_star.clf()
    plot.close(figure_star)



    #Meetings over Months
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    number = np.zeros(len(months))
    for i in range(len(start_date)):
        the_year,dash,rest = start_date[i].partition('-')
        month,dash,days = rest.partition('-')
        month_integer = int(month)
        number[month_integer-1] = number[month_integer-1]+1

    N = 12 #months
    ind = np.arange(N)
    width = 0.5

    fig, ax = plot.subplots()
    rects = ax.bar(ind,number,width,color='b')
    ax.set_ylabel('Number of Meetings')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(months)
    fig.savefig('Meetings_Months.eps',format='eps')
    fig.clf()
    plot.close(fig)


    garbage,star_year,star_total = count_strings_like_a_boss(title,keyword,year,'STAR')
    garbage,galax_year,galax_total = count_strings_like_a_boss(title,keyword,year,'GALAX')
    garbage,planet_year,planet_total = count_strings_like_a_boss(title,keyword,year,'PLANET')
    garbage,dark_year,dark_total = count_strings_like_a_boss(title,keyword,year,'DARK')
    garbage,cosmology_year,cosmology_total = count_strings_like_a_boss(title,keyword,year,'COSMOLOGY')

    figure_star = plot.figure()
    ax_star = figure_star.add_subplot(111)
    filename = 'Topic_meetings_per_Year.eps'
    ax_star.plot(dark_year,dark_total,'o-k',markersize=10,linewidth=5,label='Dark')
    ax_star.plot(star_year,star_total,'o-r',markersize=10,linewidth=5,label='Stars')
    ax_star.plot(galax_year,galax_total,'o-b',markersize=10,linewidth=5,label='Galaxies')
    ax_star.plot(planet_year,planet_total,'o-g',markersize=10,linewidth=5,label='Planets')
    ax_star.plot(cosmology_year,cosmology_total,'o-c',markersize=10,linewidth=5,label='Cosmology')
    plot.legend(loc=2)

    ax_star.set_xlabel('Year')
    ax_star.set_ylabel('Number of Meetings about the topic')
    figure_star.savefig(filename,format='eps')
    figure_star.clf()
    plot.close(figure_star)

    return(0)



def make_lists_like_a_boss():
    base_command = 'http://www1.cadc-ccda.hia-iha.nrc-cnrc.gc.ca/meetingsvc/meetings?year='
    
    for i in range(1996,2015):
        if i > 1995:
            command = 'curl -O meeting_list_'+str(i)+'.txt '+base_command+str(i)
            command = 'curl -O meeting_list_'+str(i)+'.txt '+base_command+str(i)+' > meeting_list_'+str(i)+'.txt'
            os.system(command)
    return(0)


def parse_files_like_a_boss():
    title = []
    keyword = []
    start_date = []
    end_date = []
    location = []
    year = []
    n_meetings_that_year = np.zeros(len(range(1996,2014)))

    for i in range(1996,2014):
        if i > 1995:
            file = open('./data/meeting_list_'+str(i)+'.txt','r')
            for line in file:
                thing_to_parse = line
                end_of_line = 0
                while end_of_line == 0:
                    before,middle,after = thing_to_parse.partition('"title":"')
                    before2,middle2,after2 = after.partition('"')
                    title.append(before2.upper())
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"start":"')
                    before2,middle2,after2 = after.partition('"')
                    start_date.append(before2.upper())
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"end":"')
                    before2,middle2,after2 = after.partition('"')
                    end_date.append(before2.upper())
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"keywords":"')
                    before2,middle2,after2 = after.partition('"')
                    keyword.append(before2.upper())
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"location":"')
                    before2,middle2,after2 = after.partition('"')
                    location.append(before2.upper())
                    thing_to_parse = after2

                    year.append(i)

                    if after2 == '':
                        end_of_line = 1
    for i in range(1996,2014):
        if year[i] == i:
            n_meetings_that_year[i] = n_meetings_that_year[i]+1
        

    return title,start_date,end_date,keyword,location,year,n_meetings_that_year


def count_strings_like_a_boss(title,keyword,year,topicstring):
    #print topicstring

    topicstring = topicstring.upper()
    years = np.arange(1996,2014)
    total_per_year = np.zeros(len(years))

    total = 0
    for i in range(len(title)):
        junk1 = title[i].count(topicstring)
        junk2 = title[i].count(topicstring)
        yr = np.squeeze(np.where(years == year[i] ))
        if junk1 > 0 or junk2 > 0:
            total += 1
            total_per_year[yr] += 1
        
    
    print total, " meetings total on ", topicstring        
    return total, years, total_per_year



def main():
    #Generate lists of meetings
    #dummy = make_lists_like_a_boss()

    #Read in files and parse
    title,start_date,end_date,keyword,location,year,n_meetings_that_year = parse_files_like_a_boss()


    #make plots of meetings over years and meetings over months
    dummy = make_meetings_vs_time_plots_like_a_boss(title,start_date,end_date,keyword,location,year)








if __name__ == '__main__':
    main()
