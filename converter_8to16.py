import rasterio
import numpy as np
import argparse

def convert_byte_to_uint16(input_tif, output_tif):
    # Open the original TIFF file
    with rasterio.open(input_tif) as src:
        profile = src.profile  # Get metadata
        data = src.read()  # Read image data as a NumPy array

        # Ensure the data is uint8 before conversion
        if data.dtype == np.uint8:
            # Convert uint8 to uint16 and multiply by 256
            data_uint16 = (data.astype(np.uint16)) * 256

            # Update profile to match uint16 format
            profile.update(dtype=rasterio.uint16)

            # Write the new TIFF file
            with rasterio.open(output_tif, "w", **profile) as dst:
                dst.write(data_uint16)

            print(f"Conversion successful: {output_tif}")

        else:
            print("Error: Input image is not uint8, conversion not performed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert 8-bit TIFF to 16-bit TIFF without changing color/bands.")
    parser.add_argument("--input", required=True, help="Path to the input 8-bit TIFF file.")
    parser.add_argument("--hasil", required=True, help="Path to the output 16-bit TIFF file.")

    args = parser.parse_args()
    convert_byte_to_uint16(args.input, args.hasil)