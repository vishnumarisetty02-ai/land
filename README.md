# 🌍 GeoVision AI · Drone Land Survey & Cadastral Mapping Suite

**AI-Powered Drone Land Surveying · Patta / Deed Document Verification · DSM & DTM Topography · FMB Cadastral Mapping · Surrounding Topologies · Field Verification (Accept / Reject)**

GeoVision AI is a comprehensive, production-grade GIS & Drone Land Surveying application tailored for licensed surveyors, revenue officers, urban local bodies (ULBs), and land owners.

---

## 🚀 Key Modules & Capabilities

### 1. 📄 User Land Papers & Deed Registration (పట్టా / దస్తావేజు వివరాలు)
- Input official legal land title documents:
  - **Survey / Sub-Division Number** (e.g. `Sy. No. 142/2A`)
  - **Patta Passbook / Document Number** (e.g. `8842`)
  - **Pattadar (Owner Name)**, Father/Husband Name
  - **Village / Gram Panchayat, Mandal / Tehsil, District, State**
  - **Registered Deed Area** (in Cents, Acres, Guntas, Gajalu / Sq.Yards, or m²)
  - **Schedule of Boundaries (చక్కుబందులు / Chakkubandhulu):**
    - ⬆️ North Boundary (e.g. Road / Sy. No. 141)
    - ⬇️ South Boundary (e.g. Sy. No. 142/1)
    - ➡️ East Boundary (e.g. Irrigation Canal / Ayacut)
    - ⬅️ West Boundary (e.g. Sy. No. 143)
  - Document Upload (PDF, JPG, PNG) of Patta copy, Sale Deed, or FMB sketch.

### 2. 📍 Exact Land Location ("భూమి ఎక్కడ ఉంది?")
- Instant GPS Centroid calculation in Decimal Degrees and DMS (Degrees, Minutes, Seconds).
- High-resolution interactive Satellite Map (Esri World Imagery + Google Hybrid).
- Direct link for **Google Maps Navigation** to the land's physical location.

### 3. 🚁 Drone Survey & Metric Measurement (Perimeter & Area)
- Upload Drone Orthomosaic GeoTIFF (`.tif`, `.tiff`).
- Interactive on-map boundary tracing with live polygon editing.
- Automatic projected local **UTM EPSG conversion** for metric accuracy.
- Complete unit breakdown:
  - **Cents** (100 Cents = 1 Acre)
  - **Acres**
  - **Guntas** (40 Guntas = 1 Acre)
  - **Square Yards / Gajalu** (4,840 Sq.Yds = 1 Acre)
  - **Square Meters (m²)** & **Square Feet (sq ft)**
- **Deed vs. Surveyed Area Comparison Matrix:** Computes variance % and flags surplus or deficits.
- **FMB Corner Stone Measurements:** Exact side lengths (P1→P2, P2→P3 in meters and feet) along with 360° compass bearings (e.g., `N 88° 24' E`).

### 4. ⛰️ DSM & DTM Elevation & Topography Analysis
- **DSM (Digital Surface Model):** Captures overall surface elevation including houses, sheds, and trees.
- **DTM (Digital Terrain Model):** Captures bare-earth ground elevation Above Mean Sea Level (AMSL).
- **nDSM (Normalized DSM = DSM - DTM):** Accurately extracts building heights and tree canopies.
- **Slope & Terrain Analysis:** Computes average slope (degrees and %), gradient direction, and suitability for gravity drainage and construction.

### 5. 🗺️ Village Cadastral (FMB) Map Integration
- Overlay official village revenue cadastral maps (Shapefile `.zip`, GeoJSON, KML, GPKG).
- Match Land Paper Survey Numbers with official revenue boundaries.
- Boundary shift and common bund alignment inspection.

### 6. 📐 Surrounding Land Topologies (చుట్టూ ఉన్న భూములు & ఎన్‌క్రోచ్‌మెంట్‌లు)
- Directional Neighbor Identification (North, South, East, West adjoining Survey Numbers & Owners).
- Topological checks:
  - **Self-intersection / Geometry validity:** Ensures clean polygons without bow-ties.
  - **Adjoining Overlaps:** Automatically flags encroachment into neighbor's land with exact overlapping area (m² and Cents).
  - **Sliver gaps & unallocated lands:** Identifies discrepancies with revenue records.
  - **Buffer compliance:** Verifies clearance from road widening setbacks and canal buffer zones.

### 7. ✅ Field Verification Console (Accept & Reject Workflow)
- Dedicated surveyor ground inspection workflow:
  - **✅ ACCEPT & APPROVE SURVEY:** Formally approves survey when physical ground stones match deed.
  - **❌ REJECT SURVEY:** Rejects survey and marks for re-survey with mandatory justification.
  - Standardized ground finding reasons:
    - *Physical boundary stones (Gudikattus) match deed & drone survey exactly*
    - *Boundary stones verified with RTK-GNSS at all corners*
    - *REJECT: Encroachment identified on North/East boundary*
    - *REJECT: Boundary stones missing or moved by neighbor*
    - *REJECT: Possession area deficit exceeds 5% from deed record*
  - Surveyor Name, Registration ID, Field notes, and Corner stone ground photos.
  - Immutable audit trail tracking every approval and rejection.

### 8. 📦 Official Land Survey Certificate (PDF) & GIS Exports
- One-click generation of an **Official Government-Style Land Survey Certificate (PDF)** containing:
  - Complete Land & Pattadar Details
  - Deed vs. Drone Survey Area Table
  - Schedule of Boundaries (Chakkubandhulu)
  - Corner Points & Side Lengths (FMB Table with bearings)
  - DSM/DTM Elevation & Terrain Summary
  - Field Surveyor Verification Sign-off & Seal Block
- Downloadable GIS layers: **GeoJSON**, **Shapefile**, and **CSV coordinates**.

---

## 🏃 Quick Start

Run the application:
```bash
streamlit run app.py
```
Or double-click [`run.bat`](file:///c:/Users/VISHNU/AI/run.bat) on Windows.

Open your browser at: **`http://localhost:8501`**

---

## 🗂️ Sample Datasets Included in `sample_data/`

| File | Description |
| :--- | :--- |
| `sample_drone_orthomosaic.tif` | High-resolution georeferenced aerial orthomosaic |
| `sample_drone_dsm.tif` | Digital Surface Model (Ground + Houses + Trees) |
| `sample_drone_dtm.tif` | Digital Terrain Model (Bare Earth AMSL Elevation) |
| `sample_cadastral_parcels.geojson` | Village Cadastral Map (Sy. Nos 142/1, 142/2A, 142/2B, 143, 144) |
| `sample_cadastral_shapefile.zip` | ESRI Shapefile archive of village survey parcels |
