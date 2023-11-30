from PIL import Image, ImageDraw

# Creer une nouvelle image
icon_size = (64, 64)  # Icon size (adjust as needed)
icon = Image.new('RGBA', icon_size, (0,0,0,0))  # Create a white icon

# Create a drawing context
draw = ImageDraw.Draw(icon)

# Define the tower's dimensions and colors
tower_gauche = (18, 6, 24, 12)  # (left, top, right, bottom)
tower_droite = (42, 6, 48, 12)  # (left, top, right, bottom)
tower_base = (10, 40, 54, 54)  # (left, top, right, bottom)
tower_body = (20, 10, 44, 40)
tower_color = (200, 10, 100)  # Gray color

# Draw the tower using rectangles
draw.rectangle(tower_base, fill=tower_color)
draw.rectangle(tower_body, fill=tower_color)
draw.rectangle(tower_gauche, fill=tower_color)
draw.rectangle(tower_droite, fill=tower_color)

# enregistrer l'icone
icon.save('tower_icon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

