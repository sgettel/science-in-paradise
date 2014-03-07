#!/usr/bin/env python3
# Translate conference venue strings to geographical coordinates.

import pickle;
import urllib;
import json;
import glob;
import numpy;

for filename in numpy.sort(glob.glob("data/meeting_list_????_utf8.txt")):
  # Read JSON file into one large Array.
  print("Reading " + filename);
  with open(filename, "rt") as input:
    meetingArray = json.load(input);
  # Cycle through all meetings.
  for meetingIndex in range(len(meetingArray)):
    meeting = meetingArray[meetingIndex];
    # See if there is location information, or if not, at least address.
    if len(meeting["location"]) == 0:
      if len(meeting["address"]) == 0:
        continue;
      else:
        location = meeting["address"];
    else:
      location = meeting["location"];
    # Quote accented letters and stuff, and prepare URL.
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.parse.quote(location) + "&sensor=false";
    # Query Google Maps into a file.
    response = urllib.request.urlretrieve(url);
    # Read file, again JSON.
    with open(response[0], "rt") as input:
      data = json.load(input);
    # If there are no results, skip.
    if len(data["results"]) == 0:
      print("No results for " + meeting["address"]);
      continue;
    # Otherwise, print coordinates.
    latlong = data["results"][0]["geometry"]["location"];
    print("{0:d} results for {1:s}, lat {2:f}, long {3:f}.".format(len(data["results"]), location, latlong["lat"], latlong["lng"]));
    # Add field to meeting dict.
    meeting["GoogleMapsResponse"] = data;
  # Save array of dicts of arrays and dicts of arrays and dicts of... into file.
  print("Writing " + filename[:-4] + "_with_GoogleMapsResponse.txt");
  with open(filename[:-4] + "_with_GoogleMapsResponse.txt", "wt") as output:
    json.dump(meetingArray, output);
  # Clean up tempfiles after processing each year.
  urllib.request.urlcleanup();
