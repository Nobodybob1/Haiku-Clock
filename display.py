import inky_frame
from picographics import PicoGraphics, DISPLAY_INKY_FRAME_7 as DISPLAY
from jpegdec import JPEG

graphics = PicoGraphics(DISPLAY)

# Display picture for day
def day_picture(haiku_text = None):
    graphics.set_pen(graphics.create_pen(255, 255, 255)) # White background
    graphics.clear()
    
    j = JPEG(graphics)
    j.open_file("/sd/bg_day.jpg")
    j.decode()
    
    # Draw haiku
    if haiku_text:
        draw_haiku(haiku_text, is_day=True)
        
    graphics.update()

# Display picture for night
def night_picture(haiku_text = None):
    graphics.set_pen(graphics.create_pen(0, 0, 0)) # Black background
    graphics.clear()
    
    j = JPEG(graphics)
    j.open_file("/sd/bg_night.jpg")
    j.decode()
    
    # Draw haiku
    if haiku_text:
        draw_haiku(haiku_text, is_day=False)
    
    graphics.update()

# Wrap lines because some lines are too long
def wrap_line(graphis, text, max_width, scale):
    words = text.split(" ")
    wrapped = []
    current = ""
    
    for word in words:
        test = current + (" " if current else "") + word
        if graphics.measure_text(test, scale) <= max_width:
            current = test
        else:
            wrapped.append(current)
            current = word
    
    if current:
        wrapped.append(current)
    
    return wrapped

def draw_haiku(haiku_text, is_day=True):
    if is_day:
        graphics.set_pen(graphics.create_pen(0, 0, 0)) # Black text for day
    else:
        graphics.set_pen(graphics.create_pen(255, 255, 255)) # White text for night
    
    # Font
    graphics.set_font("serif_italic")
    scale = 1.25
    graphics.set_thickness(2)

    # Split by commas into 3 rows
    parts = haiku_text.split(',')
    if len(parts) >= 3:
        semantic_lines = [
            parts[0].strip() + ', ',
            ','.join(parts[1:-1]).strip() + ', ',
            parts[-1].strip()
        ]
    else:
        semantic_lines = [p.strip() for p in parts]
    
    # Visual wrapping
    MAX_WIDTH = 750
    lines = []
    
    for s_line in semantic_lines:
        if graphics.measure_text(s_line, scale) <= MAX_WIDTH:
            lines.append(s_line)
        else:
            wrapped = wrap_line(graphics, s_line, MAX_WIDTH, scale)
            lines.extend(wrapped)
    
    # Calculate vertical centering
    line_height = int(35 * scale)
    total_height = line_height * len(lines)
    x = 25
    # start_y = 350
    SCREEN_HEIGHT = 480
    LOWER_HALF_TOP = SCREEN_HEIGHT // 2
    LOWER_HALF_HEIGHT = SCREEN_HEIGHT - LOWER_HALF_TOP
    
    start_y = LOWER_HALF_TOP + (LOWER_HALF_HEIGHT - total_height) // 2 + 40
    
    # Draw each line
    for i, line in enumerate(lines):
        if line:
            text_width = graphics.measure_text(line, scale)
            y = start_y + (i * line_height)
            
            graphics.text(line, x, y, scale=scale)
