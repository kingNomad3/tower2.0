from PIL import Image, ImageDraw

taille = 70

#################################### PACMAN ############################################

# ---- PIL.Image.new(mode, size, color)
## im = Image.new('RGB', (400, 400), (250, 0, 0))
# img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

# draw = ImageDraw.Draw(img)
# draw.ellipse((0, 0, taille-1, taille-1), fill=(0, 0, 255))
# draw.pieslice((0, 0, taille-1, taille-1), start=25, end=325, fill=(255, 255, 0), outline=(0, 0, 0))

# img.save('test.gif', 'GIF', transparency=0)
# img.save('pacman.png', 'PNG')


################################### FANTOME ############################################

### Normal

# colors = {
#     'bleu' : (47, 237, 209),
#     'orange' : (255, 152, 2),
#     'rouge' : (211, 0, 0),
#     'rose' : (255, 139, 218)
# }
# # color = (47, 237, 209)
# x_axis = 17.25

# for nom, color in colors.items():
#     img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

#     draw = ImageDraw.Draw(img)

#     #Corps
#     draw.pieslice((0, 0, taille-1, taille-1), start=180, end=360, fill=color)
#     draw.rectangle((0, taille/2-1, taille-1, taille-15),fill=color)
#     draw.polygon(((0, taille-15), (4, taille-1), (6, taille-1), (15, taille-15)), fill=color)
#     draw.polygon(((15, taille-15), (24, taille-1), (26, taille-1), (34.5, taille-15)), fill=color)
#     draw.polygon(((34.5, taille-15), (44, taille-1), (46, taille-1), (54, taille-15)), fill=color)
#     draw.polygon(((54, taille-15), (64, taille-1), (66, taille-1), (69, taille-15)), fill=color)
#     draw.line([0, taille-14, taille-1, taille-14], fill=color, width=3)

#     # Yeux
#     draw.ellipse((x_axis-6, 11, x_axis+12, 36), fill=(255,255,255))
#     draw.ellipse(((x_axis*3)-12, 11, (x_axis*3)+6, 36), fill=(255,255,255))
#     draw.ellipse((x_axis-1, 22, x_axis+7, 32), fill=(0,0,0))
#     draw.ellipse(((x_axis*3)-7, 22, (x_axis*3)+1, 32), fill=(0,0,0))

#     img.save(f'img/f_{nom}_center.png', 'PNG')


## Spécial

# colors = {
#     'electrocute' : (14, 58, 235),
#     'empoisonne' : (20, 156, 25),
# }
# # color = (47, 237, 209)
# x_axis = 17.25

# for nom, color in colors.items():
#     img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

#     draw = ImageDraw.Draw(img)
#     w = 5

#     #Corps
#     draw.pieslice((0, 0, taille-1, taille-1), start=180, end=360, fill=color)
#     draw.rectangle((0, taille/2-1, taille-1, taille-15),fill=color)
#     draw.polygon(((0, taille-15), (4, taille-1), (6, taille-1), (15, taille-15)), fill=color)
#     draw.polygon(((15, taille-15), (24, taille-1), (26, taille-1), (34.5, taille-15)), fill=color)
#     draw.polygon(((34.5, taille-15), (44, taille-1), (46, taille-1), (54, taille-15)), fill=color)
#     draw.polygon(((54, taille-15), (64, taille-1), (66, taille-1), (69, taille-15)), fill=color)
#     draw.line([4.5, taille-23, 11, taille-23], fill=(237, 240, 237), width=w)
#     draw.line([12, taille-28, 26, taille-28], fill=(237, 240, 237), width=w)
#     draw.line([27, taille-23, 41, taille-23], fill=(237, 240, 237), width=w)
#     draw.line([42, taille-28, 57, taille-28], fill=(237, 240, 237), width=w)
#     draw.line([58, taille-23, 64.5, taille-23], fill=(237, 240, 237), width=w)

#     # Yeux
#     draw.rectangle((x_axis-1, 22, x_axis+7, 32), fill=(237, 240, 237))
#     draw.rectangle(((x_axis*3)-7, 22, (x_axis*3)+1, 32), fill=(237, 240, 237))

#     img.save(f'img/f_{nom}_center.png', 'PNG')


################################### CERISE ############################################


img = Image.new('RGBA', (taille, taille), (0, 0, 0, 0))

draw = ImageDraw.Draw(img)
draw.ellipse((0, taille/2-10, taille/2, taille-10), fill=(255, 0, 0), outline=(0,0,0))
draw.ellipse((taille/2-3, taille/2-3, taille-3, taille-3), fill=(255, 0, 0), outline=(0,0,0))
draw.arc((taille/3, taille/2, taille-1, 0), fill=(212, 159, 74))

img.save('img/cerise.png', 'PNG')


################################### CHATEAU ############################################

img = Image.new('RGBA', (130, 200), (255, 0, 0, 0))

x = 20
color = 'blue'
draw = ImageDraw.Draw(img)
#     draw.line([58, taille-23, 64.5, taille-23], fill=(237, 240, 237), width=w)
draw.line([7,70,7,7], fill=color, width=7)
draw.line([4,7,122,7], fill=color, width=7)
draw.line([122,4,122,192], fill=color, width=7)
draw.line([125,192,7,192], fill=color, width=7)
draw.line([7,195,7,130], fill=color, width=7)

draw.line([7+x,70,7+x,7+x], fill=color, width=7)
draw.line([4+x,7+x,122-x,7+x], fill=color, width=7)
draw.line([122-x,4+x,122-x,192-x], fill=color, width=7)
draw.line([125-x,192-x,7+x,192-x], fill=color, width=7)
draw.line([7+x,195-x,7+x,130], fill=color, width=7)

draw.line([4,70,10+x,70], fill=color, width=7)
draw.line([4,130,10+x,130], fill=color, width=7)

draw.line([15.5,74,15.5,126], fill='pink', width=7)

img.save('chateau.png', 'PNG')
