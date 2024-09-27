# -*- coding: utf-8 -*-
"""PEF_python.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1zCxn63DsG82WoYTm9b5G3Ldz6B-19VWA
"""

import numpy as np
import time

n1 = 400

# exponentially decaying sinusoids with different frequencies
inp = np.zeros(n1, dtype=np.float32)
for j in range(n1 // 15, n1, n1 // 5):
    wave = np.zeros(n1, dtype=np.float32)
    for x in range(j, 399):
        y = (x - j) / 400
        wave[x] = np.exp(-y * 15) * np.sin(y * 0.95 * j)
    inp += wave

res = np.copy(inp)
bak = np.copy(inp)

import matplotlib.pyplot as plt

def stems(data, label, color):
    """
    Plot data using stems (stem plot).
    """
    n1 = len(data)

    # Create a plot with initial zeros
    plt.plot(np.zeros(n1), label=None, color='black')

    # Create a stem plot
    plt.stem(data, label=label, linefmt=color, markerfmt=' ', basefmt=" ")

    # Add legend and formatting
    plt.legend(loc='upper left')
    plt.xlim([0.5, n1 + 0.5])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # Show the plot
    plt.show()

def stems(data, label, color):
    """
    Plot data using stems (stem plot).
    """
    n1 = len(data)

    # Create a plot with initial zeros
    plt.plot(np.zeros(n1), label=None, color='black')

    # Create a stem plot
    # plt.stem(data, label=label, linefmt=color, markerfmt=' ', basefmt=" ", use_line_collection=True)
    plt.stem(data, label=label, linefmt=color, markerfmt=' ', basefmt=" ")

    # Add legend and formatting
    plt.legend(loc='upper left')
    plt.xlim([0.5, n1 + 0.5])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)

    # Show the plot
    plt.show()

plot_input = stems(inp, "input", "blue")

def stream(inv, d, r, na, lambd):
    """
    Streaming PEF algorithm.

    Parameters:
    inv (bool): Direction of streaming, from r to d (True) or d to r (False).
    d (np.ndarray): Input/output data vector.
    r (np.ndarray): Output/input data vector.
    na (int): Number of coefficients.
    lambd (float): Lambda parameter (λ).
    """
    a = np.zeros(na)  # streaming PEF
    dd = da = 0.0  # d (dot) d, d (dot) a

    for ia in range(na):
        if inv:
            d[ia] = r[ia]
        else:
            r[ia] = d[ia]
        dd += d[ia] * d[ia]

    for i1 in range(na, len(d)):
        if inv:  # from r to d
            rn = r[i1] / lambd
            dn = rn * (lambd + dd) - da
            d[i1] = dn
        else:  # from d to r
            dn = d[i1]
            rn = (dn + da) / (lambd + dd)
            r[i1] = lambd * rn

        # update PEF
        for ia in range(na):
            a[ia] -= rn * d[i1 - ia - 1]

        # update dd and da
        dd += dn * dn - d[i1 - na] * d[i1 - na]
        da = dn * a[0]
        for ia in range(1, na):
            da += a[ia] * d[i1 - ia]

# Call the stream function
stream(False, inp, res, 2, 0.1)

# Create the stem plot for the result
plot_decon = stems(res, "decon", "green")

# Call the stream function with inverse set to True
stream(True, bak, res, 2, 0.1)

# Create the stem plot for the inverse result
plot_inverse = stems(bak, "inverse", "purple")

import matplotlib.pyplot as plt

# Create subplots with a layout of 3 rows and 1 column
fig, axs = plt.subplots(3, 1, figsize=(8, 12))  # Adjust figsize as needed

# Plot the input data
# axs[0].stem(inp, linefmt='blue', markerfmt=' ', basefmt=" ", use_line_collection=True)
axs[0].stem(inp, linefmt='blue', markerfmt=' ', basefmt=" ")
axs[0].set_title("Input")
axs[0].set_xlim([0.5, len(inp) + 0.5])
axs[0].legend(["Input"], loc='upper left')
axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[0].spines['left'].set_visible(False)
axs[0].spines['bottom'].set_visible(False)

