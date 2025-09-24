# OpenET Monthly Exporter

Export OpenET Ensemble (CONUS GRIDMET monthly v2_0) mosaics from Google Earth Engine to Google Drive at 30 m resolution, clipped to a boundary.

## Setup

1. Create a conda environment and install requirements:

```bash
conda create -n openet python=3.11
conda activate openet
pip install -r Download/requirements.txt
```

2. Authenticate Earth Engine (first time):

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
