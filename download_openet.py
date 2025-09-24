import ee
import geopandas as gpd
from get_boundary import read_shapefile
import geemap
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule
import time


def split_date_range_into_months(start_date_str, end_date_str):
    """
    Splits a date range into lists of the first and last day of each month.
    """
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    start_dates = []
    end_dates = []
    
    # Generate the first day of each month in the range
    for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        first_day = dt.strftime("%Y-%m-%d")
        # Get the last day by adding one month and subtracting one day
        last_day = (dt + relativedelta(months=1) - relativedelta(days=1)).strftime("%Y-%m-%d")
        
        start_dates.append(first_day)
        end_dates.append(last_day)
        
    return start_dates, end_dates

def get_OpenET_Ensemble(boundary:ee.Geometry, start_date:str, end_date:str):
    # Filter by boundary and month, then mosaic to a single image
    ic = ee.ImageCollection("OpenET/ENSEMBLE/CONUS/GRIDMET/MONTHLY/v2_0").\
        select("et_ensemble_mad").filterBounds(boundary).\
        filterDate(start_date, end_date)
    print("Original images", ic.size().getInfo())
    # Use the first image's projection (30 m) for the mosaic
    first_proj = ic.first().select("et_ensemble_mad").projection()
    mosaic = ic.mosaic().setDefaultProjection(first_proj).\
        set({"system:time_start": ee.Date(start_date).millis()})
    # Print native scale and projection for verification (should be ~30 m)
    try:
        native_scale = mosaic.projection().nominalScale().getInfo()
        print("Mosaic nominal scale (m):", native_scale)
        print("Mosaic projection:", mosaic.projection().getInfo())
    except Exception as e:
        print("Could not fetch projection info:", e)
    return mosaic

def export_image_to_drive(image, year, month, region_geom, drive_folder=None):
    """
    Creates and starts an export task using the image's own projection.
    """
    filename = f'OpenET_ET_{year}_{month:02d}'
    
    # Export at 30 m in a projected CRS to ensure meter-based pixels
    export_scale_m = 30
    export_crs = "EPSG:5070"  # Albers Equal Area CONUS
    print("Exporting at", export_scale_m, "m with CRS", export_crs)
    export_args = dict(
        image=image,
        description=filename,
        fileNamePrefix=filename,
        region=region_geom.geometry(),
        fileFormat='GeoTIFF',
        scale=export_scale_m,
        crs=export_crs,
        maxPixels=1e13,
    )
    if drive_folder:
        export_args["folder"] = drive_folder
    task = ee.batch.Export.image.toDrive(**export_args)
    
    task.start()
    print(f"--> Submitted export task for {year}-{month:02d}")

if __name__ == "__main__":
    project_ID = "ee-rouhinmitraucla"
    ee.Initialize(project=project_ID)
    shapefile_path = "D:\Backup\Rouhin_Lenovo\Misc\OpenET_REST\Download\OpenET_extent\OpenET_extent\Spatial_ext.shp"
    # Export all images to a single, consistent Drive folder
    google_drive_folder = "OpenET_exports"

    boundary = read_shapefile(shapefile_path)
    # Create a geometry object from the boundary
    geometry = geemap.gdf_to_ee(boundary)

    overall_start_date = "2020-04-01"
    overall_end_date = "2020-06-30"

    start_dates, end_dates = split_date_range_into_months(overall_start_date, overall_end_date)
    # monthly_et_mosaics = []

    # To avoid Drive creating duplicate folders when many tasks start at once,
    # we submit exports sequentially with a small delay. If you manually
    # create the folder in Drive beforehand, you may set delay_seconds to 0.
    delay_seconds = 2
    for start_date, end_date in zip(start_dates, end_dates):
        openet_mosaic = get_OpenET_Ensemble(geometry, start_date, end_date)
        year = int(start_date.split("-")[0])
        month = int(start_date.split("-")[1])
        # openet_mosaic.save(f"{google_drive_folder}/ET_{year}_{month}.tif")
        export_image_to_drive(openet_mosaic, year, month, geometry, google_drive_folder)

        print(f"ET_{year}_{month}.tif saved to Google Drive")
        # monthly_et_mosaics.append(openet_mosaic)
        if delay_seconds > 0:
            time.sleep(delay_seconds)

    print(f"\Processing {len(start_dates)} monthly images.")

    # print(openet_ensemble)
    # Get the data for the boundary
    # openet_clipped = openet_ensemble.clip(geometry)
