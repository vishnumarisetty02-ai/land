"""
GeoVision AI - Comprehensive Village Cadastral (FMB) Dataset Generator
Generates:
1. sample_data/cadastral_village_fmb.geojson (GeoJSON)
2. sample_data/cadastral_village_fmb.zip (ESRI Shapefile package)
3. sample_data/cadastral_village_fmb.kml (Google Earth KML)
4. sample_data/cadastral_village_fmb.csv (Attributes and Coordinates CSV)
"""

import os
import json
import zipfile
import tempfile
import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "sample_data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_rich_cadastral_dataset():
    # 8 realistic contiguous village cadastral parcels covering Survey Block 141-146
    # Region: Venkatapuram Village, Narasaraopet Mandal, Palnadu District, Andhra Pradesh
    parcels_data = [
        {
            "survey_no": "142/2A",
            "sub_div": "2A",
            "khata_no": "8842",
            "patta_no": "AP-PLN-1422A",
            "pattadar": "V. R. Krishna Rao",
            "relation": "S/o Venkata Subbaiah",
            "land_class": "Dry Land (Metta / Orchard)",
            "land_use": "Agriculture (Horticulture/Citrus)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 106.0,
            "area_acres": 1.06,
            "market_val": "₹ 42,40,000",
            "north_bnd": "12m Panchayat Road & Sy. No. 141",
            "south_bnd": "Sy. No. 142/1 (B. Ramaiah Land)",
            "east_bnd": "Irrigation Ayacut Canal",
            "west_bnd": "Sy. No. 143 (Smt. Lakshmi Devi Plot)",
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
            "sub_div": "1",
            "khata_no": "6410",
            "patta_no": "AP-PLN-1421",
            "pattadar": "B. Ramaiah",
            "relation": "S/o Kotayya",
            "land_class": "Wet Land (Magani / Double Crop)",
            "land_use": "Agriculture (Paddy / Rice)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 125.0,
            "area_acres": 1.25,
            "market_val": "₹ 56,25,000",
            "north_bnd": "Sy. No. 143",
            "south_bnd": "Village Boundary & Drain",
            "east_bnd": "Irrigation Canal",
            "west_bnd": "Sy. No. 142/2A",
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
            "sub_div": "2B",
            "khata_no": "9201",
            "patta_no": "AP-PLN-1422B",
            "pattadar": "K. Venkataswamy",
            "relation": "S/o Narayana",
            "land_class": "Dry Land (Metta)",
            "land_use": "Agriculture (Cotton / Chilli)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 98.0,
            "area_acres": 0.98,
            "market_val": "₹ 39,20,000",
            "north_bnd": "Sy. No. 144",
            "south_bnd": "Sy. No. 142/2A",
            "east_bnd": "Sy. No. 143",
            "west_bnd": "Sy. No. 140 (Cart Track)",
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
            "sub_div": "0",
            "khata_no": "5512",
            "patta_no": "AP-PLN-143",
            "pattadar": "Smt. Lakshmi Devi",
            "relation": "W/o Appa Rao",
            "land_class": "Converted Non-Agriculture",
            "land_use": "Commercial / Farmhouse & Solar Pump",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 115.0,
            "area_acres": 1.15,
            "market_val": "₹ 69,00,000",
            "north_bnd": "Sy. No. 141 (Panchayat Road)",
            "south_bnd": "Sy. No. 142/1",
            "east_bnd": "Irrigation Canal",
            "west_bnd": "Sy. No. 142/2B",
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
            "sub_div": "0",
            "khata_no": "7730",
            "patta_no": "AP-PLN-144",
            "pattadar": "G. Srinivas",
            "relation": "S/o Ranga Rao",
            "land_class": "Dry Land (Metta)",
            "land_use": "Agriculture (Maize / Pulses)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 85.0,
            "area_acres": 0.85,
            "market_val": "₹ 34,00,000",
            "north_bnd": "Sy. No. 145",
            "south_bnd": "Sy. No. 142/2B",
            "east_bnd": "Sy. No. 141",
            "west_bnd": "Sy. No. 139",
            "geometry": Polygon([
                [78.1008, 16.5072],
                [78.1030, 16.5070],
                [78.1030, 16.5098],
                [78.1005, 16.5098],
                [78.1008, 16.5072]
            ])
        },
        {
            "survey_no": "141",
            "sub_div": "0",
            "khata_no": "GOVT-101",
            "patta_no": "AP-GOVT-PORAMBOKE",
            "pattadar": "Gram Panchayat & Irrigation Dept",
            "relation": "Government Land (Poramboke)",
            "land_class": "Government Public Utility",
            "land_use": "Panchayat Main Road & Irrigation Channel",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 120.0,
            "area_acres": 1.20,
            "market_val": "Government Public Asset",
            "north_bnd": "Sy. No. 146",
            "south_bnd": "Sy. No. 143 & 142",
            "east_bnd": "Ayacut Canal Bund",
            "west_bnd": "Sy. No. 144",
            "geometry": Polygon([
                [78.1030, 16.5070],
                [78.1062, 16.5070],
                [78.1065, 16.5098],
                [78.1030, 16.5098],
                [78.1030, 16.5070]
            ])
        },
        {
            "survey_no": "145",
            "sub_div": "0",
            "khata_no": "3310",
            "patta_no": "AP-PLN-145",
            "pattadar": "Ch. Venkata Reddy",
            "relation": "S/o Sambasiva Rao",
            "land_class": "Dry Land (Metta)",
            "land_use": "Agriculture (Tobacco / Cotton)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 92.0,
            "area_acres": 0.92,
            "market_val": "₹ 36,80,000",
            "north_bnd": "Hillock / Forest Border",
            "south_bnd": "Sy. No. 144",
            "east_bnd": "Sy. No. 146",
            "west_bnd": "Sy. No. 138",
            "geometry": Polygon([
                [78.1005, 16.5098],
                [78.1030, 16.5098],
                [78.1030, 16.5125],
                [78.1002, 16.5125],
                [78.1005, 16.5098]
            ])
        },
        {
            "survey_no": "146",
            "sub_div": "0",
            "khata_no": "4421",
            "patta_no": "AP-PLN-146",
            "pattadar": "M. Satyanarayana",
            "relation": "S/o Subbaiah",
            "land_class": "Wet Land (Magani)",
            "land_use": "Agriculture (Paddy / Banana Plantation)",
            "village": "Venkatapuram",
            "mandal": "Narasaraopet",
            "district": "Palnadu",
            "state": "Andhra Pradesh",
            "area_cents": 110.0,
            "area_acres": 1.10,
            "market_val": "₹ 49,50,000",
            "north_bnd": "Village Boundary",
            "south_bnd": "Sy. No. 141",
            "east_bnd": "Major Irrigation Distributary",
            "west_bnd": "Sy. No. 145",
            "geometry": Polygon([
                [78.1030, 16.5098],
                [78.1065, 16.5098],
                [78.1065, 16.5125],
                [78.1030, 16.5125],
                [78.1030, 16.5098]
            ])
        }
    ]

    gdf = gpd.GeoDataFrame(parcels_data, crs="EPSG:4326")

    # 1. Save GeoJSON
    geojson_path = os.path.join(OUTPUT_DIR, "cadastral_village_fmb.geojson")
    gdf.to_file(geojson_path, driver="GeoJSON")
    print(f"Generated: {geojson_path}")

    # Also keep sample_cadastral_parcels.geojson updated
    gdf.to_file(os.path.join(OUTPUT_DIR, "sample_cadastral_parcels.geojson"), driver="GeoJSON")

    # 2. Save ESRI Shapefile Package (ZIP)
    zip_path = os.path.join(OUTPUT_DIR, "cadastral_village_fmb.zip")
    with tempfile.TemporaryDirectory() as tmp_dir:
        shp_base = os.path.join(tmp_dir, "village_cadastral_fmb.shp")
        # Shorten column names for DBF compliance (10 chars max)
        gdf_shp = gdf.rename(columns={
            "survey_no": "survey_no",
            "sub_div": "sub_div",
            "khata_no": "khata_no",
            "patta_no": "patta_no",
            "pattadar": "pattadar",
            "relation": "relation",
            "land_class": "land_class",
            "land_use": "land_use",
            "village": "village",
            "mandal": "mandal",
            "district": "district",
            "state": "state",
            "area_cents": "cents",
            "area_acres": "acres",
            "market_val": "market_val",
            "north_bnd": "north_bnd",
            "south_bnd": "south_bnd",
            "east_bnd": "east_bnd",
            "west_bnd": "west_bnd"
        })
        gdf_shp.to_file(shp_base, driver="ESRI Shapefile")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for file in os.listdir(tmp_dir):
                zf.write(os.path.join(tmp_dir, file), arcname=file)
    print(f"Generated: {zip_path}")
    # Also update sample_cadastral_shapefile.zip
    import shutil
    shutil.copy2(zip_path, os.path.join(OUTPUT_DIR, "sample_cadastral_shapefile.zip"))

    # 3. Save KML (Google Earth)
    kml_path = os.path.join(OUTPUT_DIR, "cadastral_village_fmb.kml")
    kml_content = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        '  <name>Village Cadastral FMB Map - Venkatapuram</name>',
        '  <description>Revenue Cadastral Map for Drone Land Survey Verification</description>',
        '  <Style id="cadastral_style">',
        '    <LineStyle><color>ff00aaff</color><width>2.5</width></LineStyle>',
        '    <PolyStyle><color>4400aaff</color></PolyStyle>',
        '  </Style>'
    ]
    for p in parcels_data:
        coords_kml = " ".join([f"{c[0]},{c[1]},0" for c in p["geometry"].exterior.coords])
        kml_content.extend([
            '  <Placemark>',
            f'    <name>Sy. No. {p["survey_no"]}</name>',
            '    <description><![CDATA[',
            f'      <b>Pattadar:</b> {p["pattadar"]}<br/>',
            f'      <b>Patta No:</b> {p["patta_no"]}<br/>',
            f'      <b>Area:</b> {p["area_cents"]} Cents ({p["area_acres"]} Ac)<br/>',
            f'      <b>Classification:</b> {p["land_class"]}<br/>',
            f'      <b>Village:</b> {p["village"]}, {p["mandal"]}<br/>',
            f'      <b>North:</b> {p["north_bnd"]}<br/>',
            f'      <b>South:</b> {p["south_bnd"]}<br/>',
            f'      <b>East:</b> {p["east_bnd"]}<br/>',
            f'      <b>West:</b> {p["west_bnd"]}',
            '    ]]></description>',
            '    <styleUrl>#cadastral_style</styleUrl>',
            '    <Polygon>',
            '      <outerBoundaryIs><LinearRing><coordinates>',
            f'        {coords_kml}',
            '      </coordinates></LinearRing></outerBoundaryIs>',
            '    </Polygon>',
            '  </Placemark>'
        ])
    kml_content.extend(['</Document>', '</kml>'])
    with open(kml_path, "w", encoding="utf-8") as f:
        f.write("\n".join(kml_content))
    print(f"Generated: {kml_path}")

    # 4. Save CSV
    csv_rows = []
    for p in parcels_data:
        coords_str = "; ".join([f"({c[1]:.6f}, {c[0]:.6f})" for c in p["geometry"].exterior.coords[:-1]])
        csv_rows.append({
            "Survey Number": p["survey_no"],
            "Sub-Division": p["sub_div"],
            "Khata Number": p["khata_no"],
            "Patta Passbook No": p["patta_no"],
            "Pattadar Name": p["pattadar"],
            "Relation / Guardian": p["relation"],
            "Land Classification": p["land_class"],
            "Land Use": p["land_use"],
            "Area (Cents)": p["area_cents"],
            "Area (Acres)": p["area_acres"],
            "Market Valuation": p["market_val"],
            "North Boundary": p["north_bnd"],
            "South Boundary": p["south_bnd"],
            "East Boundary": p["east_bnd"],
            "West Boundary": p["west_bnd"],
            "Corner Coordinates (Lat, Long)": coords_str
        })
    csv_path = os.path.join(OUTPUT_DIR, "cadastral_village_fmb.csv")
    pd.DataFrame(csv_rows).to_csv(csv_path, index=False, encoding="utf-8")
    print(f"Generated: {csv_path}")

    # Copy files to Downloads and Desktop
    downloads = os.path.expanduser('~/Downloads')
    onedrive_desktop = os.path.expanduser('~/OneDrive/Desktop')
    for f_name in ["cadastral_village_fmb.geojson", "cadastral_village_fmb.zip", "cadastral_village_fmb.kml", "cadastral_village_fmb.csv"]:
        src_f = os.path.join(OUTPUT_DIR, f_name)
        if os.path.exists(downloads):
            shutil.copy2(src_f, os.path.join(downloads, f_name))
        if os.path.exists(onedrive_desktop):
            shutil.copy2(src_f, os.path.join(onedrive_desktop, f_name))

if __name__ == "__main__":
    generate_rich_cadastral_dataset()
    print("Cadastral dataset generation complete across all formats!")
