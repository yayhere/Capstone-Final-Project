from PIL import Image

def convert_image_to_coe(image_path, coe_path):
    try:
        # Open the image and force standard RGB mode (removes transparency/alpha channels)
        img = Image.open(image_path).convert('RGB')
        width, height = img.size
        
        with open(coe_path, 'w') as f:
            # Write the required Vivado COE headers
            f.write("memory_initialization_radix=16;\n")
            f.write("memory_initialization_vector=\n")
            
            # Iterate through every pixel, row by row (top to bottom, left to right)
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    
                    # Scale 8-bit color (0-255) down to 4-bit color (0-15) for the FPGA
                    r_4bit = r >> 4
                    g_4bit = g >> 4
                    b_4bit = b >> 4
                    
                    # Format as a 3-character uppercase hex string (e.g., pure red = F00)
                    hex_val = f"{r_4bit:X}{g_4bit:X}{b_4bit:X}"
                    
                    # Vivado requires commas separating values, and a semicolon at the very end
                    if y == height - 1 and x == width - 1:
                        f.write(f"{hex_val};\n")
                    else:
                        f.write(f"{hex_val},\n")
                        
        print(f"Success! Converted '{image_path}' to '{coe_path}'.")
        print(f"Sprite Dimensions: {width}x{height} (Total: {width * height} addresses required in BRAM)")
        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{image_path}'. Check your spelling and path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# --- Execute the Conversion ---
# Simply change 'sprite.png' to whatever your image is named.
input_image = 'over.png'
output_coe = 'over.coe'

convert_image_to_coe(input_image, output_coe)