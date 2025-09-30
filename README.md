# OpenET Monthly Exporter

Export OpenET Ensemble Monthly Evapotranspiration v2.0 mosaics from Google Earth Engine to Google Drive at 30 m resolution, clipped to a boundary.

## Dataset Information

This tool uses the [OpenET Ensemble Monthly Evapotranspiration v2.0](https://developers.google.com/earth-engine/datasets/catalog/OpenET_ENSEMBLE_CONUS_GRIDMET_MONTHLY_v2_0#image-properties) dataset from Google Earth Engine.

**Key Features:**
- **Spatial Resolution:** 30 meters × 30 meters (0.22 acres per pixel)
- **Temporal Coverage:** 1999-10-01 to 2024-12-01
- **Data Type:** Monthly evapotranspiration (ET) as equivalent depth of water in millimeters
- **Models:** Ensemble of 6 ET models (ALEXI/DisALEXI, eeMETRIC, geeSEBAL, PT-JPL, SIMS, SSEBop)
- **License:** CC-BY-4.0
- **Source:** Landsat satellite data

The ensemble ET value is calculated as the mean of the ensemble after filtering outliers using the median absolute deviation approach.

## Setup

Create the conda environment from the full export (exact replica):
```bash
conda env create -f environment_full.yml
conda activate rs  # or the name inside environment_full.yml
```

Authenticate Earth Engine (first time):
```bash
python -c "import ee; ee.Authenticate()"
```

## Usage

Edit the script variables in `Download/download_openet.py`:
```python
# Update these variables in the script:
project_ID = "your-ee-project-id"
shapefile_path = "path/to/your_boundary.shp"
google_drive_folder = "OpenET_exports"
overall_start_date = "2020-04-01"
overall_end_date = "2020-06-30"
```

Then run:
```bash
python Download/download_openet.py
```

## What it does

- Downloads OpenET Ensemble monthly data for your boundary
- Mosaics multiple tiles per month into single images
- Exports at 30m resolution in EPSG:5070 projection
- Saves to Google Drive folder with sequential submission (2s delay between exports)
- Prints mosaic scale and projection info for verification

## Notes

- The script uses the first image's projection for the mosaic to maintain 30m resolution
- Sequential export submission prevents Google Drive from creating duplicate folders
- Adjust `delay_seconds = 2` if you want faster/faster submission