# Plot the decon data
# axs[1].stem(res, linefmt='green', markerfmt=' ', basefmt=" ", use_line_collection=True)
axs[1].stem(res, linefmt='green', markerfmt=' ', basefmt=" ")
axs[1].set_title("Decon")
axs[1].set_xlim([0.5, len(res) + 0.5])
axs[1].legend(["Decon"], loc='upper left')
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)
axs[1].spines['left'].set_visible(False)
axs[1].spines['bottom'].set_visible(False)

# Plot the inverse data
# axs[2].stem(bak, linefmt='purple', markerfmt=' ', basefmt=" ", use_line_collection=True)
axs[2].stem(bak, linefmt='purple', markerfmt=' ', basefmt=" ")
axs[2].set_title("Inverse")
axs[2].set_xlim([0.5, len(bak) + 0.5])
axs[2].legend(["Inverse"], loc='upper left')
axs[2].spines['top'].set_visible(False)
axs[2].spines['right'].set_visible(False)
axs[2].spines['left'].set_visible(False)
axs[2].spines['bottom'].set_visible(False)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()

plt.savefig("stream.pdf")

plt.savefig("stream.pdf")

"""### Multiple dimensions"""

# Create a deepcopy of inp
inp2 = np.copy(inp)
known = np.ones(n1, dtype=bool)

# Cut holes in the data and create a mask
holes = [55, 153, 246, 301, 376]
for hole in holes:
    inp2[hole:hole + 20] = 0  # Note: Python slicing is exclusive of the end index
    known[hole:hole + 20] = False

def stream_missing(d, k, na, lambd):
    """
    Streaming PEF with missing data handling.

    Parameters:
    d (np.ndarray): Input/output data vector.
    k (np.ndarray): Boolean mask indicating known values.
    na (int): Number of coefficients.
    lambd (float): Lambda parameter (λ).
    """
    a = np.zeros(na)  # streaming PEF
    da = 0.0  # d (dot) a
    dd = 0.0  # d (dot) d

    for ia in range(na):
        dd += d[ia] * d[ia]

    for i1 in range(na, len(d)):
        if k[i1]:  # from d to r
            dn = d[i1]
            rn = (dn + da) / (lambd + dd)
        else:  # assume r=0
            dn = -da
            rn = 0.0
            d[i1] = dn

        # update PEF
        for ia in range(na):
            a[ia] -= rn * d[i1 - ia - 1]

        # update dd and da
        dd += dn * dn - d[i1 - na] * d[i1 - na]
        da = dn * a[0]
        for ia in range(1, na):
            da += a[ia] * d[i1 - ia]

# Create the stem plot for the ideal data
plot_ideal = stems(inp, "ideal", "blue")

# Create the stem plot for the input with holes
plot_hole = stems(inp2, "input", "green")

# Create a deepcopy of inp2
miss = np.copy(inp2)

# Call the stream_missing function
stream_missing(miss, known, 2, 0.05)

# Create the stem plot for the interpolated data
plot_interp = stems(miss, "filled", "purple")

# Create subplots with a layout of 3 rows and 1 column
fig, axs = plt.subplots(3, 1, figsize=(8, 12))  # Adjust figsize as needed

# Plot the ideal data
axs[0].stem(inp, linefmt='blue', markerfmt=' ', basefmt=" ")
axs[0].set_title("Ideal")
axs[0].set_xlim([0.5, len(inp) + 0.5])
axs[0].legend(["Ideal"], loc='upper left')
axs[0].spines['top'].set_visible(False)
axs[0].spines['right'].set_visible(False)
axs[0].spines['left'].set_visible(False)
axs[0].spines['bottom'].set_visible(False)

