.. _`working-with-maps`:

*****************
Working with Maps
*****************

MicroCider uses Highmaps to handle mapping. Note that Highmaps does things differently
from other mapping libraries like Leaflet, so the way maps are specified does not translate
well between the two approaches.

Converting Maps to GeoJSON
==========================

Convert the File

In GIS, export the shapefile. You may want to simplify it first, to make it smaller.

Bundle all the output files into one zip file (the .shp, .shx, .dbf, etc.).

Go to http://ogre.adc4gis.com/

Choose the zip file in the "Convert to GeoJSON" section.

Leave the source SRS blank, but put "EPSG:2263" into the "Target SRS" field (this will reproject to NY state plane Long Island).

.. note::
	Alternatively, you can reproject in GIS, and then use the `ESRI2Open tools <https://github.com/project-open-data/esri2open>`_) to output to geojson or topojson.

Whatever the method, the GeoJSON file that is created will have much more precision than we need, so we can make the file smaller by running it through this utility:

	http://jsfiddle.net/highcharts/92oymdb7/

Select all the output from the ogre website and paste it into the left-hand box in the lower-right section of the fiddle. Then, hit "Optimize". Select-all the text in the output box, and copy that.

Paste into a new text file, and save as a .geojson file. You can use this file, but if you want to be able to use lat/long points with it, you need to add a field (see [http://www.highcharts.com/docs/maps/latlon])::

	"hc-transform": {
		"default": {
			"crs": "Your map projection in proj4 string format, as supported by pro4js"
		}
	}


In order to get the proj4 string, go find the projection you want on [http://www.spatialreference.org/], and click the "Proj4" link (e.g. http://www.spatialreference.org/ref/epsg/2263/proj4/). Note that Proj4js will give you a similar result, but it will have extra text.

Insert the "hc-transform" field after the `{"type":"FeatureCollection",` part, before the "crs" field. Here is the string to paste for NYC:
```javascript
"hc-transform":{"default":{"crs":"+proj=lcc +lat_1=41.03333333333333 +lat_2=40.66666666666666 +lat_0=40.16666666666666 +lon_0=-74 +x_0=300000.0000000001 +y_0=0 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs"}},
```

To check it all worked, copy and paste into this fiddle:
http://jsfiddle.net/highcharts/xbzxfx2L/
