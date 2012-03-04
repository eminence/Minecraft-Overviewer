#!/usr/bin/python2

'''
genPOI.py

Writes out Point Of Interest data to a markers.js file

Step 1) build a list of all POIs for each regionset that's rendered

the set of *all* POIs is the union of all the POIs from each regionset

Step 2)
1. for each regionset:
   a. Figure out what tilesets use this region set
   b. for each POI in regionset:
      i. if this POI matches a filter in of the tilesets:
         1. record (POI, {tileset: [list of groups]})

markerDB.js contains a list of POIs
the index is unique

markers.js:
    tileset:
        groups:
            group1: [list of DB indexs]
            group2: [list of DB idnexes]

'''
import sys
import re
import os
import cPickle
import logging
import json
import glob
from optparse import OptionParser

from overviewer_core import nbt
from overviewer_core import configParser, world

helptext = """
%prog --config=<config file> [options]"""

def handleSigns(rset, outputdir, render, rname):
    	
    print "handling %r" % rset
    if hasattr(rset, "_pois"):
        print "Already have pois for this regionset"
        return

    filters = render['signs']
    rset._pois = dict(TileEntities=[], Entities=[])

    for (x,z,mtime) in rset.iterate_chunks():
        data = rset.get_chunk(x,z)
        for entity in data['TileEntities']:
            #this_groups = [x.__doc__ for x in filters if x(entity)]
            #if this_groups:
            #    entity.update({"groups":this_groups})
            rset._pois['TileEntities'].append(entity)
        for entity in data['Entities']:
            rset._pois['Entities'].append(entity)
    #groups = [x.__doc__ for x in filters]
    ##with open(os.path.join(outputdir, "markers.js"), "w") as f:
    ##    f.write("overviewer.collections.markerInfo['%s'] = {raw:[], created:false};\n" %rname)
    ##    f.write("overviewer.collections.markerInfo['%s']['groups'] = %s\n" % (rname,json.dumps(groups)))
    ##    f.write("overviewer.collections.markerInfo['%s']['raw'] = " % rname)
    ##    json.dump(pois, f, indent=1)
    ##    f.write(";\n")

def updateBaseMarkers(outputdir):
    with open(os.path.join(outputdir, "markers.js"), "w") as output:
        for entry in os.listdir(outputdir):
            if os.path.isdir(os.path.join(outputdir,entry)) and os.path.isfile(os.path.join(outputdir, entry, "markers.js")):
                output.write("overviewer.util.injectMarkerScript('%s/markers.js');\n" % entry)


def main():
    parser = OptionParser(usage=helptext)
    parser.add_option("--config", dest="config", action="store", help="Specify the config file to use.")

    options, args = parser.parse_args()

    # Parse the config file
    mw_parser = configParser.MultiWorldParser()
    mw_parser.parse(options.config)
    try:
        config = mw_parser.get_validated_config()
    except Exception:
        logging.exception("An error was encountered with your configuration. See the info below.")
        return 1

    destdir = config['outputdir']
    # saves us from creating the same World object over and over again
    worldcache = {}
    rsets=[]

    markersets = set()
    markers = dict()

    for rname, render in config['renders'].iteritems():
        try:
            worldpath = config['worlds'][render['world']]
        except KeyError:
            logging.error("Render %s's world is '%s', but I could not find a corresponding entry in the worlds dictionary.",
                    rname, render['world'])
            return 1
        render['worldname_orig'] = render['world']
        render['world'] = worldpath
        
        # find or create the world object
        if (render['world'] not in worldcache):
            w = world.World(render['world'])
            worldcache[render['world']] = w
        else:
            w = worldcache[render['world']]
        
        rset = w.get_regionset(render['dimension'])
        if rset == None: # indicates no such dimension was found:
            logging.error("Sorry, you requested dimension '%s' for %s, but I couldn't find it", render['dimension'], render_name)
            return 1
      
        for f in render['signs']:
            markersets.add((f, rset))
            name = f.__name__ + hex(hash(f))[-4:] + "_" + hex(hash(rset))[-4:]
            try:
                l = markers[rname]
                l.append(dict(groupName=name, displayName = f.__doc__))
            except KeyError:
                markers[rname] = [dict(groupName=name, displayName=f.__doc__),]
        if rset not in rsets: 
            handleSigns(rset, os.path.join(destdir, rname), render, rname)
            rsets.append(rset)

    print "OK"
    markerSetDict = dict()
    for (flter, rset) in markersets:
        # generate a unique name for this markerset.  it will not be user visible
        name = flter.__name__ + hex(hash(flter))[-4:] + "_" + hex(hash(rset))[-4:]
        print name
        markerSetDict[name] = dict(created=False, raw=[])
        for poi in rset._pois['TileEntities']:
            if flter(poi):
                markerSetDict[name]['raw'].append(poi)
    #print markerSetDict

    with open(os.path.join(destdir, "markersDB.js"), "w") as output:
        output.write("var markersDB=")
        json.dump(markerSetDict, output, indent=2)
        output.write(";\n");
    with open(os.path.join(destdir, "markers.js"), "w") as output:
        output.write("var markers=")
        json.dump(markers, output, indent=2)
        output.write(";\n");
    with open(os.path.join(destdir, "baseMarkers.js"), "w") as output:
        output.write("overviewer.util.injectMarkerScript('markersDB.js');\n")
        output.write("overviewer.util.injectMarkerScript('markers.js');\n")
        output.write("overviewer.collections.haveSigns=true;\n")

if __name__ == "__main__":
    main()
