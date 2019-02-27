#!/bin/bash

#####################
#usage example:
#./copy_img.sh tq_server orbit_number data_id  dst_dir
#####################
set -e 
tq_server=$1
orbit_number=$2
data_id=$3
dst_dir=$4

if [[ $# < 4 ]]; then
    echo "error args"
    exit
fi

if [ $tq_server = "tq-data04" ]; then
    tq_server="tq-data05"
    echo $tq_server
fi

tmp1="/home/tq/"$tq_server"/sentinel_GRD/$orbit_number/*"$data_id"*/*_TC_DB.data/*VV*.img"
tmp2=$dst_dir"/VV/Sigma0_VV_"$data_id".img"
[ -e "$tmp2" ] || cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/$orbit_number/*"$data_id"*/*_TC_DB.data/*VV*.hdr"
tmp2=$dst_dir"/VV/Sigma0_VV_"$data_id".hdr"
[ -e "$tmp2" ] || cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/$orbit_number/*"$data_id"*/*_TC_DB.data/*VH*.img"
tmp2=$dst_dir"/VH/Sigma0_VH_"$data_id".img"
[ -e "$tmp2" ] || cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/$orbit_number/*"$data_id"*/*_TC_DB.data/*VH*.hdr"
tmp2=$dst_dir"/VH/Sigma0_VH_"$data_id".hdr"
[ -e "$tmp2" ] || cp $tmp1 $tmp2