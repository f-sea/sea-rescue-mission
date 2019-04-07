import gmplot

gmap = gmplot.GoogleMapPlotter(37.428, -122.145, 16)
lats= (44.41301,44.403545)
longs= (8.79217,8.909109)
gmap.plot(lats, longs, 'cornflowerblue', edge_width=10)
#gmap.scatter(more_lats, more_lngs, '#3B0B39', size=40, marker=False)
#gmap.scatter(marker_lats, marker_lngs, 'k', marker=True)
#gmap.heatmap(heat_lats, heat_lngs)

gmap.draw("mymap.html")
