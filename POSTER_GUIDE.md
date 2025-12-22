# 📊 Panduan Academic Poster

## File: `academic_poster.html`

Academic poster profesional untuk Final Project dengan ukuran **4608 x 2304 pixels** (landscape, ratio 2:1).

---

## 🎨 Fitur Poster

### **Konten Utama:**
1. ✅ **Introduction** - Challenges & Contributions
2. ✅ **Dataset** - MS COCO overview & statistics
3. ✅ **Methodology** - System architecture & components
4. ✅ **Results Analysis** - Metrics, charts, dan findings

### **Desain:**
- 🎨 Modern gradient background (Purple-Indigo)
- 📐 3-column layout untuk readability
- 📊 Visual charts dan metrics cards
- 🎯 Color-coded sections
- ✨ Smooth animations
- 🖨️ Print-ready

---

## 🚀 Cara Menggunakan

### **1. Buka File**
```bash
# Double-click file atau
start academic_poster.html

# Atau buka di browser favorit
chrome academic_poster.html
firefox academic_poster.html
```

### **2. Edit Konten**
Buka file dengan text editor dan edit bagian-bagian ini:

#### **Header - Ganti Info Anda:**
```html
<!-- Line ~165 -->
<div class="text-right">
    <div class="bg-gradient-to-br from-purple-600 to-indigo-600 text-white px-12 py-8 rounded-2xl">
        <p class="text-[36px] font-bold">Final Project</p>
        <p class="text-[32px] mt-2">Image Retrieval</p>
        <p class="text-[28px] mt-4 opacity-90">2025</p>
    </div>
</div>
```

#### **Footer - Ganti Contact Info:**
```html
<!-- Line ~450 -->
<div class="text-[32px] text-gray-700">
    <span class="font-bold">Contact:</span> [Your Name] | [Your Email] | [University]
</div>
```

### **3. Export ke PDF/Image**

#### **Opsi A: Print to PDF (Recommended)**
1. Buka poster di browser
2. Tekan `Ctrl + P` (Windows) atau `Cmd + P` (Mac)
3. Pilih "Save as PDF"
4. Settings:
   - Paper size: Custom (4608 x 2304 px)
   - Margins: None
   - Background graphics: ON
5. Save!

#### **Opsi B: Screenshot (High Quality)**
1. Buka di browser dengan zoom 100%
2. Gunakan tool screenshot:
   - **Windows**: Snipping Tool / Snip & Sketch
   - **Mac**: Cmd + Shift + 4
   - **Browser Extension**: Full Page Screen Capture

#### **Opsi C: Export via Browser DevTools**
1. Buka DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Set dimensions: 4608 x 2304
4. Capture screenshot

---

## 🎨 Kustomisasi Warna

### **Ganti Gradient Background:**
```css
/* Line ~12 */
.poster-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    /* Ganti dengan warna favorit Anda */
}
```

### **Contoh Alternatif:**
```css
/* Blue-Teal */
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);

/* Orange-Pink */
background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);

/* Green-Blue */
background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
```

---

## 📝 Tips Presentasi

### **Untuk Cetak Fisik:**
1. Export ke PDF dengan quality tinggi
2. Print di percetakan dengan spesifikasi:
   - Size: 4608 x 2304 px (atau 48" x 24")
   - Resolution: 150 DPI minimum
   - Material: Art paper / Photo paper
   - Finish: Matte atau Glossy

### **Untuk Presentasi Digital:**
1. Export ke PDF
2. Atau tampilkan langsung di browser (fullscreen: F11)
3. Bisa juga convert ke PowerPoint slide

### **Untuk Submit Online:**
1. Export ke PDF (file size kecil)
2. Atau screenshot ke PNG/JPG (compress jika perlu)

---

## 🔧 Troubleshooting

### **Poster tidak muncul dengan benar:**
- Pastikan koneksi internet aktif (untuk load Tailwind CDN & Google Fonts)
- Refresh browser (Ctrl + F5)
- Coba browser lain (Chrome recommended)

### **Print tidak sesuai ukuran:**
- Set custom paper size di print dialog
- Disable margins
- Enable background graphics
- Gunakan "Save as PDF" bukan print langsung

### **Font tidak muncul:**
- Pastikan koneksi internet aktif
- Google Fonts: Inter harus ter-load
- Fallback: akan gunakan system font

---

## 📊 Struktur Konten

### **Column 1 (Kiri):**
- Introduction (Challenges & Contributions)
- Dataset (Statistics & Overview)

### **Column 2 (Tengah):**
- Methodology (Architecture diagram)
- Key Components (CLIP, FAISS, LLM, SD)

### **Column 3 (Kanan):**
- Results Analysis
  - Retrieval Performance (Bar charts)
  - Generation Quality (Metrics)
  - Scenario Comparison
  - Key Findings

---

## 🎯 Checklist Sebelum Submit

- [ ] Ganti nama & contact info di footer
- [ ] Cek semua angka/metrics sudah benar
- [ ] Test print preview (Ctrl + P)
- [ ] Cek readability dari jarak 1-2 meter
- [ ] Export ke PDF dengan quality tinggi
- [ ] Backup file HTML original

---

## 💡 Pro Tips

1. **Font Size**: Sudah dioptimalkan untuk dibaca dari jarak 1-2 meter
2. **Color Contrast**: High contrast untuk readability
3. **White Space**: Cukup breathing room, tidak terlalu padat
4. **Visual Hierarchy**: Title > Subtitle > Body text jelas
5. **Data Visualization**: Charts lebih mudah dipahami daripada tabel

---

## 📸 Preview

Poster ini akan terlihat seperti:
- **Header**: Judul besar dengan gradient text
- **3 Kolom**: Layout seimbang
- **Visual Elements**: Charts, metrics cards, architecture diagram
- **Footer**: Contact info & date
- **Background**: Gradient purple dengan decorative circles

---

**File siap digunakan!** 🎉

Tinggal edit info personal Anda, lalu export ke PDF untuk presentasi atau cetak.
