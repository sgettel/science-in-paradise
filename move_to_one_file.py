#!/usr/bin/env python3
# Open all JSON files and save data in a single one.

import json;
import glob;
import numpy;

allMeetings = [];

for filename in numpy.sort(glob.glob("data/meeting_list_????.txt")):
  # Read JSON file into one large Array.
  print("Reading " + filename);
  with open(filename, "rt") as input:
    meetingsThisYear = json.load(input, encoding="iso-8859-2");
  allMeetings += meetingsThisYear;

filename = "data/meeting_list_all.txt";
print("Writing {0:d} meetings to {1:s}.".format(len(allMeetings), filename));
with open(filename, "wt") as output:
  json.dump(allMeetings, output);
