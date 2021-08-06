# Glasgow-City-Council-Project

These are the files from my Dissertation project in which I extracted information on the various SCOOT Links in Glasgow, 
matched them with their positions and created a map showing the traffic flow at any given point.

I have included the following datasets:
- The NETL1405.txt file which contains the SCOOT Link name, the upstream and downstream Nodes and Links, as well as other information not in the scope for this project
- A table of Links, with their positions and live traffic flow fetched from the GCC API
- A table of Links from the table above which contained either null or incorrect information (initially)
- A table of some of the missing links, with their positional data in Easting/Northing co-ordinates
- A table of each link pair and their corresponding co-ordinates without their bearings
- 
I have included scripts to:
- Clean and process the Scoot Names and Connections from the NETL1405.txt file before assigning each link it's own file
- A script to fetch live traffic data and positional information from the GCC live traffic API @ https://gcc.portal.azure-api.net/docs/services/traffic/operations/movement?
- A script to convert the multiple Link Files into a table of link pairs
- A script to fill in the missing datapoints for some of the link pairs
- A script to convert the Easting/Northing co-ordinates from some of the datasets into Longitudes and Latitudes
- A script to join the link data retrieved in the first part and join it to the API Data
- A script to display all of these links on a map of Glasgow
- A script to calculate the Bearings between each link pair (WIP)

More scripts to come
