import geopandas as gpd
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
    urls = []
    for i in range(len(area)):
        try:
            if point.within(area['geometry'][i]):
                url = base_url + str(int(area['ID_NO'][i])) + '/' + str(int(area['ASSESSMENT'][i]))
                urls.append(url)
        except:
            fixed = area['geometry'][i].buffer(0)
            if point.within(fixed):
                url = base_url + str(int(area['ID_NO'][i])) + '/' + str(int(area['ASSESSMENT'][i]))
                urls.append(url)
    no_rep_urls = list(set(urls)) # get rid of repeats
    return(no_rep_urls)
    
def loop_files(files, lat, lon):

    ### run the functions for multiple status - vulnerable, endangered, etc.
    ### files - a list of filenames based on the statuses the user selects
    ### takes list of filenames and a latitude and longitude location
    ### returns list of urls
    urls = []
    for i in range(len(files)):
        area = get_area_data(files[i],lat,lon)
        urls.append(get_url(area,lat,lon))
    return(urls)

## example
if __name__ == "__main__":
    testlat = 53.759180
    testlon = 29.208048
    files = ['endangered_shp']
    test = loop_files(files, testlat, testlon)
    print(test)

    print(get_area_data('endangered_shp', testlat, testlon))
