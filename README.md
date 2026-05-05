# Project Restorasi Citra (Image Restoration)

**Nama:** Ilan Hawwari Prasojo  
**NRP:** 5024241039 

---

## Pipeline Restorasi

Pada program ini, proses restorasi citra dilakukan per *channel* warna (B, G, R) menggunakan urutan (pipeline) pemrosesan spasial sebagai berikut:

1. **Median Filter (Kernel 5x5):**
   * **Alasan:** Median filter sangat efektif untuk menghilangkan *impulse noise* atau *salt-and-pepper noise* tanpa banyak merusak tepi (edges) pada gambar. Kernel 5x5 dipilih untuk menangani intensitas noise awal yang cukup besar.
2. **Mean Filter (Kernel 5x5):**
   * **Alasan:** Digunakan untuk meratakan dan menghaluskan (*smoothing*) sisa-sisa noise yang mungkin tidak tertangani oleh median filter, seperti variansi *Gaussian noise*.
3. **Mean Filter (Kernel 3x3):**
   * **Alasan:** Diterapkan lagi dengan kernel yang lebih kecil untuk menghaluskan citra secara lebih detail setelah penghalusan kasar di tahap sebelumnya.
4. **Gaussian Smoothing (Kernel 3x3, Sigma 1):**
   * **Alasan:** Memberikan efek *blur* yang lebih natural dan terdistribusi normal dibandingkan *mean filter*. Ini berfungsi sebagai *base image* untuk tahap penajaman.
5. **Sharpening (Unsharp Masking):**
   * **Alasan:** Karena proses *filtering* (Median dan Mean) di tahap 1-4 menyebabkan gambar menjadi kabur (*blur*) dan kehilangan detail, tahap *sharpening* digunakan. Teknik yang digunakan mirip dengan *unsharp masking*, di mana detail gambar didapatkan dari selisih citra awal dengan citra yang di-*blur* (Gaussian), lalu ditambahkan kembali ke citra dengan faktor penguatan (*gain* = 1.8) untuk mempertegas tepi/detail.

---
**Hasil Visualisasi Sebelum dan Sesudah:**

Sebelum:
<img width="512" height="512" alt="lena_noisy" src="https://github.com/user-attachments/assets/8f9011b5-a2c8-498b-ad2b-3765542a5e2c" />

Sesudah:
<img width="512" height="512" alt="lena_restored" src="https://github.com/user-attachments/assets/abf48aea-257e-44a0-b6b8-f1495bc6b975" />

**Hasil Visualisasi dengan Histogram:**
<img width="855" height="713" alt="Figure 2026-05-05 230050" src="https://github.com/user-attachments/assets/3c33476c-ecd6-4b71-a7ca-c7d6e6742d90" />
<img width="1723" height="3441" alt="image" src="https://github.com/user-attachments/assets/8655abe5-78b4-4e6d-83e3-2015749a57f7" />



## Analisis
Pipeline secara keseluruhan berhasil mereduksi noise pada gambar *noisy* awal. Perpaduan antara Median filter di awal sukses membuang noise titik (ekstrem), sementara Sharpening di akhir sukses memunculkan kembali beberapa garis tepi (edge) yang memudar. Perubahan distribusi piksel juga terlihat lebih baik pada grafik histogram, menunjukkan gambar tidak lagi didominasi oleh titik-titik noise.
Penggunaan Mean filter secara berurutan (terutama dengan ukuran kernel 5x5 lalu 3x3) menyebabkan *smoothing* yang terlalu agresif (over-blurring). Hal ini membuat tekstur halus pada gambar asli (seperti detail rambut atau kulit) hilang secara permanen dan tidak bisa sepenuhnya dikembalikan oleh tahap *sharpening*.


---

## Analisis

* Median filter efektif untuk menghilangkan noise impuls (salt and pepper).
* Mean dan Gaussian filter membantu mengurangi noise yang menyebar, namun membuat citra sedikit blur.
* Sharpening membantu mengembalikan detail agar tidak terlalu halus.

Kelebihan:

* Noise berkurang cukup signifikan
* Warna dan bentuk objek tetap terlihat

Kekurangan:

* Beberapa detail halus masih hilang
* Jika filtering terlalu kuat, citra bisa terlihat terlalu halus

---

## Cara Menjalankan

1. Install library yang dibutuhkan:

   * numpy
   * opencv-python
   * matplotlib

2. Pastikan struktur folder seperti berikut:

```
mp1-image-restoration/
├── restoration.py
├── Inputpcv/
│   └── lena_noisy.png
└── Outputpcv/
```

3. Jalankan program:

```
python restoration.py
```

4. Hasil akan:

* Ditampilkan dalam plot
* Disimpan di:

  ```
  Outputpcv/lena_restored.png
  ```

