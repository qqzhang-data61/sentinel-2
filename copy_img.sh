#!/bin/bash

#####################
#usage example:
#./cope.sh tq_server data_id  dst_dir
#####################
set -e 
tq_server=$1
data_id=$2
dst_dir=$3

if [[ $# < 3 ]]; then
    echo "error args"
    exit
fi

tmp1="/home/tq/"$tq_server"/sentinel_GRD/*/*"$data_id"*/*_TC_DB.data/*VV*.img"
tmp2=$dst_dir"VV/Sigma0_VV_"$data_id".img"
cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/*/*"$data_id"*/*_TC_DB.data/*VV*.hdr"
tmp2=$dst_dir"VV/Sigma0_VV_"$data_id".hdr"
cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/*/*"$data_id"*/*_TC_DB.data/*VH*.img"
tmp2=$dst_dir"VH/Sigma0_VH_"$data_id".img"
cp $tmp1 $tmp2

tmp1="/home/tq/"$tq_server"/sentinel_GRD/*/*"$data_id"*/*_TC_DB.data/*VH*.hdr"
tmp2=$dst_dir"VH/Sigma0_VH_"$data_id".hdr"
cp $tmp1 $tmp2