# Plot the input with holes
axs[1].stem(inp2, linefmt='green', markerfmt=' ', basefmt=" ")
axs[1].set_title("Input with Holes")
axs[1].set_xlim([0.5, len(inp2) + 0.5])
axs[1].legend(["Input"], loc='upper left')
axs[1].spines['top'].set_visible(False)
axs[1].spines['right'].set_visible(False)
axs[1].spines['left'].set_visible(False)
axs[1].spines['bottom'].set_visible(False)

# Plot the interpolated data
axs[2].stem(miss, linefmt='purple', markerfmt=' ', basefmt=" ")
axs[2].set_title("Filled")
axs[2].set_xlim([0.5, len(miss) + 0.5])
axs[2].legend(["Filled"], loc='upper left')
axs[2].spines['top'].set_visible(False)
axs[2].spines['right'].set_visible(False)
axs[2].spines['left'].set_visible(False)
axs[2].spines['bottom'].set_visible(False)

f = plt.figure()

# Adjust layout
# plt.tight_layout()

# plt.show()

# Save the figure to a PDF file
# plt.savefig("stream.pdf")
# f.savefig("foo.pdf", bbox_inches='tight')

# Optionally, you can also show the plot
# plt.show()

import zipfile

import requests
import os

# Download data from a public server
url = "https://zenodo.org/api/records/11099632/files-archive"
response = requests.get(url)
with open("files.zip", "wb") as file:
    file.write(response.content)

# Unzip the archive file
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    zip_ref.extractall("extracted_folder")  # Specify the directory to extract to

# Create a dictionary for easy access to files
patterns = {}

# Open the ZIP file and populate the dictionary
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    for file_info in zip_ref.infolist():
        name = os.path.splitext(file_info.filename)[0]
        patterns[name] = file_info

# Example usage: access a specific file from the dictionary
# file_obj = patterns['some_filename']

patterns

# Create a dictionary for easy access to files
patterns = {}

# Open the ZIP file and populate the dictionary
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    for file_info in zip_ref.infolist():
        name = os.path.splitext(file_info.filename)[0]
        patterns[name] = file_info.filename

# Example usage: access a specific file from the dictionary
# To read the content of a file named "wood":
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    with zip_ref.open(patterns["wood"]) as file:
        # Read the file content (for example, as bytes)
        data = file.read()
        # Convert the data to an appropriate format, if necessary
        # For example, you can convert it to a numpy array if it's numerical data
        wood = np.frombuffer(data, dtype=np.float32).reshape(128, 128,order='F')

wood

# Create the heatmap for the wood array

# wood2 = np.rot90(wood,2)
# wood2 = wood.T

plt.imshow(wood, cmap='inferno', interpolation='none', origin="lower")
# plt.imshow(wood, cmap='gray', interpolation='none')
plt.colorbar(label='Intensity')  # Optional: add a color bar to show intensity scale

# Hide axes and remove legend
# plt.axis('off')  # Hide axes

# Show the plot
plt.show()

# plt.imshow(wood,orientation=u'vertical')

def punch_hole(data):
    """
    Create an elliptical hole in the data.

    Parameters:
    data (np.ndarray): Input data matrix.

    Returns:
    tuple: (hole, mask) where `hole` is the data with an elliptical hole,
            and `mask` indicates where the hole was punched.
    """
    n1, n2 = data.shape
    hole = np.zeros_like(data, dtype=np.float32, order='F')
    mask = np.zeros((n1, n2), dtype=bool, order='F')

    for i2 in range(n2):
        for i1 in range(n1):
            # x = (i1 - 1) / n1 - 0.5
            # y = (i2 - 1) / n2 - 0.3
            x = (i1) / n1 - 0.5
            y = (i2) / n2 - 0.3
            u = x + y
            v = (x - y) / 2
            if u*u + v*v < 0.15:
                hole[i1, i2] = 0.0
            else:
                hole[i1, i2] = data[i1, i2]
                mask[i1, i2] = True

    return hole, mask

# Example usage with `wood` array
whole, wmask = punch_hole(wood)

# whole_julia = np.load("whole_julia.npy")
# np.array_equal(whole,whole_julia)

