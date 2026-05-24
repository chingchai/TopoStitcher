import re
import os

with open("doc.kml", 'r', encoding='utf-8') as f:
    data = f.read()

# ดึง GroundOverlay ทั้งหมด (L1 ถึง L5)
overlays = re.findall(r'<GroundOverlay.*?</GroundOverlay>', data, re.DOTALL | re.IGNORECASE)

commands = []
tif_list = []

for overlay in overlays:
    href_match = re.search(r'<href>\s*(.*?)\s*</href>', overlay, re.IGNORECASE)
    if not href_match:
        continue
        
    href = href_match.group(1)
    n = re.search(r'<north>\s*(.*?)\s*</north>', overlay, re.IGNORECASE).group(1)
    s = re.search(r'<south>\s*(.*?)\s*</south>', overlay, re.IGNORECASE).group(1)
    e = re.search(r'<east>\s*(.*?)\s*</east>', overlay, re.IGNORECASE).group(1)
    w = re.search(r'<west>\s*(.*?)\s*</west>', overlay, re.IGNORECASE).group(1)
    
    out_tif = href.replace('.png', '.tif')
    tif_list.append(out_tif)
    
    # แปลง Palette เป็น RGB ในทุกๆ Level (L1-L5) พร้อมฝังพิกัด
    cmd = f'gdal_translate -q -expand rgb -a_ullr {w} {n} {e} {s} -a_srs EPSG:4326 "{href}" "{out_tif}"'
    commands.append(cmd)

# สร้างไฟล์ List เพื่อให้ gdalbuildvrt อ่านตามลำดับ
with open("file_list.txt", "w") as f:
    for t in tif_list:
        f.write(f"{t}\n")

# สร้าง Shell Script สำหรับรันคำสั่งรวดเดียว
with open("run_convert.sh", "w") as f:
    f.write("#!/bin/bash\n")
    f.write("echo '1/4: Expanding Palette and stamping coordinates (L1 to L5)...'\n")
    for c in commands:
        f.write(c + "\n")
    f.write("echo '2/4: Building Virtual Raster (VRT)...'\n")
    f.write("gdalbuildvrt -resolution highest -input_file_list file_list.txt merged.vrt\n")
    f.write("echo '3/4: Exporting final Topomap...'\n")
    f.write("gdal_translate -of GTiff -co COMPRESS=DEFLATE -co TILED=YES merged.vrt Final_Topomap_Full.tif\n")
    f.write("echo '4/4: Building Overviews for smooth zooming in QGIS...'\n")
    f.write("gdaladdo -r average Final_Topomap_Full.tif 2 4 8 16 32\n")
    f.write("echo 'Done! The comprehensive map is ready.'\n")

print(f"Found {len(tif_list)} tiles in total. 'run_convert.sh' generated!")