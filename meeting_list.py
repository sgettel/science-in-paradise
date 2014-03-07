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

import pyfits
from pywcs import WCS
from ephem import Equatorial, Ecliptic

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')
import matplotlib.pyplot as plot


import urllib2 as urllib



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

    for i in range(1996,2015):
        if i > 1995:
            file = open('meeting_list_'+str(i)+'.txt','r')
            for line in file:
                thing_to_parse = line
                end_of_line = 0
                while end_of_line == 0:
                    before,middle,after = thing_to_parse.partition('"title":"')
                    before2,middle2,after2 = after.partition('"')
                    title.append(before2)
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"start":"')
                    before2,middle2,after2 = after.partition('"')
                    start_date.append(before2)
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"end":"')
                    before2,middle2,after2 = after.partition('"')
                    end_date.append(before2)
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"keywords":"')
                    before2,middle2,after2 = after.partition('"')
                    keyword.append(before2)
                    thing_to_parse = after2

                    before,middle,after = thing_to_parse.partition('"location":"')
                    before2,middle2,after2 = after.partition('"')
                    location.append(before2)
                    thing_to_parse = after2

                    year.append(i)

                    if after2 == '':
                        end_of_line = 1

    return title,start_date,end_date,keyword,location,year





def main():
    #Generate lists of meetings
    #dummy = make_lists_like_a_boss()

    title,start_date,end_date,keyword,location,year = parse_files_like_a_boss()

    #

    for i in range(len(title)):
        print keyword[i]





if __name__ == '__main__':
    main()
