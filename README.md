# TopoStitcher
A Python and Bash utility script to fix, stitch, and convert KML/KMZ SuperOverlay (Image Pyramid) files into a single, high-resolution, and color-accurate GeoTIFF for QGIS and other GIS software.

## 📌 ปัญหาที่สคริปต์นี้เข้ามาช่วยแก้ (The Problem)
เมื่อนำไฟล์แผนที่แบบ KML SuperOverlay (ที่มีการซอยภาพเป็น L1 - L5) ไปเปิดใน QGIS มักจะพบปัญหา:
1. **ภาพแตก/เบลอ:** โปรแกรมอ่านเฉพาะภาพ L1 (Thumbnail) มาขยายคลุมพื้นที่ทั้งหมด
2. **สีเพี้ยน (Palette Color Issue):** โปรแกรมพยายามต่อภาพ Palette Color (Indexed) เข้าด้วยกัน ทำให้ตารางสีตีกันจนเกิดเป็นตารางหมากรุกสีเพี้ยน
3. **ขอบแหว่ง:** ภาพระดับ L5 ไม่ครอบคลุมเต็มพื้นที่ ทำให้ขอบแผนที่ขาดหาย

สคริปต์นี้จะข้ามข้อจำกัดของโปรแกรม โดยการดึงพิกัด (Bounding Box) สั่งแปลงสีเป็น RGB 3 แบนด์ (True Color) และต่อภาพทุก Level (L1-L5) เข้าด้วยกันแบบไร้รอยต่อ พร้อมสร้าง Overviews (Pyramid) เพื่อให้ซูมแผนที่ขนาดใหญ่ได้อย่างลื่นไหล

---

## 📂 โครงสร้างโปรเจกต์ (Project Structure)

ก่อนรันสคริปต์ โฟลเดอร์ที่แตกไฟล์ KMZ ออกมาควรมีโครงสร้างดังนี้:

```text
📦 your-kmz-extracted-folder/
 ┣ 📜 doc.kml                # ไฟล์ KML แกนหลักที่เก็บพิกัด
 ┣ 📜 stitch.py              # 1️⃣ สคริปต์ Python สำหรับรันตัวแรก
 ┣ 🖼️ _L1_0_0.png            # ไฟล์ภาพย่อยระดับ L1
 ┣ 🖼️ _L2_0_0.png            # ไฟล์ภาพย่อยระดับ L2
 ┣ 🖼️ ...
 ┗ 🖼️ _L5_x_y.png            # ไฟล์ภาพย่อยระดับ L5 (ความละเอียดสูงสุด)
```

## หลังรันสคริปต์เสร็จสิ้น ระบบจะสร้างไฟล์ใหม่ดังนี้
```text
┣ 📜 file_list.txt          # รายชื่อไฟล์สำหรับจัดลำดับ VRT
 ┣ 📜 run_convert.sh         # 2️⃣ Bash script ที่ถูกสร้างขึ้นอัตโนมัติ
 ┣ 📜 merged.vrt             # ไฟล์ Virtual Raster ที่ประกอบร่างภาพทั้งหมด
 ┣ 🖼️ _L1_0_0.tif            # ไฟล์ TIF ที่ถูกฝังพิกัดและแปลงเป็น RGB
 ┣ 🖼️ ...
 ┗ 🗺️ Final_Topomap_Full.tif # ✅ ไฟล์ผลลัพธ์สุดท้าย (นำไฟล์นี้ไปใช้งาน)
```

## ⚙️ สิ่งที่ต้องเตรียม (Prerequisites)
เครื่องคอมพิวเตอร์ของคุณต้องติดตั้งเครื่องมือต่อไปนี้:
 - Python 3
 - GDAL (สำหรับผู้ใช้ macOS แนะนำให้ติดตั้งผ่าน Homebrew: brew install gdal)

## 🚀 วิธีใช้งาน (Usage)
1. เตรียมไฟล์
เปลี่ยนนามสกุลไฟล์แผนที่ของคุณจาก .kmz เป็น .zip แล้วทำการแตกไฟล์ (Extract) ออกมาเป็นโฟลเดอร์ นำไฟล์ stitch.py เข้าไปวางไว้ในโฟลเดอร์เดียวกับ doc.kml

2. รัน Python Script
เปิด Terminal ชี้ Path เข้าไปที่โฟลเดอร์นั้น แล้วรันคำสั่ง:
```bash
python3 stitch.py
```
สคริปต์จะทำการวิเคราะห์ไฟล์ doc.kml กวาดหาภาพย่อยทั้งหมด และสร้างไฟล์ run_convert.sh พร้อมคำสั่งแปลงพิกัดและสี

3. ประมวลผลและสร้าง GeoTIFF
รัน Bash Script ที่เพิ่งได้มาด้วยคำสั่ง:
```bash
sh run_convert.sh
```
ระบบจะรันกระบวนการ 4 ขั้นตอน:
 - ฝังพิกัดและแปลง Palette Color เป็น RGB ในทุกไฟล์ภาพ
 - สร้าง Virtual Raster (VRT) เรียงลำดับจากภาพ L1 (ล่างสุด) ซ้อนทับจนถึง L5 (บนสุด)
 - ส่งออกภาพเป็นไฟล์ GeoTIFF แผ่นเดียว
 - สร้าง Overviews (Pyramid) เพื่อการเรนเดอร์ที่รวดเร็วในโปรแกรม GIS

 4. นำไปใช้งาน
เมื่อ Terminal แจ้งเตือนว่า Done! The comprehensive map is ready. คุณจะได้ไฟล์ชื่อ Final_Topomap_Full.tif สามารถลากไฟล์นี้เข้าไปใช้ใน QGIS หรืออัปโหลดขึ้น Cloud Server ได้ทันทีแบบไร้ปัญหาภาพแตกหรือสีเพี้ยน

## 🛠️ เครื่องมือที่ใช้ (Built With)
 - Python 3 - ตัวจัดการ Regex และสร้าง Automated Script
 - GDAL (Geospatial Data Abstraction Library) - เอนจินหลักในการแปลงพิกัด จัดการ Raster และต่อภาพ (gdal_translate, gdalbuildvrt, gdaladdo)