# bsc5.py

A python3 port of [https://opengameart.org/content/night-sky-skybox-generator](https://opengameart.org/content/night-sky-skybox-generator), with some additional features
Requires [Numpy](https://numpy.org/) and [Pillow](https://python-pillow.org) packages

Generates a skybox textures using the [Yale Bright Star Catalog](http://tdc-www.harvard.edu/catalogs/bsc5.html).
Scroll [down](#cool-stuff) for links to some resources.



Original author: Mystic Mike (Mike Hosker)


Added features: 
- Downloads the catalog for you
- watch this space!
- That's pretty much it

## Installation
You'll need the numpy and Pillow packages to run the script, use ```python3 -m pip install Pillow numpy```

## Running
You can make the script executable and do a ```bsc.py SIZE``` or else run it using ```python3 bsc.py SIZE```. 


```SIZE``` is the length of the side of each of the square output textures.


It will output 6 textures, corresponding to each side of a skybox, in the directory it's run from.


## cool-stuff
[http://tdc-www.harvard.edu/catalogs/bsc5.html](http://tdc-www.harvard.edu/catalogs/bsc5.html)


[The original generator, with code](https://opengameart.org/content/night-sky-skybox-generator)


[Information on J2000 coordinates](https://en.wikipedia.org/wiki/Equinox_\(celestial_coordinates\)#J2000.0)


[A brief description on RA and DEC](https://astronomy.swin.edu.au/cosmos/e/equatorial+coordinate+system)
