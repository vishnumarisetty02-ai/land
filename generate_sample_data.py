"""
GeoVision AI - Realistic Village Survey Sample Data Generator
Generates sample datasets:
1. sample_data/sample_drone_orthomosaic.tif (GeoTIFF)
2. sample_data/sample_drone_dsm.tif (Digital Surface Model GeoTIFF)
3. sample_data/sample_drone_dtm.tif (Digital Terrain Model GeoTIFF)
4. sample_data/sample_cadastral_parcels.geojson (Village Cadastral GeoJSON)
5. sample_data/sample_cadastral_shapefile.zip (Shapefile package)
"""

import os
import zipfile
import tempfile
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import rasterio
from rasterio.transform import from_bounds

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Georeferenced bounds in Guntur/Palnadu district region, Andhra Pradesh (EPSG:4326)
BOUNDS = (78.098, 16.498, 78.108, 16.511)
WIDTH, HEIGHT = 512, 512

def generate_drone_rasters():
    transform = from_bounds(*BOUNDS, WIDTH, HEIGHT)
    y, x = np.mgrid[0:HEIGHT, 0:WIDTH]

    # 1. ORTHOMOSAIC RGB
    red = (115 + 30 * np.sin(x / 40.0) + 20 * np.cos(y / 35.0)).astype(np.uint8)
    green = (155 + 40 * np.cos(x / 45.0) + 30 * np.sin(y / 40.0)).astype(np.uint8)
    blue = (85 + 25 * np.sin((x + y) / 50.0)).astype(np.uint8)

    # Add realistic field bunds / boundary hedgerows (natural green/brown lines)
    bund_mask = ((x % 85 < 4) | (y % 85 < 4))
    red[bund_mask] = 55
    green[bund_mask] = 85
    blue[bund_mask] = 45

    # Add Panchayat Village Road (running horizontally across survey numbers)
    road_mask = (y >= 250) & (y <= 265)
    red[road_mask] = 190
    green[road_mask] = 190
    blue[road_mask] = 195

    # Add Irrigation Canal (running vertically along East boundary)
    canal_mask = (x >= 470) & (x <= 488)
    red[canal_mask] = 40
    green[canal_mask] = 95
    blue[canal_mask] = 150

    # Add farm houses / sheds
    buildings = [(120, 140), (130, 320), (320, 160), (360, 340)]
    for bx, by in buildings:
        b_mask = (x >= bx) & (x <= bx + 35) & (y >= by) & (y <= by + 28)
        red[b_mask] = 215
        green[b_mask] = 110
        blue[b_mask] = 85

    rgb_stack = np.stack([red, green, blue], axis=0)
    ortho_path = os.path.join(OUTPUT_DIR, "sample_drone_orthomosaic.tif")
    with rasterio.open(
        ortho_path, "w", driver="GTiff", height=HEIGHT, width=WIDTH, count=3, dtype="uint8", crs="EPSG:4326", transform=transform
    ) as dst:
        dst.write(rgb_stack)
    print(f"Generated: {ortho_path}")

    # 2. DTM (Digital Terrain Model - Bare Ground Elevation AMSL in meters)
    # Natural gentle slope from South-West (42.0m) to North-East (47.5m)
    dtm = (42.0 + 3.2 * (x / WIDTH) + 2.3 * (y / HEIGHT) + 0.4 * np.sin(x / 25.0)).astype(np.float32)
    dtm_path = os.path.join(OUTPUT_DIR, "sample_drone_dtm.tif")
    with rasterio.open(
        dtm_path, "w", driver="GTiff", height=HEIGHT, width=WIDTH, count=1, dtype="float32", crs="EPSG:4326", transform=transform
    ) as dst:
        dst.write(dtm, 1)
    print(f"Generated: {dtm_path}")

    # 3. DSM (Digital Surface Model - Ground + Structures + Trees)
    dsm = dtm.copy()
    # Add farm building heights (+6.5m to +8.5m)
    for bx, by in buildings:
        dsm[by:by+28, bx:bx+35] += 7.8
    
    # Add orchard tree canopies along field bunds (+3.5m to +5.5m)
    tree_spots = (bund_mask & (dsm == dtm))
    rng = np.random.default_rng(42)
    dsm[tree_spots] += rng.uniform(3.0, 5.5, size=np.count_nonzero(tree_spots)).astype(np.float32)

    dsm_path = os.path.join(OUTPUT_DIR, "sample_drone_dsm.tif")
    with rasterio.open(
        dsm_path, "w", driver="GTiff", height=HEIGHT, width=WIDTH, count=1, dtype="float32", crs="EPSG:4326", transform=transform
    ) as dst:
        dst.write(dsm, 1)
    print(f"Generated: {dsm_path}")


