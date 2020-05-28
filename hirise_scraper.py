#!/usr/bin/python3



#https://www.uahirise.org/PDS/DTM/PSP/

from bs4 import BeautifulSoup
import requests


def parse3(url):
  page = requests.get(url).text
  soup = BeautifulSoup(page, 'html.parser')
  r = {}
  for node in soup.find_all('a'):
    if node.get('href').startswith("DT"):
      path = url + node.get('href')
      r[path] = requests.head(path).headers['content-length']      
      print(path, r[path])
  return r

def parse2(url):
  page = requests.get(url).text
  soup = BeautifulSoup(page, 'html.parser')
  l = [url + node.get('href') for node in soup.find_all('a') if node.get('href')!="../"]
  r = {}
  for f in l:
    r.update(parse3(f))
  return r

def parse1():
  url1 = 'https://www.uahirise.org/PDS/DTM/PSP/'
  url2 = 'https://www.uahirise.org/PDS/DTM/ESP/'
  page = requests.get(url1).text
  soup = BeautifulSoup(page, 'html.parser')
  l = [url1 + node.get('href') for node in soup.find_all('a') if node.get('href')!="../"]
  page = requests.get(url2).text
  soup = BeautifulSoup(page, 'html.parser')
  l = l + [url2 + node.get('href') for node in soup.find_all('a') if node.get('href')!="../"]
  r = {}
  for f in l:
    r.update(parse2(f))
  return r

# PHASE 1
r = parse1()

#PHASE 2
mission_dict = {"PSP": "PSP (Primary Science Phase)", "ESP":"ESP (Extended Science Phase)"}
type_dict = {"E": "Aeroid elevation", "R": "Radii", "F": "Figure of Merit (FOM) map"}
projection_dict = {"E":"Equirectangular", "P": "Polar stereographic"}
spacing_dict = {"A": 0.25, "B": 0.5, "C": 1, "D": 2, "E": 4}
institution_dict={"A": "University of Arizona",
			"B":"Birkbeck University of London",
			"C" : "Caltech",
			"G" : "Laboratoire de Planetologie et Geodynamique",
			"H" : "Natural History Museum",
			"L" : "University College London",
			"J" : "JPL",
						"N" : "NASA Ames",
			"O" : "Open University",
			"P" : "Planetary Science Institute",
			"U" : "USGS",
			"Z": "Other"}
with open("TABLE.csv", "w") as outfile:  
  outfile.write("NAME; DESCRIPTION; URL; SIZE; MISSION; TYPE; PROJECTION; SPACING(m/pixel); LATITUDE (central); LONGITUDE (central); ORBIT PHASING A; TARGET A; ORBIT PHASING B; TARGET B; INSTITUTION; VERSION\n")
  for (url, size) in r.items():
    mission = url.split('/')[5]
    fname = url.split('/')[-1].split('.')[0]
    classification = fname.split('_')[0]
    datatype = fname.split('_')[0][2]
    projection = fname.split('_')[0][3]
    spacing = fname.split('_')[0][4]
    [orbit_a, target_a] = fname.split('_')[1:3]
    [orbit_b, target_b] = fname.split('_')[3:5]
    institution = fname.split('_')[5][0]
    version = int(fname.split('_')[5][1:3])
    page = requests.get("https://www.uahirise.org/dtm/dtm.php?ID="+mission+"_"+orbit_a+"_"+target_a).text
    soup = BeautifulSoup(page, 'html.parser')
    description = soup.findAll('span',{"class":'observation-id-title'})[0].text
    infos = soup.findAll('td',{"class":'product-text-gamma'})[0].contents
    lat = infos[15]
    lon = infos[20]
    print("File name:  ", fname)
    print("Description:", description)
    print("Size:       ", size.strip())
    print("Mission:    ", mission_dict[mission])
    print("Type:       ", type_dict[datatype])
    print("Projection: ", projection_dict[projection])
    print("Spacing:    ", spacing_dict[spacing],"m/pixel")
    print("Latitude:   ", lat)
    print("Longitude:  ", lon)
    print("Orbit A:    ", orbit_a)
    print("Target A:   ", target_a)
    print("Orbit B:    ", orbit_b)
    print("Target B:   ", target_b)
    print("Institution:", institution_dict[institution.upper()])
    print("Version:    ", version)
    outfile.write(fname + "; " + description.strip() + "; " +
    url +"; " +
    size.strip() +"; " +
    mission_dict[mission]+"; " +
    type_dict[datatype]+"; " +
    projection_dict[projection]+"; " +
    str(spacing_dict[spacing])+"; " +
    lat[:-1] + "; " + lon[:-1] + "; " +
    orbit_a+"; " +
    target_a+"; " +
    orbit_b+"; " +
    target_b+"; " +
    institution_dict[institution.upper()]+"; " +
    str(version)+"\n")    
    print()
   
