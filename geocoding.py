#!/usr/env/python3
# Translate conference venue strings to geographical coordinates.

import pickle;
import urllib;
import json;

address = "Harvard Smithsonian Center for Astrophysics";

response = urllib.request.urlretrieve("http://maps.googleapis.com/maps/api/geocode/json?address=" + address + "&sensor=false");

with open(response[0], "rt") as input:
  data = json.load(input);

urllib.request.urlcleanup();

latlong = data["results"][0]["geometry"]["location"];
print(latlong["lat"], latlong["lng"]);