def generate_cadastral_dataset():
    # Authentic village cadastral parcels with revenue Survey Numbers
    parcels_data = [
        {
            "survey_no": "142/2A",
            "patta_no": "8842",
            "pattadar": "V. R. Krishna Rao",
            "land_use": "Agriculture (Paddy/Orchard)",
            "village": "Venkatapuram",
            "deed_acres": 1.06,
            "geometry": Polygon([
                [78.1000, 16.5000],
                [78.1030, 16.5000],
                [78.1030, 16.5035],
                [78.1004, 16.5038],
                [78.1000, 16.5020],
                [78.1000, 16.5000]
            ])
        },
        {
            "survey_no": "142/1",
            "patta_no": "6410",
            "pattadar": "B. Ramaiah",
            "land_use": "Agriculture",
            "village": "Venkatapuram",
            "deed_acres": 1.25,
            "geometry": Polygon([
                [78.1030, 16.5000],
                [78.1065, 16.5002],
                [78.1065, 16.5035],
                [78.1030, 16.5035],
                [78.1030, 16.5000]
            ])
        },
        {
            "survey_no": "142/2B",
            "patta_no": "9201",
            "pattadar": "K. Venkataswamy",
            "land_use": "Agriculture",
            "village": "Venkatapuram",
            "deed_acres": 0.98,
            "geometry": Polygon([
                [78.1004, 16.5038],
                [78.1030, 16.5035],
                [78.1030, 16.5070],
                [78.1008, 16.5072],
                [78.1004, 16.5038]
            ])
        },
        {
            "survey_no": "143",
            "patta_no": "5512",
            "pattadar": "Smt. Lakshmi Devi",
            "land_use": "Commercial / Farmhouse",
            "village": "Venkatapuram",
            "deed_acres": 1.15,
            "geometry": Polygon([
                [78.1030, 16.5035],
                [78.1065, 16.5035],
                [78.1062, 16.5070],
                [78.1030, 16.5070],
                [78.1030, 16.5035]
            ])
        },
        {
            "survey_no": "144",
            "patta_no": "7730",
            "pattadar": "G. Srinivas",
            "land_use": "Agriculture",
            "village": "Venkatapuram",
            "deed_acres": 0.85,
            "geometry": Polygon([
                [78.1008, 16.5072],
                [78.1030, 16.5070],
                [78.1030, 16.5098],
                [78.1005, 16.5098],
                [78.1008, 16.5072]
            ])
        },
        {
            "survey_no": "141 (Road & Canal)",
            "patta_no": "GOVT-101",
            "pattadar": "Gram Panchayat / Irrigation Dept",
            "land_use": "Public Infrastructure",
            "village": "Venkatapuram",
            "deed_acres": 1.20,
            "geometry": Polygon([
                [78.1030, 16.5070],
                [78.1062, 16.5070],
                [78.1065, 16.5098],
                [78.1030, 16.5098],
                [78.1030, 16.5070]
            ])
        }
    ]

    gdf = gpd.GeoDataFrame(parcels_data, crs="EPSG:4326")

    # 1. Save GeoJSON
    geojson_path = os.path.join(OUTPUT_DIR, "sample_cadastral_parcels.geojson")
    gdf.to_file(geojson_path, driver="GeoJSON")
    print(f"Generated: {geojson_path}")

    # 2. Save Shapefile inside ZIP
    zip_path = os.path.join(OUTPUT_DIR, "sample_cadastral_shapefile.zip")
    with tempfile.TemporaryDirectory() as tmp_dir:
        shp_base = os.path.join(tmp_dir, "village_cadastral_parcels.shp")
        gdf.to_file(shp_base, driver="ESRI Shapefile")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in os.listdir(tmp_dir):
                zf.write(os.path.join(tmp_dir, file), arcname=file)
    print(f"Generated: {zip_path}")


if __name__ == "__main__":
    generate_drone_rasters()
    generate_cadastral_dataset()
    print("All sample datasets successfully generated in sample_data/")
