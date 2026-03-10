# Interpolation Calculator

A graphical calculator that solves **Lagrange Interpolation** and **Newton's Divided Difference** problems with full step-by-step solutions

Built with Python and Tkinter. No external GUI frameworks required.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey)

---

## Features

- **Lagrange Interpolation** — basis polynomials, polynomial expansion, and evaluation
- **Newton's Divided Difference** — divided difference table, detailed calculations, and evaluation
- **Side-by-side results** with both methods displayed simultaneously
- **Step-by-step solutions** that mirror the manual calculation process:
  - Step 1: Compute basis polynomials / divided difference table
  - Step 2: Build the interpolating polynomial (with full algebraic expansion)
  - Step 3: Evaluate at a given point
- **Cross-verification** — confirms both methods produce the same result
- **Interactive graph** (matplotlib) showing the polynomial curve, data points, and evaluated point
- **Preloaded examples** to get started immediately
- Hover-to-scroll on result panels
- Clean, modern UI with color-coded output

### Prerequisites

- Python 3.10 or higher
- `tkinter` (included with most Python installations)

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Interpolation-Calculator.git
cd Interpolation-Calculator

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# Install dependencies
pip install numpy matplotlib
```

---

## Usage

```bash
# Run as a package
python -m Interpolation

# Or run directly
python Interpolation/__main__.py
```

### Quick Start

1. Launch the app
2. Enter your data points (x, f(x)) or click **Example 1** / **Example 2**
3. Enter the x-value to evaluate at
4. Click **Compute**
5. View the step-by-step solutions for both methods side by side
6. Click **Show Graph** to visualize the interpolating polynomial

## Examples

### Example 1 — Paper Problem 3

| x   | f(x) |
|-----|------|
| 1   | 2.3  |
| 3   | 4.2  |
| 4   | 3.3  |

Evaluate at **x = 2.5** → **P(2.5) = 4.1875**

### Example 2

| x   | f(x) |
|-----|------|
| 1   | 2.5  |
| 3   | 5.7  |
| 6   | 4.1  |

Evaluate at **x = 2.5** → Both methods agree.

---

## How It Works

### Lagrange Interpolation

Given data points $(x_0, y_0), (x_1, y_1), \ldots, (x_n, y_n)$, the interpolating polynomial is:

$$P(x) = \sum_{i=0}^{n} f(x_i) \cdot L_i(x)$$

where each basis polynomial is:

$$L_i(x) = \prod_{\substack{j=0 \\ j \neq i}}^{n} \frac{x - x_j}{x_i - x_j}$$

### Newton's Divided Difference

Using the same data points, the interpolating polynomial is:

$$P(x) = f[x_0] + f[x_0, x_1](x - x_0) + f[x_0, x_1, x_2](x - x_0)(x - x_1) + \cdots$$

where divided differences are computed recursively:

$$f[x_i, \ldots, x_{i+k}] = \frac{f[x_{i+1}, \ldots, x_{i+k}] - f[x_i, \ldots, x_{i+k-1}]}{x_{i+k} - x_i}$$

Both methods produce the **same** polynomial — the app verifies this automatically.
