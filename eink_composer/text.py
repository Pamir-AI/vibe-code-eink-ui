import numpy as np
from typing import Dict, Tuple, Optional, List

# 6x8 bitmap font data (subset of characters)
FONT_6X8 = {
    ' ': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
    'A': [0x30, 0x78, 0xCC, 0xCC, 0xFC, 0xCC],
    'B': [0xFC, 0x66, 0x66, 0x7C, 0x66, 0xFC],
    'C': [0x3C, 0x66, 0xC0, 0xC0, 0x66, 0x3C],
    'D': [0xF8, 0x6C, 0x66, 0x66, 0x6C, 0xF8],
    'E': [0xFE, 0x62, 0x68, 0x78, 0x62, 0xFE],
    'F': [0xFE, 0x62, 0x68, 0x78, 0x60, 0xF0],
    'G': [0x3C, 0x66, 0xC0, 0xCE, 0x66, 0x3E],
    'H': [0xCC, 0xCC, 0xCC, 0xFC, 0xCC, 0xCC],
    'I': [0x78, 0x30, 0x30, 0x30, 0x30, 0x78],
    'J': [0x1E, 0x0C, 0x0C, 0x0C, 0xCC, 0x78],
    'K': [0xE6, 0x66, 0x6C, 0x78, 0x6C, 0xE6],
    'L': [0xF0, 0x60, 0x60, 0x60, 0x62, 0xFE],
    'M': [0xC6, 0xEE, 0xFE, 0xD6, 0xC6, 0xC6],
    'N': [0xC6, 0xE6, 0xF6, 0xDE, 0xCE, 0xC6],
    'O': [0x38, 0x6C, 0xC6, 0xC6, 0x6C, 0x38],
    'P': [0xFC, 0x66, 0x66, 0x7C, 0x60, 0xF0],
    'Q': [0x78, 0xCC, 0xCC, 0xCC, 0xDC, 0x78],
    'R': [0xFC, 0x66, 0x66, 0x7C, 0x6C, 0xE6],
    'S': [0x78, 0xCC, 0x60, 0x18, 0xCC, 0x78],
    'T': [0xFC, 0xB4, 0x30, 0x30, 0x30, 0x78],
    'U': [0xCC, 0xCC, 0xCC, 0xCC, 0xCC, 0x78],
    'V': [0xCC, 0xCC, 0xCC, 0x78, 0x30, 0x30],
    'W': [0xC6, 0xC6, 0xD6, 0xFE, 0xEE, 0xC6],
    'X': [0xC6, 0x6C, 0x38, 0x38, 0x6C, 0xC6],
    'Y': [0xCC, 0xCC, 0x78, 0x30, 0x30, 0x78],
    'Z': [0xFE, 0xC6, 0x8C, 0x18, 0x32, 0xFE],
    '0': [0x78, 0xCC, 0xDC, 0xFC, 0xEC, 0x78],
    '1': [0x30, 0x70, 0x30, 0x30, 0x30, 0xFC],
    '2': [0x78, 0xCC, 0x0C, 0x38, 0x60, 0xFC],
    '3': [0x78, 0xCC, 0x0C, 0x38, 0x0C, 0xF8],
    '4': [0x1C, 0x3C, 0x6C, 0xCC, 0xFE, 0x0C],
    '5': [0xFC, 0xC0, 0xF8, 0x0C, 0x0C, 0xF8],
    '6': [0x38, 0x60, 0xC0, 0xF8, 0xCC, 0x78],
    '7': [0xFC, 0xCC, 0x0C, 0x18, 0x30, 0x30],
    '8': [0x78, 0xCC, 0x78, 0xCC, 0xCC, 0x78],
    '9': [0x78, 0xCC, 0xCC, 0x7C, 0x0C, 0x78],
    '.': [0x00, 0x00, 0x00, 0x00, 0x30, 0x30],
    ',': [0x00, 0x00, 0x00, 0x00, 0x30, 0x10],
    '!': [0x30, 0x30, 0x30, 0x30, 0x00, 0x30],
    '?': [0x78, 0xCC, 0x0C, 0x30, 0x00, 0x30],
    ':': [0x00, 0x30, 0x30, 0x00, 0x30, 0x30],
    ';': [0x00, 0x30, 0x30, 0x00, 0x30, 0x10],
    '-': [0x00, 0x00, 0x7E, 0x00, 0x00, 0x00],
    '_': [0x00, 0x00, 0x00, 0x00, 0x00, 0xFF],
    '(': [0x18, 0x30, 0x60, 0x60, 0x30, 0x18],
    ')': [0x60, 0x30, 0x18, 0x18, 0x30, 0x60],
    '/': [0x00, 0x06, 0x0C, 0x18, 0x30, 0x60],
    '+': [0x00, 0x30, 0x30, 0xFC, 0x30, 0x30],
    '=': [0x00, 0x00, 0xFC, 0x00, 0xFC, 0x00],
}

