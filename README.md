# Image Restoration
## Deskripsi

Pada tugas ini dilakukan proses restorasi citra Lena yang telah mengalami beberapa kerusakan seperti:

* Low contrast (kontras rendah)
* Gaussian noise
* Salt and pepper noise
* Blur

Tujuan dari program ini adalah memperbaiki kualitas citra agar mendekati kondisi yang lebih baik dan lebih jelas.

## Pipeline Restorasi

Proses restorasi dilakukan secara bertahap pada setiap channel warna (B, G, R). Teknik yang digunakan adalah sebagai berikut:

1. Median Filter
   Digunakan untuk menghilangkan noise tipe salt and pepper. Filter ini bekerja dengan mengambil nilai median dari lingkungan sekitar pixel.

2. Mean Filter
   Digunakan untuk menghaluskan noise yang lebih menyebar (seperti gaussian noise). Dilakukan dua kali untuk hasil yang lebih bersih.

3. Gaussian Filter (Manual Convolution)
   Digunakan untuk smoothing tambahan agar noise semakin berkurang dan hasil lebih natural.

4. Sharpening (Unsharp Masking)
   Digunakan untuk mengembalikan detail yang hilang akibat proses smoothing sebelumnya.
---

## Hasil

Program akan menampilkan perbandingan antara:

* Citra sebelum restorasi
* Citra setelah restorasi

Hasil akhir juga akan disimpan pada folder output.

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

