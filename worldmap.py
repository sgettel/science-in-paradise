#/usr/bin/env python3
# Plot conferences on world map per year.

import glob;
import numpy;
import json;
from matplotlib import pyplot;
pyplot.ion();
from mpl_toolkits.basemap import Basemap;

# Parse coordinates into these arrays.
latArray = [];
longArray = [];

for filename in numpy.sort(glob.glob("data/meeting_list_????_utf8_with_GoogleMapsResponse.txt")):
  # Read each year into one large array.
  with open(filename, "rt") as input:
    meetingArray = json.load(input);
  for meetingIndex in range(len(meetingArray)):
    # Cycle through each meeting, extract coordinates.
    try:
      latlong = meetingArray[meetingIndex]["GoogleMapsResponse"]["results"][0]["geometry"]["location"];
      latArray.append(latlong["lat"]);
      longArray.append(latlong["lng"]);
    # Do not stress out too much if we don't find anything.
    except KeyError:
      pass;

# Draw projection with coastlines and countries.
pyplot.figure(figsize=(20,12));
m = Basemap(projection="kav7", lon_0=0, resolution="l");
m.drawmapboundary(fill_color="white", zorder=1);
m.fillcontinents(color="#ddddff");
m.drawcoastlines(zorder=2);
m.drawcountries(zorder=2);
# Transform geographical coordinates into Basemap coordinates, and plot.
x, y = m(longArray,latArray);
m.scatter(x, y, marker="o", color="r", s=6, zorder=3);
# Save plot.
pyplot.savefig("worldmap.png");