# wmask_julia = np.load("wmask_julia.npy")
# np.array_equal(wmask,wmask_julia)

np.isfortran(whole)

plt.imshow(whole, cmap='inferno', interpolation='none', origin="lower")

plt.imshow(wmask, cmap='inferno', interpolation='none', origin="lower")

def helix(lag, ci):
    """
    Convert filter lags to helix lags for a given grid.

    Args:
        lag: A list of tuples representing the filter lags.
        ci: A tuple representing the shape of the grid.

    Returns:
        A list of helix lags.
    """

    # Middle of the grid
    # mid = (np.array(holepad.shape) // 2) -1
    mid = (np.array(ci) // 2) -1

    # Helix index of middle
    # linear_indices_ci = np.arange(holepad.size).reshape(holepad.shape, order='F')
    linear_indices_ci = np.arange(ci.prod()).reshape(tuple(ci), order='F')

    hmid = linear_indices_ci[mid[0],mid[1]]


    # map = [l + mid for l in lag]
    map = lag + mid

    # values = [(linear_indices_ci[idx[0], idx[1]])-hmid for idx in map]
    values = linear_indices_ci[map[:, 0], map[:, 1]] - hmid
    return values

# def stream_missing_helix(d_n_dim, k_n_dim, lag, λ, std=0, seed=1):
#     "Fill missing data in multiple dimensions using streaming PEF on a helix"
#     d = np.reshape(d_n_dim,-1,order='F')
#     k = np.reshape(k_n_dim,-1,order='F')


#     n1 = len(d)
#     na = len(lag)
#     ci = np.array(d_n_dim.shape, order='F')
#     hlag = helix(lag, ci)
#     maxlag = np.max(hlag)

#     a = np.zeros(na, order='F')  # streaming PEF
#     da = 0.  # d (dot) a
#     dd = 0.  # d (dot) d

#     # Compute initial dd
#     for ia in range(na):
#         # i1, i2 = np.unravel_index(maxlag - hlag[ia],d.shape)
#         dd += d[maxlag - hlag[ia]] ** 2
#         # dd += d[i1,i2]

#     np.random.seed(seed)

#     ################################################################### OLD
#     for i1 in range(maxlag, n1):
#         if k[i1]:
#             dn = d[i1]
#             rn = (dn + da) / (λ + dd)
#         else:  # assume r_n is random
#             rn = std * np.random.randn() / λ
#             dn = rn * (λ + dd) - da
#             d[i1] = dn

#         # Update PEF
#         for ia in range(na):
#             if (i1 - hlag[ia]) >= 0:  # Ensure index is within bounds
#                 a[ia] -= rn * d[i1 - hlag[ia]]

#         # Update dd and da
#         if (i1 - maxlag) >= 0:  # Ensure index is within bounds
#             dd += dn * dn - d[i1 - maxlag] * d[i1 - maxlag]
#         da = dn * a[0]
#         for ia in range(1, na):
#             if (i1 + 1 - hlag[ia]) >= 0:  # Ensure index is within bounds
#                 da += a[ia] * d[i1 + 1 - hlag[ia]]
#     ################################################################### OLD

from numba import njit
import numpy as np

@njit
def stream_missing_helix_core(d, k, hlag, λ, std, maxlag, n1):
    na = len(hlag)
    a = np.zeros(na)
    da = 0.
    dd = 0.

    # Compute initial dd
    for ia in range(na):
        dd += d[maxlag - hlag[ia]] ** 2

    for i1 in range(maxlag, n1):
        if k[i1]:
            dn = d[i1]
            rn = (dn + da) / (λ + dd)
        else:  # assume r_n is random
            rn = std * np.random.randn() / λ
            dn = rn * (λ + dd) - da
            d[i1] = dn

        # Update PEF
        for ia in range(na):
            if (i1 - hlag[ia]) >= 0:  # Ensure index is within bounds
                a[ia] -= rn * d[i1 - hlag[ia]]

        # Update dd and da
        if (i1 - maxlag) >= 0:  # Ensure index is within bounds
            dd += dn * dn - d[i1 - maxlag] * d[i1 - maxlag]
        da = dn * a[0]
        for ia in range(1, na):
            if (i1 + 1 - hlag[ia]) >= 0:  # Ensure index is within bounds
                da += a[ia] * d[i1 + 1 - hlag[ia]]

    return d

def stream_missing_helix(d_n_dim, k_n_dim, lag, λ, std=0, seed=1):
    "Fill missing data in multiple dimensions using streaming PEF on a helix"
    d = np.reshape(d_n_dim, -1, order='F')
    k = np.reshape(k_n_dim, -1, order='F')

    n1 = len(d)
    na = len(lag)
    ci = np.array(d_n_dim.shape, order='F')
    hlag = helix(lag, ci)
    maxlag = np.max(hlag)

    np.random.seed(seed)

    # Call the JIT-compiled core function
    d = stream_missing_helix_core(d, k, hlag, λ, std, maxlag, n1)

    return np.reshape(d, d_n_dim.shape, order='F')

# 11 x 11 PEF
lag = [(x, 0) for x in range(1, 6)]  # Initial filter lags for the first row
# Extend to a 2D grid
for k in range(1, 11):
    lag.extend([(x, k) for x in range(-5, 6)])

# Convert to numpy array if needed
lag = np.array(lag)

def fill_hole(forward, hole, mask, pad, noise=0, seed=1):
    "Fill holes in data using forward or backward filling"

    if forward:
        # Pad data with zeros on the left
        holepad = np.hstack([np.zeros((hole.shape[0], pad), dtype=np.float32, order="F"), hole])

        maskpad = np.hstack([np.zeros((mask.shape[0], pad), dtype=bool, order="F"), mask])

        # Fill missing data
        stream_missing_helix(holepad, maskpad, lag, 1e6, noise, seed)

        # Return data without the padding
        return holepad[:, pad:]

    else:
        # Reverse the data
        rhole = np.flip(hole, axis=1)
        rmask = np.flip(mask, axis=1)

        # Pad reversed data with zeros on the left
        holepad = np.hstack([np.zeros((rhole.shape[0], pad), dtype=np.float32, order="F"), rhole])
        maskpad = np.hstack([np.zeros((rmask.shape[0], pad), dtype=bool, order="F"), rmask])

        # Fill missing data
        stream_missing_helix(holepad, maskpad, lag, 1e6, noise, seed + 1)

        # Return reversed filled data
        return np.flip(holepad[:, pad:], axis=1)

# Assuming `whole` and `wmask` are already defined NumPy arrays
# Also assuming `lag` and `stream_missing_helix` are defined

# Fill the hole using forward filling
filled1 = fill_hole(True, whole, wmask, 20)

# Fill the hole using backward filling
filled2 = fill_hole(False, whole, wmask, 20)

# holepad_julia = np.load("holepad_julia.npy")
# maskpad_julia = np.load("maskpad_julia.npy")

###############
# filled1_julia = np.load("filled1_julia.npy")
# np.array_equal(filled1_julia,filled1)
###############

###############
# filled2_julia = np.load("filled2_julia.npy")
# np.array_equal(filled2_julia,filled2)
###############

def plot2(ax, data, title):
    # Display heatmap on the provided axis
    im = ax.imshow(data, cmap='gray', vmin=-137, vmax=137, origin='upper')
    ax.set_title(title)
    ax.axis('off')  # Remove axis labels and ticks
    return im  # Return the image for adding colorbars if needed

# Create the figure and subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot the three images
im1 = plot2(ax1, filled1, "(a) Filled 1")
im2 = plot2(ax2, filled2, "(b) Filled 2")
im3 = plot2(ax3, filled1 + filled2 - whole, "(c) Filled 1+2")

# Add a colorbar for each subplot (optional)
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)

