import rioxarray as rxr
import xarray as xr
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import sys
import glob
import re
import time
import datetime

def read_ET_image(image_path):
    # GeoTIFF: use rioxarray to open via rasterio
    et = rxr.open_rasterio(image_path)
    print(et)
    et.plot(vmin=0, vmax=200)
    # plt.colorbar(label="ET (mm)")
    plt.title("ET Image")
    # plt.xlabel("Longitude")
    # plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig("et.png")
    print("ET image saved to et.png")
    # Histogram from first band
    try:
        da = et.squeeze()
        data = da.values
        if data.ndim == 3:
            data = data[0]
        nodata = da.rio.nodata
        mask = np.isfinite(data)
        if nodata is not None:
            mask &= data != nodata
        values = data[mask].ravel()
        plt.figure()
        plt.hist(values, bins=50, color="steelblue", edgecolor="black")
        plt.title("ET value distribution")
        plt.xlabel("ET (mm)")
        plt.ylabel("Pixel count")
        plt.tight_layout()
        plt.savefig("et_hist.png")
        print("Histogram saved to et_hist.png; n=", values.size)
    except Exception as e:
        print("Histogram failed:", e)
    try:
        print("CRS:", et.rio.crs)
        print("Bounds:", et.rio.bounds())
        print("Shape:", et.shape)

    except Exception:
        pass
    return et

if __name__ == "__main__":
    image_path = r"D:\Backup\Rouhin_Lenovo\Misc\OpenET_REST\Download\Data\OpenET_ET_2020_05.tif"
    read_ET_image(image_path)