# Font dimensions
FONT_WIDTH = 6
FONT_HEIGHT = 8


def render_text(text: str, x: int = 0, y: int = 0, 
                canvas: Optional[np.ndarray] = None,
                color: int = 0, font_size: int = 1) -> np.ndarray:
    """
    Render text using bitmap font.
    
    Args:
        text: Text to render
        x: X position
        y: Y position  
        canvas: Optional canvas to draw on. If None, creates new canvas
        color: Text color (0=black, 255=white)
        font_size: Font scale factor (1=normal, 2=double, etc.)
        
    Returns:
        Canvas with rendered text
    """
    # Calculate scaled dimensions
    scaled_font_width = FONT_WIDTH * font_size
    scaled_font_height = FONT_HEIGHT * font_size
    
    if canvas is None:
        # Calculate required canvas size
        width = len(text) * scaled_font_width
        height = scaled_font_height
        canvas = np.full((height, width), 255 if color == 0 else 0, dtype=np.uint8)
        x = 0
        y = 0
    
    canvas_h, canvas_w = canvas.shape
    
    for i, char in enumerate(text):
        if char not in FONT_6X8:
            char = ' '  # Default to space for unknown characters
            
        char_data = FONT_6X8[char]
        char_x = x + i * scaled_font_width
        
        # Skip if character is outside canvas
        if char_x >= canvas_w or y >= canvas_h:
            continue
            
        # Render character with scaling
        for row in range(FONT_HEIGHT):
            if y + row * font_size >= canvas_h:
                break
                
            byte = char_data[row] if row < len(char_data) else 0
            
            for col in range(FONT_WIDTH):
                if char_x + col * font_size >= canvas_w:
                    break
                    
                # Check if bit is set
                if byte & (0x80 >> col):
                    # Draw scaled pixel block
                    for dy in range(font_size):
                        for dx in range(font_size):
                            pixel_y = y + row * font_size + dy
                            pixel_x = char_x + col * font_size + dx
                            if pixel_y < canvas_h and pixel_x < canvas_w:
                                canvas[pixel_y, pixel_x] = color
    
    return canvas


def measure_text(text: str, font_size: int = 1) -> Tuple[int, int]:
    """
    Measure the dimensions of rendered text.
    
    Args:
        text: Text to measure
        font_size: Font scale factor
        
    Returns:
        (width, height) tuple
    """
    return (len(text) * FONT_WIDTH * font_size, FONT_HEIGHT * font_size)


def wrap_text(text: str, max_width: int) -> List[str]:
    """
    Wrap text to fit within specified width.
    
    Args:
        text: Text to wrap
        max_width: Maximum width in pixels
        
    Returns:
        List of wrapped text lines
    """
    chars_per_line = max_width // FONT_WIDTH
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if len(current_line) + len(word) + 1 <= chars_per_line:
            if current_line:
                current_line += " "
            current_line += word
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
            
            # If word is too long, break it
            while len(current_line) > chars_per_line:
                lines.append(current_line[:chars_per_line])
                current_line = current_line[chars_per_line:]
    
    if current_line:
        lines.append(current_line)
    
    return lines