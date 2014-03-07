#!/usr/env/python3
# Translate conference venue strings to geographical coordinates.

import pickle;
import urllib;
import json;
import glob;
import numpy;

for filename in numpy.sort(glob.glob("data/meeting_list_????_utf8.txt")):
  print("Reading " + filename);
  with open(filename, "rt") as input:
    meetingArray = json.load(input);
  for meetingIndex in range(len(meetingArray)):
    meeting = meetingArray[meetingIndex];
    if len(meeting["location"]) == 0:
      if len(meeting["address"]) == 0:
        continue;
      else:
        location = meeting["address"];
    else:
      location = meeting["location"];
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + urllib.parse.quote(location) + "&sensor=false";
    response = urllib.request.urlretrieve(url);
    with open(response[0], "rt") as input:
      data = json.load(input);
    if len(data["results"]) == 0:
      print("No results for " + meeting["address"]);
      continue;
    latlong = data["results"][0]["geometry"]["location"];
    print("{0:d} results for {1:s}, lat {2:f}, long {3:f}.".format(len(data["results"]), location, latlong["lat"], latlong["lng"]));
    meeting["GoogleMapsResponse"] = data;
  print("Writing " + filename[:-4] + "_with_GoogleMapsResponse.txt");
  with open(filename[:-4] + "_with_GoogleMapsResponse.txt", "wt") as output:
    json.dump(meetingArray, output);
  urllib.request.urlcleanup();
