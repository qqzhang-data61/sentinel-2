import os

home_dir = os.path.expanduser("~")

MPOB_data = {
    "2017": {
        "Overall": 5811145,
        "peninsula": 2708413,
        "Johor": 748860,
        "Kedah": 87538,
        "Kelantan": 158310,
        "Melaka": 57372,
        "Negeri Sembilan": 184815,
        "Pahang": 741495,
        "Perak": 406469,
        "Perlis": 660,
        "Pulau Pinang": 13563,
        "Sabah": 1546904,
        "Sarawak": 1555828,
        "Selangor": 137783,
        "Trengganu": 171548,
    },
    "2016": {
        "Overall": 5737985,
        "peninsula": 2679502,
        "Johor": 745630,
        "Kedah": 87786,
        "Kelantan": 155458,
        "Melaka": 56149,
        "Negeri Sembilan": 178958,
        "Pahang": 732052,
        "Perak": 397908,
        "Perlis": 652,
        "Pulau Pinang": 14135,
        "Sabah": 1551714,
        "Sarawak": 1506769,
        "Selangor": 138831,
        "Trengganu": 171943,
    },
}

valid_states = [
    "Johor",
    "Melaka",
    "Negeri Sembilan",
    "Pahang",
    "Perak",
    "Selangor",
    "Trengganu",
]

shape_path = {
    "peninsula": {
        "Overall": home_dir + "/data_pool/zgq/vector/malay.shp",
        "Johor": home_dir + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Johor.shp",
        "Kedah": home_dir + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Kedah.shp",
        "Kelantan": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Kelantan.shp",
        "Melaka": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Melaka.shp",
        "Negeri Sembilan": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Negeri_Sembilan.shp",
        "Pahang": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Pahang.shp",
        "Perak": home_dir + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Perak.shp",
        "Perlis": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Perlis.shp",
        "Pulau Pinang": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Pulau_Pinang.shp",
        "Sabah": home_dir + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Sabah.shp",
        "Sarawak": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Sarawak.shp",
        "Selangor": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Selangor.shp",
        "Trengganu": home_dir
        + "/data_pool/Palm/Palm_Shape/peninsula_Shp/states/Trengganu.shp",
    }
}

raster_path = {
    "peninsula": {
        "201703": {
            "trainData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201703.npz",
            "auxData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_aux_L0913_peninsula_201703.npz",
            "VV": home_dir + "/data_pool/Palm/MLY_data/sentinel_201703/VV_malay_13.tif",
            "VH": home_dir + "/data_pool/Palm/MLY_data/sentinel_201703/VH_malay_13.tif",
            "EVI": home_dir + "/data_pool/Palm/palm_NDVI/201703/EVI_malay_201703.tif",
            "NDVI": home_dir + "/data_pool/Palm/palm_NDVI/201703/NDVI_malay_201703.tif",
        },
        "201706": {
            "trainData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201706.npz",
            "auxData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_aux_L0913_peninsula_201706.npz",
            "VV": home_dir + "/data_pool/Palm/MLY_data/sentinel_201706/VV_malay_13.tif",
            "VH": home_dir + "/data_pool/Palm/MLY_data/sentinel_201706/VH_malay_13.tif",
            "EVI": home_dir + "/data_pool/Palm/palm_NDVI/201706/EVI_malay_201706.tif",
            "NDVI": home_dir + "/data_pool/Palm/palm_NDVI/201706/NDVI_malay_201706.tif",
        },
        "201709": {
            "trainData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201709.npz",
            "auxData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_aux_L0913_peninsula_201709.npz",
            "VV": home_dir + "/data_pool/Palm/MLY_data/sentinel_201709/VV_malay_13.tif",
            "VH": home_dir + "/data_pool/Palm/MLY_data/sentinel_201709/VH_malay_13.tif",
            "EVI": home_dir + "/data_pool/Palm/palm_NDVI/201709/EVI_malay_201709.tif",
            "NDVI": home_dir + "/data_pool/Palm/palm_NDVI/201709/NDVI_malay_201709.tif",
        },
        "201712": {
            "trainData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201712.npz",
            "auxData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_aux_L0913_peninsula_201712.npz",
            "VV": home_dir + "/data_pool/Palm/MLY_data/sentinel_201712/VV_malay_13.tif",
            "VH": home_dir + "/data_pool/Palm/MLY_data/sentinel_201712/VH_malay_13.tif",
            "EVI": home_dir + "/data_pool/Palm/palm_NDVI/201712/EVI_malay_201712.tif",
            "NDVI": home_dir + "/data_pool/Palm/palm_NDVI/201712/NDVI_malay_201712.tif",
        },
        "201609": {
            "trainData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201609.npz",
            "auxData": home_dir
            + "/tq-data05/Palm_test/peninsula data/train/traindata_s1_L0913_peninsula_201609.npz",
            "VV": home_dir + "/data_pool/Palm/MLY_data/sentinel_201609/VV_13.tif",
            "VH": home_dir + "/data_pool/Palm/MLY_data/sentinel_201609/VH_13.tif",
            "EVI": home_dir + "/data_pool/Palm/palm_NDVI/201609/EVI_malay_201609.tif",
            "NDVI": home_dir + "/data_pool/Palm/palm_NDVI/201609/NDVI_malay_201609.tif",
        },
        "DEM": home_dir + "/data_pool/Palm/palm_dem/malay/maly_dem_clip.tif",
        "Slope": home_dir + "/data_pool/Palm/palm_dem/malay/maly_dem_slope_clip.tif",
        "Aspect": home_dir + "/data_pool/Palm/palm_dem/malay/maly_dem_aspect_clip.tif",
    }
}

testData_path = {
    "peninsula": {
        "201609": home_dir + "/tq-data05/Palm_test/Palm/testdata_peninsula_201609.npy",
        "201703": home_dir + "/tq-data05/Palm_test/Palm/testdata_peninsula_201703.npy",
        "201706": home_dir + "/tq-data05/Palm_test/Palm/testdata_peninsula_201706.npy",
        "201709": home_dir + "/tq-data05/Palm_test/Palm/testdata_peninsula_201709.npy",
        "201712": home_dir + "/tq-data05/Palm_test/Palm/testdata_peninsula_201712.npy",
    }
}

mask_shape_path = {
    "peninsula": home_dir + "/data_pool/Palm/MLY_data/mask/qipa_mask.shp"
}

mask_raster_path = {
    "peninsula": home_dir + "/data_pool/Palm/MLY_data/mask/qipa_mask.tif"
}