# Adjust layout
plt.tight_layout()
plt.show()

np.save('filled1.npy', filled1)
np.save('filled2.npy', filled2)
filled1.shape
# filled1

# imported = np.load('filled1.npy')
# imported == filled1

# julia_filled1=np.load("npy/julia_filled1.npy")
# julia_filled2=np.load("npy/julia_filled2.npy")
# julia_both=np.load("npy/julia_both_filled.npy")

def plot2(ax, data, title):
    # Display heatmap on the provided axis
    im = ax.imshow(data, cmap='gray', vmin=-137, vmax=137, origin='upper')
    ax.set_title(title)
    ax.axis('off')  # Remove axis labels and ticks
    return im  # Return the image for adding colorbars if needed

# Fill the hole (similar to your Julia code)
filled = fill_hole(True, whole, wmask, 20, 2) + fill_hole(False, whole, wmask, 20, 2) - whole

# Create the figure and subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot the three images
im1 = plot2(ax1, wood, "(a) Ideal")
im2 = plot2(ax2, whole, "(b) Gapped")
im3 = plot2(ax3, filled, "(c) Filled")

# Add a colorbar for each subplot (optional)
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)

# Adjust layout
plt.tight_layout()
plt.show()

# Create a 128x128 array for the "herring" pattern
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    with zip_ref.open(patterns["herr"]) as file:
        # Read the file content (for example, as bytes)
        data = file.read()
        # Convert the data to an appropriate format, if necessary
        # For example, you can convert it to a numpy array if it's numerical data
        herr = np.frombuffer(data, dtype=np.float32).reshape(128, 128, order="F")

