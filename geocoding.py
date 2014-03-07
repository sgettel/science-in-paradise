#!/usr/env/python3
# Translate conference venue strings to geographical coordinates.

import pickle;
import urllib;
import json;
import glob;
import numpy;

for filename in numpy.sort(glob.glob("meeting_list_????.txt")):
  with open(filename, "rt") as input:
    meetingData = json.load(input, encoding="iso-8859-2");
  for meeting in meetingData:
    if len(meeting["address"]) == 0:
      continue;
    url = "http://maps.googleapis.com/maps/api/geocode/json?address=" + meeting["address"] + "&sensor=false";
    response = urllib.request.urlretrieve(url);
    with open(response[0], "rt") as input:
      data = json.load(input);
      if len(data["results"]) == 0:
        continue;
      latlong = data["results"][0]["geometry"]["location"];
      print(latlong["lat"], latlong["lng"]);

urllib.request.urlcleanup();
