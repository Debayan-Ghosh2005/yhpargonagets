# Least Significant Bit (LSB) Steganography

## 1. What is LSB and How Does It Work?

In digital images (especially in 24-bit or 8-bit bitmap images), each pixel is represented by a combination of red, green, and blue color channels. Each of these channels typically uses 8 bits (1 byte), representing values from 0 to 255.

The **Least Significant Bit** is the bit in a byte that contributes the smallest amount to the total value. For example, in the byte `10010110`, the LSB is the rightmost `0`. Changing the LSB causes only a minor change in the value — for instance, from 150 to 151 — which is usually imperceptible to the human eye.

### LSB Image Steganography Process:

* A binary representation of the secret message is created.
* Each bit of this message is sequentially embedded into the LSB of the image pixels.

**Example:**

* Original pixel value (Red channel): `10010110` → 150
* Secret bit: `1`
* Modified pixel value: `10010111` → 151

The image looks almost identical visually, but it now carries part of the hidden message.

## 2. Origins and Discovery

The concept of steganography is ancient — used in Greek and Roman times — but the digital LSB method became practical with the rise of personal computing and bitmap image formats.

Although no single person is credited with "inventing" LSB steganography, it started appearing in technical discussions and experimentation in the early 1990s, when digital image formats became widely accessible.

The first academic-style reference to LSB steganography can be traced to the 1994 paper by Tierney and Johnson et al., but even earlier, Christian Cachin (1998) provided a solid information-theoretic analysis.

The JPEG format presented more challenges for LSB embedding due to compression, which is why early LSB methods were focused mostly on **BMP** and **TIFF** formats (uncompressed).

The technique gained popularity through **steganalysis research** in the early 2000s.

> ✉️ **Note**: While this historical data is based on factual records and papers, the explanation here is original and not copied from academic literature.

## 3. Practical Example with Real Data

Let’s consider an example of hiding the message **"Hi"** inside a grayscale image.

* Message: `"Hi"` → ASCII → `01001000 01101001`
* Each pixel of a grayscale image is 8 bits. We take 16 pixels and replace their LSBs:

```
Pixel[0] value: 11011010 → embed 0 → 11011010
Pixel[1] value: 10110111 → embed 1 → 10110111
...
```

After embedding, the visual difference in the image is negligible, but the binary payload now contains "Hi".

In actual implementation (e.g., Python using Pillow), the modified image remains visually identical. However, if you extract every LSB of the pixel sequence, you recover the original message.

## 4. Limitations and Detection

While LSB is simple, it is also vulnerable to:

* **Compression** (e.g., JPEG), which destroys LSB data
* **Steganalysis tools**, which detect statistical anomalies
* **Histogram analysis**, which reveals unnatural patterns

To counter this, more advanced techniques like **LSB matching**, **adaptive LSB**, or **transform-domain methods** (e.g., **DCT**, **DWT**) are used.

## 5. Code Overview

### 🔴 `encode_red_channel()` → *Hides a secret message*

* Converts the text `"my name is debayan"` to binary.
* Opens an image (`apple.png`) and edits **only the red channel** of each pixel.
* It replaces the **Least Significant Bit (LSB)** of red with each bit of your message.
* Adds a **null character (`\0`)** at the end to mark where the message stops.
* Saves the result to `basic_encoded.png`.

**✅ Output**: Image looks the same but secretly contains the message in the red channel.

### 🔵 `decode_red_channel()` → *Extracts the hidden message*

* Opens the previously saved `basic_encoded.png`.
* Collects the **LSB of the red channel** of each pixel in order.
* Groups every 8 bits into a character.
* Stops reading when it sees a null byte (`00000000`).
* Reconstructs and prints the hidden message.

**✅ Output**: `"my name is debayan"`

---

## 6. References (Used for Context, Not Copied)

* Johnson, N. F., & Jajodia, S. (1998). *Exploring Steganography: Seeing the Unseen*.
* Cachin, C. (1998). *An Information-Theoretic Model for Steganography*.
* Provos, N., & Honeyman, P. (2003). *Hide and Seek: An Introduction to Steganography*.
* Real malware case: *Duqu Analysis by Symantec Labs, 2011*
