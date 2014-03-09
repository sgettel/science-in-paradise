#!/usr/bin/env python3
# Open all JSON files and save data in a single one.

import json;
import glob;
import numpy;

for suffix, encoding in [[".txt", "iso-8859-2"], ["_utf8_with_GoogleMapsResponse.txt", "utf8"]]:
  allMeetings = [];

  for filename in numpy.sort(glob.glob("data/meeting_list_????" + suffix)):
    # Read JSON file into one large Array.
    print("Reading " + filename);
    with open(filename, "rt") as input:
      meetingsThisYear = json.load(input, encoding=encoding);
    allMeetings += meetingsThisYear;

  filename = "data/meeting_list_all" + suffix;
  print("Writing {0:d} meetings to {1:s}.".format(len(allMeetings), filename));
  with open(filename, "wt") as output:
    json.dump(allMeetings, output);
