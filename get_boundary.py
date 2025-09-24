import geopandas as gpd 
import pandas as pd
import matplotlib.pyplot as plt

def read_shapefile(filepath:str):
    boundary = gpd.read_file(filepath)
    # print(boundary.head())
    print(boundary.crs)
    if boundary.crs != "EPSG:4326":
        boundary = boundary.to_crs("EPSG:4326")
    ## The polygon has too many vertices so the retrival takes too much time by EE[solution is to convert the boundary to a box]
    boundary = boundary.dissolve()
    boundary = boundary.envelope.to_frame(name='geometry')
    # Create and save the plot
    boundary.plot()
    plt.savefig("boundary.png")
    print("\nPlot saved to boundary.png")
    return boundary

if __name__ == "__main__":
    # Replace with the path to the boundary file
    boundary = read_shapefile("D:\Backup\Rouhin_Lenovo\Misc\OpenET_REST\Download\OpenET_extent\OpenET_extent\Spatial_ext.shp")
    print(boundary)