# Make a hole in the pattern using the punch_hole function
hhole, hmask = punch_hole(herr)

# Fill the hole using forward and backward filling
filled = (
    fill_hole(True, hhole, hmask, 20, 6) +
    fill_hole(False, hhole, hmask, 20, 6) - hhole
)

# Assuming 'herr', 'hhole', and 'filled' are already defined

# Create the figure and subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot the three images
im1 = plot2(ax1, herr, "(a) Ideal")
im2 = plot2(ax2, hhole, "(b) Gapped")
im3 = plot2(ax3, filled, "(c) Filled")

# Add a colorbar for each subplot (optional)
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)

# Adjust layout
plt.tight_layout()
plt.show()

# "seismic" pattern
seis_base = np.empty((250, 125), dtype=np.float32)  # single-precision array

# Read the seismic pattern data from the zip file
with zipfile.ZipFile("files.zip", "r") as zip_ref:
    with zip_ref.open(patterns["seis"]) as file:
        # Read the file content (assuming it's binary data)
        data = file.read()
        # Convert the data to a numpy array
        seis_base = np.frombuffer(data, dtype=np.float32).reshape((250, 125), order="F")

# Normalize the seismic pattern
seis = seis_base.copy()
m = np.mean(seis)
seis -= m
scale = np.std(wood) / np.std(seis)
seis *= scale

# Make a hole in the seismic pattern
shole, smask = punch_hole(seis)

# Fill the hole in the seismic pattern
filled = fill_hole(True, shole, smask, 20, 0.7) + \
         fill_hole(False, shole, smask, 20, 0.7) - shole

# Create the plots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot the three images
im1 = plot2(ax1, seis, "(a) Ideal")
im2 = plot2(ax2, shole, "(b) Gapped")
im3 = plot2(ax3, filled, "(c) Filled")

# Add a colorbar for each subplot (optional)
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)

# Adjust layout
plt.tight_layout()
plt.show()

# def stream_helix(inv, d_n_dim, r_n_dim, lag, lambd):
#     # d = d_n_dim.reshape(-1)
#     # r = r_n_dim.reshape(-1)
#     d = np.reshape(d_n_dim,-1,order='F')
#     r = np.reshape(r_n_dim,-1,order='F')

#     n1, na = len(d), len(lag)
#     # print(f"{np.indices(d.shape)=}")
#     # hlag = helix(lag, np.indices(d.shape))
#     print(f"{d_n_dim.shape=}")
#     hlag = helix(lag, np.array(d_n_dim.shape))
#     maxlag = np.max(hlag)
#     T = d.dtype
#     a = np.zeros(na, dtype=T)  # streaming PEF

