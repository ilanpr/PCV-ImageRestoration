import numpy as np
import cv2
import matplotlib.pyplot as plt

# --- KUMPULAN FUNGSI FILTER ---

def median_filter(img, ksize=3):
    pad = ksize // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+ksize, j:j+ksize]
            output[i, j] = np.median(window)
    return output

def gaussian_kernel(size=3, sigma=1):
    k = size // 2
    kernel = np.zeros((size, size))
    for x in range(-k, k+1):
        for y in range(-k, k+1):
            kernel[x+k, y+k] = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel = kernel / np.sum(kernel)
    return kernel

def convolution(img, kernel):
    k = kernel.shape[0] // 2
    padded = np.pad(img, k, mode='edge')
    output = np.zeros_like(img, dtype=float)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+2*k+1, j:j+2*k+1]
            output[i, j] = np.sum(window * kernel)
    return output

def sharpening(img):
    kernel = gaussian_kernel(3, 1)
    blurred = convolution(img, kernel)
    sharpened = img + 1.8 * (img - blurred)
    sharpened = np.clip(sharpened, 0, 255)
    return sharpened.astype(np.uint8)

def mean_filter(img, ksize=3):
    pad = ksize // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img, dtype=float)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+ksize, j:j+ksize]
            output[i, j] = np.mean(window)
    return output

# --- FUNGSI BANTUAN ---

def apply_to_image(img, func, *args, **kwargs):
    """Menerapkan filter 2D ke citra berwarna (3 channel)"""
    b, g, r = cv2.split(img)
    b_res = func(b, *args, **kwargs)
    g_res = func(g, *args, **kwargs)
    r_res = func(r, *args, **kwargs)
    return cv2.merge((b_res, g_res, r_res))

def to_uint8(img_array):
    """Memastikan array berada di rentang 0-255 dan bertipe uint8 untuk visualisasi"""
    return np.clip(img_array, 0, 255).astype(np.uint8)

def plot_color_histogram(image, title):
    """Menampilkan histogram warna RGB"""
    colors = ('b', 'g', 'r')
    for i, col in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=col, alpha=0.7)
        plt.xlim([0, 256])
    plt.title(title)
    plt.xlabel('Intensitas Piksel')
    plt.ylabel('Frekuensi')

# --- MAIN ---

if __name__ == "__main__":
    img = cv2.imread("Inputpcv/lena_noisy.png")

    if img is None:
        print("Error: Gambar tidak ditemukan.")
    else:
        print("Memproses tahap 1: Original")
        img_orig = img.copy()

        print("Memproses tahap 2: Median Filter (5x5)")
        img_median = apply_to_image(img_orig, median_filter, 5)

        print("Memproses tahap 3: Mean Filter (5x5)")
        img_mean5 = apply_to_image(img_median, mean_filter, 5)

        print("Memproses tahap 4: Mean Filter (3x3)")
        img_mean3 = apply_to_image(img_mean5, mean_filter, 3)

        print("Memproses tahap 5: Gaussian Smoothing")
        kernel_gauss = gaussian_kernel(3, 1)
        img_smooth = apply_to_image(img_mean3, convolution, kernel_gauss)

        print("Memproses tahap 6: Sharpening (Restored)...")
        img_restored = apply_to_image(to_uint8(img_smooth), sharpening)
        stages = [
            ("1. Original Noisy", img_orig),
            ("2. After Median (5x5)", to_uint8(img_median)),
            ("3. After Mean (5x5)", to_uint8(img_mean5)),
            ("4. After Mean (3x3)", to_uint8(img_mean3)),
            ("5. After Gaussian Smoothing", to_uint8(img_smooth)),
            ("6. Final Restored", img_restored)
        ]
        plt.figure(figsize=(14, 24))

        for i, (title, image) in enumerate(stages):
            #Tampilan Gambar
            plt.subplot(len(stages), 2, 2 * i + 1)
            plt.title(title, fontsize=12, fontweight='bold')
            plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            plt.axis('off')

            #Tampilan Histogram
            plt.subplot(len(stages), 2, 2 * i + 2)
            plot_color_histogram(image, f"Histogram: {title}")

        plt.tight_layout()
        plt.show()
