#!/bin/bash

#####################
#usage example:
#./merge_img.sh src_tif_dir dst_tif_dir dst_big_tif_name palm_or_cdl [PATCH_TIF]
#./merge_img.sh /tmp/palm-s1-2015  /home/tq/data_pool/Ray_EX/palm/2015 s1-2015-palm palm
#####################
set -e 
SRC_DIR=$1
DST_DIR=$2
DST_NAME=$3
PALM_CDL=$4
PATCH_TIF=$5

if [[ $# < 4 ]]; then
    echo "error args"
    exit
fi
TIME_SUFFIX=$(date +"%Y%m%d%H%M%S")

mkdir -p $DST_DIR && cd $DST_DIR
if [[ $PALM_CDL = "palm" || $PALM_CDL = "water" ]]; then
    cp ~/data_pool/Ray_EX/PRJ_FILE/palm_wgs84.prj wgs84.prj
    TR_SIZE='20 20'
elif [[ $PALM_CDL = "cdl" ]]; then
    cp ~/data_pool/Ray_EX/PRJ_FILE/cdlwgs84.prj wgs84.prj
    TR_SIZE='30 30'
fi

for f in $(ls $SRC_DIR/*.tif)
do 
    n=${f##*/}
    [ -e $DST_DIR/$n-*.wgs84.tif ] || gdalwarp -t_srs wgs84.prj -r cubic -srcnodata 10000 -dstnodata 10000 -of GTiff -overwrite $f $DST_DIR/$n-$TIME_SUFFIX.wgs84.tif
done
    
for i in $(ls $DST_DIR/*-$TIME_SUFFIX.wgs84.tif); do gdalbuildvrt -vrtnodata "10000" -r cubic $i-vrt.vrt $i ; done

gdalbuildvrt -vrtnodata "10000"  $DST_DIR/$DST_NAME.vrt $PATCH_TIF $(ls $DST_DIR/*-vrt.vrt)

gdal_translate -tr $TR_SIZE -r cubic -of GTiff $DST_DIR/$DST_NAME.vrt $DST_DIR/$DST_NAME.tif
rm -rf $DST_DIR/*-vrt.vrt
rm -rf $DST_DIR/*-$TIME_SUFFIX.wgs84.tif