
from importlib_metadata import install
# import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
# import earthpy as et
import geohash as gh
import shapely.geometry as sp


def get_area_data(filename, lat, lon):

    ### get the species data that intersects with the entered lat/lon
    ### takes latitude and longitude coordinates and a filename with the data to search from
    ### returns a geodataframe with the species in this area and their ranges

    prec = 6    ## set the precision - how tight is the bounding box

    # make a bounding box based on location
    geocode = gh.encode(lat, lon, prec)
    gh_bbox = gh.bbox(geocode)
    bounds = (gh_bbox['w'], gh_bbox['s'], gh_bbox['e'], gh_bbox['n'])
    # get the records that intersect with bounding box
    my_area = gpd.read_file(filename, bbox=bounds)

    return(my_area)

def get_url(area, lat, lon):

    ### get the urls from the species data
    ### also filters the area to make sure all the species are actually present
    ### takes a geodataframe with species information + the latitude and longitude location
    ### returns a list of urls

    point = sp.Point(lon, lat)

    base_url = 'https://www.iucnredlist.org/species/'
    info = []
    for i in range(len(area)):
        try:
            if point.within(area['geometry'][i]):
                url = base_url + str(int(area['ID_NO'][i])) + '/' + str(int(area['ASSESSMENT'][i]))
                name = area['BINOMIAL'][i]
                #datum = [url,name]
                info.append([url,name])
        except:
            fixed = area['geometry'][i].buffer(0)
            if point.within(fixed):
                url = base_url + str(int(area['ID_NO'][i])) + '/' + str(int(area['ASSESSMENT'][i]))
                name = area['BINOMIAL'][i]
                info.append([url,name])
    no_rep_info = []
    [no_rep_info.append(i) for i in info if i not in no_rep_info]
    #no_rep_info = list(set(info)) # get rid of repeats
    return(no_rep_info)
    
def loop_files(files, lat, lon):

    ### run the functions for multiple status - vulnerable, endangered, etc.
    ### files - a list of filenames based on the statuses the user selects
    ### takes list of filenames and a latitude and longitude location
    ### returns list of urls
    info = []
    for i in range(len(files)):
        area = get_area_data(files[i],lat,lon)
        [info.append(j) for j in get_url(area,lat,lon)]
    return(info)

## example
testlat = 53.759180
testlon = 29.208048
files = ['endangered_shp', 'critically_endangered_shp']
test = loop_files(files, testlat, testlon)
print(test)
