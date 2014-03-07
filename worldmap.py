#/usr/bin/env python3
# Plot conferences on world map per year.

import glob;
import numpy;
import json;
from matplotlib import pyplot;
pyplot.ion();
from mpl_toolkits.basemap import Basemap;

latArray = [];
longArray = [];

for filename in numpy.sort(glob.glob("data/meeting_list_????_utf8_with_GoogleMapsResponse.txt")):
  with open(filename, "rt") as input:
    meetingArray = json.load(input);
  for meetingIndex in range(len(meetingArray)):
    try:
      latlong = meetingArray[meetingIndex]["GoogleMapsResponse"]["results"][0]["geometry"]["location"];
      latArray.append(latlong["lat"]);
      longArray.append(latlong["lng"]);
    except KeyError:
      pass;

pyplot.figure();
m = Basemap(projection="kav7", lon_0=0, resolution="l");
m.drawmapboundary(fill_color="white");
m.drawcoastlines();
m.drawcountries();
x, y = m(longArray,latArray);
m.scatter(x, y, marker="o", color="k");