#     # Initialize values
#     for i1 in range(maxlag):
#         if inv:
#             d[i1] = r[i1]
#         else:
#             r[i1] = d[i1]

#     da = 0  # d (dot) a
#     dd = 0  # d (dot) d

#     for ia in range(na):
#         dd += d[maxlag + 1 - hlag[ia]] ** 2

#     for i1 in range(maxlag, n1):
#         if inv:
#             rn = r[i1] / lambd
#             dn = rn * (lambd + dd) - da
#             d[i1] = dn
#         else:
#             dn = d[i1]
#             rn = (dn + da) / (lambd + dd)
#             r[i1] = lambd * rn

#         # Update PEF
#         for ia in range(na):
#             a[ia] -= rn * d[i1 - hlag[ia]]

#         # Update dd and da
#         dd += dn * dn - d[i1 - maxlag] * d[i1 - maxlag]
#         da = dn * a[0]

#         for ia in range(1, na):
#             da += a[ia] * d[i1 + 1 - hlag[ia]]

import numpy as np
from numba import njit

@njit
def stream_helix_core(inv, d, r, hlag, lambd, maxlag, n1, na):
    T = d.dtype
    a = np.zeros(na, dtype=T)  # streaming PEF

    # Initialize values
    for i1 in range(maxlag):
        if inv:
            d[i1] = r[i1]
        else:
            r[i1] = d[i1]

    da = 0  # d (dot) a
    dd = 0  # d (dot) d

    for ia in range(na):
        dd += d[maxlag + 1 - hlag[ia]] ** 2

    for i1 in range(maxlag, n1):
        if inv:
            rn = r[i1] / lambd
            dn = rn * (lambd + dd) - da
            d[i1] = dn
        else:
            dn = d[i1]
            rn = (dn + da) / (lambd + dd)
            r[i1] = lambd * rn

        # Update PEF
        for ia in range(na):
            a[ia] -= rn * d[i1 - hlag[ia]]

        # Update dd and da
        dd += dn * dn - d[i1 - maxlag] * d[i1 - maxlag]
        da = dn * a[0]

        for ia in range(1, na):
            da += a[ia] * d[i1 + 1 - hlag[ia]]

    return d, r

def stream_helix(inv, d_n_dim, r_n_dim, lag, lambd):
    d = np.reshape(d_n_dim, -1, order='F')
    r = np.reshape(r_n_dim, -1, order='F')

    n1, na = len(d), len(lag)
    hlag = helix(lag, np.array(d_n_dim.shape))
    maxlag = np.max(hlag)

    # Call the JIT-compiled core function
    d, r = stream_helix_core(inv, d, r, hlag, lambd, maxlag, n1, na)

    # Reshape d and r back to their original shapes
    d_n_dim = np.reshape(d, d_n_dim.shape, order='F')
    r_n_dim = np.reshape(r, r_n_dim.shape, order='F')

    return d_n_dim, r_n_dim

# Apply helix filter
pad = np.hstack((np.zeros((seis.shape[0], 20), dtype=np.float32, order="F"), seis))
res = np.empty_like(pad)

# Forward filtering
stream_helix(False, pad, res, lag, 1e6)  # pad -> res

# Backward filtering
stream_helix(True, pad, res, lag, 1e6)   # pad <- res

# Plotting the results
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

# Plot the input data
im1 = plot2(ax1, seis, "(a) Input")

# Plot the residual (scaled by 20)
im2 = plot2(ax2, 20 * res[:, 20:], "(b) Residual (x 20)")

# Plot the inverse data
im3 = plot2(ax3, pad[:, 20:], "(c) Inverse")

# Add a colorbar for each subplot (optional)
fig.colorbar(im1, ax=ax1)
fig.colorbar(im2, ax=ax2)
fig.colorbar(im3, ax=ax3)

# Adjust layout
plt.tight_layout()
plt.show()

"""# TMP ZONE

"""