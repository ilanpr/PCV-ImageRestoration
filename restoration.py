import numpy as np
import cv2
import matplotlib.pyplot as plt

# Median Filter
def median_filter(img, ksize=3):
    pad = ksize // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+ksize, j:j+ksize]
            output[i, j] = np.median(window)

    return output

# Gaussian
def gaussian_kernel(size=3, sigma=1):
    k = size // 2
    kernel = np.zeros((size, size))

    for x in range(-k, k+1):
        for y in range(-k, k+1):
            kernel[x+k, y+k] = np.exp(-(x**2 + y**2) / (2 * sigma**2))

    kernel = kernel / np.sum(kernel)
    return kernel

# Convolution
def convolution(img, kernel):
    k = kernel.shape[0] // 2
    padded = np.pad(img, k, mode='edge')
    output = np.zeros_like(img, dtype=float)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+2*k+1, j:j+2*k+1]
            output[i, j] = np.sum(window * kernel)

    return output

# Histogram Equalization
def histogram_equalization(img):
    hist = np.zeros(256)

    # hitung histogram
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hist[img[i, j]] += 1

    pdf = hist / np.sum(hist)
    cdf = np.cumsum(pdf)

    output = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            output[i, j] = int(cdf[img[i, j]] * 255)

    return output



# Sharpening
def sharpening(img):
    kernel = gaussian_kernel(3, 1)
    blurred = convolution(img, kernel)

    sharpened = img + 1.8 * (img - blurred)

    sharpened = np.clip(sharpened, 0, 255)
    return sharpened.astype(np.uint8)

# Mean
def mean_filter(img, ksize=3):
    pad = ksize // 2
    padded = np.pad(img, pad, mode='edge')
    output = np.zeros_like(img, dtype=float)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            window = padded[i:i+ksize, j:j+ksize]
            output[i, j] = np.mean(window)

    return output

# Pipeline
def process_channel(channel):
    median = median_filter(channel, 5)
    mean = mean_filter(median, 5)
    mean = mean_filter(mean, 3)
    kernel = gaussian_kernel(3, 1)
    smooth = convolution(mean, kernel)
    result = sharpening(smooth.astype(np.uint8))

    return result

# MAIN
if __name__ == "__main__":
    img = cv2.imread("Inputpcv/lena_noisy.png")

    # split channel (BGR)
    b, g, r = cv2.split(img)

    # proses tiap channel
    b = process_channel(b)
    g = process_channel(g)
    r = process_channel(r)

    # gabungkan kembali
    result = cv2.merge((b, g, r))

    # simpan hasil
    cv2.imwrite("Outputpcv/lena_restored.png", result)

    # tampilkan
    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    plt.subplot(1,2,2)
    plt.title("Restored")
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

    plt.show()
