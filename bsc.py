#!/usr/bin/env python3
from PIL import Image
import urllib.request
import gzip
import numpy as np
import math
import sys
import os


def download_status(blocknum, bs, file_size):
    completed = int((blocknum*bs)/file_size * 99)
    print("\rDownloading [" + completed * "=" + (99 - completed) * " " + "]", flush = True, end="")


def sind(deg):
    return math.sin(deg * math.pi/180)


def cosd(deg):
    return math.cos(deg * math.pi/180)


def check_value(x, size):
    return (x > -size/2 and x < size/2 and y > -size/2 and y < size/2)


if __name__ == "__main__":

    try:
        size = int(sys.argv[1])
    except ValueError:
        print("Size argument must be an integer", file=sys.stderr)
        exit(1)
    except IndexError:
        print("NAME\n\tbsc.py SIZE\n\nDESCRIPTION\n\tbsc.py is a"
              " python script that generates skybox textures of size SIZE x SIZE"
              " px (pixels) \n\tThe script uses the bsc5 star catalouge, which is"
              " optionaly downloaded if not found in the current directory.",
              file=sys.stderr)
        exit(2)

    # ask to download the file if it's not found
    if not os.path.exists("bsc5.dat.gz"):
        print("Catalog not found. Would you like to download it now?\nSource: http://tdc-www.harvard.edu/catalogs/bsc5.dat.gz")

        valid_option = False
        while not valid_option:
            option = input("[Y/n]: ")
            if option in ["Y", "y", "N", "n"]:
                valid_option = True

        if option == "Y" or option == "y":
            print("Download starting...")
            try:
                urllib.request.urlretrieve("http://tdc-www.harvard.edu/catalogs/bsc5.dat.gz", "bsc5.dat.gz", download_status)
                print("\nDownload complete!")
            except KeyboardInterrupt:
                print("\nDownload interrupted. Exiting")
                os.remove("bsc5.dat.gz")  # remove half interuppted thing
                exit(3)

        else:
            print("Please download the file and rerun the script. Exiting.")
            exit(4)

    # arrays to draw into
    xplus = np.zeros((size, size))
    xminus = np.zeros((size, size))
    yplus = np.zeros((size, size))
    yminus = np.zeros((size, size))
    zplus = np.zeros((size, size))
    zminus = np.zeros((size, size))

    
    with gzip.open("bsc5.dat.gz") as bsc5cat:
        for bline in bsc5cat:
            line = bline.decode()

            try:
                rah = int(line[75:77])  # RA hours
                ram = int(line[77:79])  # RA minutes
                ras = float(line[79:83])  # RA seconds

                dec_sign = 1 if line[83] == "+" else -1
                decd = int(line[84:86])  # DEC degress
                decm = int(line[86:88])  # DEC minutes
                decs = int(line[88:90])  # DEC seconds

                vis_mag = float(line[102:107])  # visual magnitude

            except ValueError:
                print("Skipping incomplete data", file=sys.stderr)
                continue

            # convert to degrees
            dec_deg = (decd+(1.0/60.0)*decm+(1.0/3600.0)*decs)*dec_sign
            ra_deg = (rah+(1.0/60.0)*ram+(1.0/3600.0)*ras) * 15.0
            
            # sanity check the range
            if ra_deg > 360.0:
                ra_deg -= 360.0
            if ra_deg > 360.0:
                ra_deg -= 360.0
            if ra_deg < 0.0:
                ra_deg += 360.0
            if ra_deg < 0.0:
                ra_deg += 360.0

            # plot the stars

            # convert to vector
            xx = cosd(dec_deg) * cosd(ra_deg)
            yy = cosd(dec_deg) * sind(ra_deg)
            zz = sind(dec_deg)

            # normalise vector
            l = math.sqrt(xx*xx + yy*yy + zz*zz)
            xx /= l
            yy /= l
            zz /= l

            # calculate the brightness of the star
            vis_mag = 4.0 if vis_mag >= 5 else vis_mag
            bright = int(min(1.0, math.log(5.0 - vis_mag)) * 255) % 256
            
            if math.fabs(zz) > math.fabs(xx) and math.fabs(zz) > math.fabs(yy) and zz > 0.0:
                # plot in +ve z plane
                x = int(xx * (1/zz) * (size/2))
                y = int(yy * (1/zz) * (size/2))
                
                if check_value(x, size):
                    zplus[size//2 + y, size//2 + x] = bright
                    
            if math.fabs(zz) > math.fabs(xx) and math.fabs(zz) > math.fabs(yy) and zz < 0.0:
                # plot in -ve z plane
                x = int(xx * (1/zz) * (size/2))
                y = int(yy * (1/zz) * (size/2))

                if check_value(x, size):
                    zminus[size//2 + y, size//2 - x] = bright

            if math.fabs(xx) > math.fabs(zz) and math.fabs(xx) > math.fabs(yy) and xx > 0.0:
                # plot in +ve x plane
                x = int(yy * (1.0/xx) * (size/2.0))
                y = int(zz * (1.0/xx) * (size/2.0))

                if check_value(x, size):
                    xplus[size//2 - y, size//2 - x] = bright

            if math.fabs(xx) > math.fabs(zz) and math.fabs(xx) > math.fabs(yy) and xx < 0.0:
                # plot in -ve x plane
                x = int(yy * (1.0/xx) * (size/2.0))
                y = int(zz * (1.0/xx) * (size/2.0))

                if check_value(x, size):
                    xminus[size//2 - y, size//2 - x] = bright

            if math.fabs(yy) > math.fabs(zz) and math.fabs(yy) > math.fabs(xx) and yy > 0.0:
                # plot in +ve y plane
                x = int(xx * (1.0/yy) * (size/2.0))
                y = int(zz * (1.0/yy) * (size/2.0))

                if check_value(x, size):
                    yplus[size//2 - y, size//2 + x] = bright

            if math.fabs(yy) > math.fabs(zz) and math.fabs(yy) and math.fabs(xx) and yy < 0.0:
                # plot in -ve y plane
                x = int(xx * (1.0/yy) * (size/2.0))
                y = int(zz * (1.0/yy) * (size/2.0))

                if check_value(x, size):
                    yminus[size//2 - y, size//2 + x] = bright

    # write to images
    Image.fromarray(xplus).convert("RGB").save("xplus.png")
    Image.fromarray(xminus).convert("RGB").save("xminus.png")
    Image.fromarray(yplus).convert("RGB").save("yplus.png")
    Image.fromarray(yminus).convert("RGB").save("yminus.png")
    Image.fromarray(zplus).convert("RGB").save("zplus.png")
    Image.fromarray(zminus).convert("RGB").save("zminus.png")
