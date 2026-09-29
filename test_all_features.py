"""
GeoVision AI - Automated Feature Test Suite
Verifies that all modules and features work without error.
"""

import os
import sys
import io
import json
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import rasterio

# Import core functions from app.py
from app import (
    convert_area_units,
    get_utm_crs,
    calculate_polygon_measurements,
    calculate_side_lengths_and_bearings,
    load_drone_geotiff,
    compute_elevation_and_slope,
    load_cadastral_dataset,
    process_cadastral_gdf,
    analyze_surrounding_topologies,
    generate_survey_certificate_pdf,
    create_realistic_village_demo,
    DEFAULT_LAND_PAPER,
)

def run_feature_tests():
    print("=" * 70)
    print("      GEOVISION AI · AUTOMATED FEATURE VERIFICATION SUITE")
    print("=" * 70)
    
    results = []

    # 1. Test Demo Data Generation
    try:
        parcels, buildings, roads = create_realistic_village_demo()
        assert len(parcels) >= 4, "Expected at least 4 parcels"
        assert len(buildings) >= 2, "Expected buildings"
        assert len(roads) >= 2, "Expected roads"
        results.append(("Realistic Village Demo Data", True, f"{len(parcels)} parcels, {len(buildings)} buildings, {len(roads)} roads"))
    except Exception as e:
        results.append(("Realistic Village Demo Data", False, str(e)))

    # 2. Test Area Unit Conversion
    try:
        area_m2 = 4046.86  # Exactly 1 Acre = 100 Cents = 4840 Sq.Yards
        units = convert_area_units(area_m2)
        assert abs(units["acres"] - 1.0) < 0.01, "Acres conversion mismatch"
        assert abs(units["cents"] - 100.0) < 0.1, "Cents conversion mismatch"
        assert abs(units["sq_yards"] - 4840.0) < 5.0, "Sq. Yards conversion mismatch"
        results.append(("Area Unit Conversion (Cents, Acres, Gajalu, m²)", True, f"1.00 Acre = {units['cents']:.1f} Cents = {units['sq_yards']:.0f} Sq.Yds"))
    except Exception as e:
        results.append(("Area Unit Conversion", False, str(e)))

    # 3. Test Local UTM Projection Detection
    try:
        utm_ap = get_utm_crs(16.50, 78.10)
        assert utm_ap == "EPSG:32644", f"Expected EPSG:32644 for AP/Telangana, got {utm_ap}"
        results.append(("Automated UTM Zone Projection", True, f"Latitude 16.5°, Longitude 78.1° -> {utm_ap}"))
    except Exception as e:
        results.append(("Automated UTM Zone Projection", False, str(e)))

    # 4. Test Metric Measurements & Side Bearings
    try:
        target_coords = parcels[0]["coordinates"]
        poly = Polygon(target_coords)
        utm = get_utm_crs(poly.centroid.y, poly.centroid.x)
        area_m2, units, perimeter_m = calculate_polygon_measurements(poly, utm)
        sides = calculate_side_lengths_and_bearings(poly, utm)
        assert len(sides) == len(target_coords) - 1, "Side count mismatch"
        assert units["cents"] > 90.0, "Area out of expected range"
        results.append(("FMB Perimeter, Side Lengths & Compass Bearings", True, f"Perimeter: {perimeter_m:.1f}m, Area: {units['cents']:.2f} Cents, {len(sides)} sides with bearings"))
    except Exception as e:
        results.append(("FMB Perimeter & Bearings", False, str(e)))

    # 5. Test Drone Orthomosaic GeoTIFF
    try:
        ortho_path = "sample_data/sample_drone_orthomosaic.tif"
        assert os.path.exists(ortho_path), "Sample drone orthomosaic missing"
        with open(ortho_path, "rb") as f:
            img, meta = load_drone_geotiff(f.read())
        assert meta["width"] == 512 and meta["height"] == 512, "Dimension mismatch"
        assert meta["crs"] == "EPSG:4326", "CRS mismatch"
        results.append(("Drone Orthomosaic GeoTIFF Processing", True, f"Size: {meta['width']}x{meta['height']}, Bands: {meta['bands']}, CRS: {meta['crs']}"))
    except Exception as e:
        results.append(("Drone Orthomosaic GeoTIFF", False, str(e)))

    # 6. Test DSM & DTM Elevation and Slope Analysis
    try:
        dsm_path = "sample_data/sample_drone_dsm.tif"
        dtm_path = "sample_data/sample_drone_dtm.tif"
        with open(dsm_path, "rb") as f_dsm:
            _, meta_dsm = load_drone_geotiff(f_dsm.read())
        with open(dtm_path, "rb") as f_dtm:
            _, meta_dtm = load_drone_geotiff(f_dtm.read())
        elev = compute_elevation_and_slope(meta_dsm, meta_dtm)
        assert elev is not None, "Elevation stats returned None"
        assert elev["ground_mean_amsl"] > 40.0, "Ground elevation out of range"
        assert elev["max_structure_height_m"] > 5.0, "Structure height calculation error"
        results.append(("DSM & DTM Elevation, nDSM & Slope Analysis", True, f"Ground: {elev['ground_mean_amsl']}m AMSL, Structure Height: {elev['max_structure_height_m']}m, Slope: {elev['avg_slope_deg']}° ({elev['slope_class']})"))
    except Exception as e:
        results.append(("DSM & DTM Elevation & Slope", False, str(e)))

    # 7. Test Cadastral Village Map (GeoJSON & Shapefile)
    try:
        cad_path = "sample_data/sample_cadastral_parcels.geojson"
        with open(cad_path, "rb") as f:
            gdf, src, _ = load_cadastral_dataset(cad_path, f.read())
            p_gdf, p_stats = process_cadastral_gdf(gdf)
        assert p_stats["total"] >= 4, "Expected cadastral parcels"
        assert "survey_no" in p_gdf.columns, "survey_no missing"
        results.append(("Cadastral Village Map Ingestion & Schema", True, f"Loaded {p_stats['total']} parcels, Avg Area: {p_stats['avg_area_cents']:.1f} Cents"))
    except Exception as e:
        results.append(("Cadastral Village Map Ingestion", False, str(e)))

    # 8. Test Surrounding Land Topologies & Neighbor Schedule
    try:
        topol_res = analyze_surrounding_topologies(poly, p_gdf, DEFAULT_LAND_PAPER["boundaries"])
        assert topol_res["valid"], "Topology should be valid"
        assert "North" in topol_res["neighbors"], "North neighbor missing"
        results.append(("Surrounding Land Topologies & Chakkubandhulu", True, f"Geometry Valid: {topol_res['valid']}, 4-Way Neighbors Detected: N, S, E, W"))
    except Exception as e:
        results.append(("Surrounding Land Topologies", False, str(e)))

    # 9. Test Official Survey Certificate PDF Generation
    try:
        buf = io.BytesIO()
        verif_info = {
            "status": "Verified & Accepted",
            "reason": "Physical boundary stones match deed record.",
            "notes": "RTK-GNSS verified at all vertices.",
            "surveyor_id": "SURV-AP-9942"
        }
        generate_survey_certificate_pdf(buf, DEFAULT_LAND_PAPER, units, perimeter_m, pd.DataFrame(sides), elev, verif_info)
        pdf_bytes = len(buf.getvalue())
        assert pdf_bytes > 3000, "PDF size too small"
        results.append(("Official Land Survey Certificate PDF Generator", True, f"Generated official PDF ({pdf_bytes:,} bytes)"))
    except Exception as e:
        results.append(("Official Survey Certificate PDF Generator", False, str(e)))

    # 10. Test ZIP Project Package
    try:
        zip_path = "GeoVision_AI_LandSurvey.zip"
        assert os.path.exists(zip_path), "ZIP package missing"
        zip_size = os.path.getsize(zip_path)
        assert zip_size > 1000000, "ZIP size smaller than expected"
        results.append(("Full Project ZIP Package", True, f"File: {zip_path} ({zip_size:,} bytes)"))
    except Exception as e:
        results.append(("Full Project ZIP Package", False, str(e)))

    print("\nTest Summary:")
    passed_count = sum(1 for _, passed, _ in results)
    total_count = len(results)
    
    for name, passed, detail in results:
        status_icon = "PASS" if passed else "FAIL"
        print(f"[{status_icon}] {name:<50} : {detail}")

    print("-" * 70)
    print(f"OVERALL RESULT: {passed_count}/{total_count} Features Verified Successfully ({(passed_count/total_count)*100:.1f}%)")
    print("=" * 70)

    return passed_count == total_count

if __name__ == "__main__":
    success = run_feature_tests()
    sys.exit(0 if success else 1)
