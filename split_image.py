import os
import gdal
import click
import math


@click.command()
@click.option("--in_path_name", help="input path name,full path")
@click.option("--out_path", help="out_path path ,full path")
@click.option("--output_filename", help="output_filename suffix")
def clip_tif(in_path_name, out_path, output_filename):
    """
    python3 split_image.py --in_path_name=/home/tq/data_pool/Flood/flood2018/water/water-2018-rgb.tif --out_path=/home/tq/data2/ray/flood/ --output_filename=split_
    """
    assert in_path_name[0] == "/"
    in_path = "/" + "/".join(in_path_name.strip("/").split("/")[:-1]) + "/"
    input_filename = in_path_name.strip("/").split("/")[-1]
    print(in_path, input_filename)
    out_path = out_path
    output_filename = output_filename
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    ds = gdal.Open(in_path + input_filename)
    band = ds.GetRasterBand(1)
    xsize = band.XSize
    ysize = band.YSize
    tile_x = 2048
    tile_y = 2048
    print(xsize, ysize)

    for i, col in zip(range(0, xsize, tile_x), range(1, math.ceil(xsize / tile_x) + 1)):
        # set off x
        if i != 0:
            i = i - 200

        # set last x
        if i + tile_x > xsize:
            i = xsize - 2048

        for j, raw in zip(
            range(0, ysize, tile_y), range(1, math.ceil(ysize / tile_y) + 1)
        ):
            # set j off
            if j != 0:
                j = j - 200

            # set last j
            if j + tile_y > ysize:
                j = ysize - 2048

            com_string = (
                "gdal_translate -of GTIFF -srcwin "
                + str(i)
                + ", "
                + str(j)
                + ", "
                + str(tile_x)
                + ", "
                + str(tile_y)
                + " "
                # + "-a_nodata"
                # + " "
                # + "0 "
                # + " "
                + str(in_path)
                + str(input_filename)
                + " "
                + str(out_path)
                + str(output_filename)
                + str(raw)
                + "_"
                + str(col)
                + ".tif"
            )
            os.system(com_string)


if __name__ == "__main__":
    clip_tif()
