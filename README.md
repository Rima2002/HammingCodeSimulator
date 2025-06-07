# Hamming SEC-DED Code Simulator

## 📌 Project Overview

This project is a simulator for the Hamming SEC-DED (Single Error Correction, Double Error Detection) algorithm. It supports 8, 16, and 32-bit data, enabling error detection and correction through a user-friendly graphical interface.

> Developed as a term project for **BLM230 - Computer Architecture**  
> 🧑‍🎓 **Student**: Rima Farah Eleuch  
> 🆔 **Student Number**: 21360859216

---

## 🚀 Features

| Feature                       | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| Data Size Selection          | Choose between 8, 16, or 32-bit input.                                      |
| Hamming Code Calculation     | Computes parity bits following SEC-DED rules.                               |
| Memory Operations            | Encoded data can be saved to and loaded from memory.                        |
| Error Injection              | Insert single or double bit errors at specified positions.                  |
| Error Detection & Correction | Uses syndrome analysis to detect and optionally correct single-bit errors. |
| Bit Visualization            | Displays bits visually with color indicators.                               |
| Help Menu                    | Contains usage guide and information about the program.                     |

---

## 🛠️ Technologies Used

- Python 3
- Tkinter (for GUI)
- GitHub (code repository)
- YouTube (demo video)

---

## 📋 Usage Instructions

1. **Select Data Size**  
   Choose 8, 16, or 32-bit input from the "Data Size" dropdown on program start.

2. **Enter Binary Data**  
   Input your binary data (only 0s and 1s) based on the selected size.

3. **Generate Hamming Code**  
   Click on “Compute Hamming Code” to generate encoded data.

4. **Save Encoded Data**  
   Store the encoded data to memory for later use.

5. **Read From Memory**  
   Retrieve previously saved encoded data.

6. **Inject Error and Analyze**  
   - Select error type: “Single Bit” or “Double Bit”
   - Enter error positions
   - Click “Inject Error”

   - **Single Bit**: Automatically detected and corrected  
   - **Double Bit**: Detected (but not correctable)

---

## ⚙️ Technical Details

- **Parity Bits**: Located at positions 2^n
- **Overall Parity**: Added at the end as XOR of all bits
- **Syndrome**: Determines error position from parity checks
- **Double Error Detection**: Detected through overall parity and syndrome, but cannot be corrected

---

## 🧱 Code Structure

The main logic resides in the `HammingCodeSimulator` class:

- `encode_data`: Encodes binary input with SEC-DED logic
- `introduce_error`: Adds errors to data
- `detect_and_correct_error`: Detects and corrects errors via syndrome
- `visualize_bits`: Displays bits with color formatting

---

## 🎓 Conclusion

This simulator demonstrates the principles of Hamming SEC-DED coding both theoretically and practically. With its intuitive interface and visual tools, it is a great aid for learning about error correction in digital systems.

---

## 🔗 Resources

- **GitHub (Source Code)**:  
  👉 [Hamming Simulator Repository](https://github.com/kullaniciadi/hamming-simulator)

- **YouTube Demo**:  
  🎥 [Watch Demo](https://youtube.com/watch?v=demo_link)

 
- **GitHub (Source Code)**:  
  👉 [Hamming Simulator Repository](https://github.com/kullaniciadi/hamming-simulator)

- **YouTube Demo**:  
  🎥 [Watch Demo](https://youtube.com/watch?v=demo_link)
