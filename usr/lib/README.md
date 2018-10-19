# Build

## libgdal.so

```bash
# download
wget http://download.osgeo.org/gdal/2.3.2/gdal-2.3.2.tar.gz
tar xvfz gdal-2.3.2.tar.gz

cd gdal-2.3.2

# Building On Unix With Minimized Drivers
# see: https://trac.osgeo.org/gdal/wiki/BuildingOnUnixWithMinimizedDrivers
./configure \
    --prefix=${PREFIX} \
    --with-geos \
    --with-geotiff \
    --with-hide-internal-symbols \
    --with-libtiff \
    --with-libz \
    --with-threads \
    --without-rasdaman \
    --without-armadillo \
    --without-bsb \
    --without-cfitsio \
    --without-crypto \
    --without-cryptopp \
    --without-curl \
    --without-dwgdirect \
    --without-ecw \
    --without-expat \
    --without-fme \
    --without-freexl \
    --without-gif \
    --without-gif \
    --without-gnm \
    --without-grass \
    --without-grib \
    --without-hdf4 \
    --without-hdf5 \
    --without-idb \
    --without-ingres \
    --without-jasper \
    --without-jp2mrsid \
    --without-jpeg \
    --without-kakadu \
    --without-libgrass \
    --without-libkml \
    --without-libtool \
    --without-mrf \
    --without-mrsid \
    --without-mysql \
    --without-netcdf \
    --without-odbc \
    --without-ogdi \
    --without-openjpeg \
    --without-pcidsk \
    --without-pcraster \
    --without-pcre \
    --without-perl \
    --without-php \
    --without-png \
    --without-python \
    --without-qhull \
    --without-sde \
    --without-sqlite3 \
    --without-webp \
    --without-xerces \
    --without-xml2 \
    --with-pg

make
strip libgdal.so
```

memo: Google App Engine Static data limit
[In all languages except Go, no single static data file can be larger than 32MB. The limit for Go is 64MB.](https://cloud.google.com/appengine/quotas)
libgdal.so < 32MB



# [GEOS](https://trac.osgeo.org/geos/)

```bash
# download
wget http://download.osgeo.org/geos/geos-3.6.3.tar.bz2
tar jxvf geos-3.6.3.tar.bz2

cd geos-3.6.3
./configure \
    --enable-shared

make
cd ./capi/.libs
strip ./capi/.libs/libgeos_c.so.1.10.3
strip ./src/.libs/libgeos-3.6.3.so
```


# [PROJ.4](https://github.com/OSGeo/proj.4/wiki)

```bash
wget http://download.osgeo.org/proj/proj-5.2.0.tar.gz
wget http://download.osgeo.org/proj/proj-datumgrid-1.8.zip
tar xvfz proj-5.2.0.tar.gz
unzip proj-datumgrid-1.8.zip -d proj-5.2.0/nad/
cd proj-5.2.0
./configure
make
strip ./src/.libs/libproj.so.13.1.1
```
