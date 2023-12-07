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


# img = Image.new('RGBA', (taille, taille), (0, 0, 0, 0))

# draw = ImageDraw.Draw(img)
# draw.ellipse((0, taille/2-10, taille/2, taille-10), fill=(255, 0, 0), outline=(0,0,0), width=1)
# draw.ellipse((taille/2-3, taille/2-3, taille-3, taille-3), fill=(255, 0, 0), outline=(0,0,0), width=1)
# draw.arc((12, 13, taille+15, taille+15), start=210, end=280, fill='saddlebrown', width=4)
# draw.arc((43, 14, taille, taille+15), start=194, end=270, fill='saddlebrown', width=4)

# img.save('img/cerise.png', 'PNG')


################################### CHATEAU ############################################

# img = Image.new('RGBA', (130, 200), (255, 0, 0, 0))

# x = 20
# color = 'blue'
# draw = ImageDraw.Draw(img)
# #     draw.line([58, taille-23, 64.5, taille-23], fill=(237, 240, 237), width=w)
# draw.line([7,70,7,7], fill=color, width=7)
# draw.line([4,7,122,7], fill=color, width=7)
# draw.line([122,4,122,192], fill=color, width=7)
# draw.line([125,192,7,192], fill=color, width=7)
# draw.line([7,195,7,130], fill=color, width=7)

# draw.line([7+x,70,7+x,7+x], fill=color, width=7)
# draw.line([4+x,7+x,122-x,7+x], fill=color, width=7)
# draw.line([122-x,4+x,122-x,192-x], fill=color, width=7)
# draw.line([125-x,192-x,7+x,192-x], fill=color, width=7)
# draw.line([7+x,195-x,7+x,130], fill=color, width=7)

# draw.line([4,70,10+x,70], fill=color, width=7)
# draw.line([4,130,10+x,130], fill=color, width=7)

# draw.line([15.5,74,15.5,126], fill='pink', width=7)

# img.save('./img/chateau.png', 'PNG')





######################################################################################
#                                                                                    #
#                                     2                                              #
#                                                                                    #
#                                                                                    #
######################################################################################






#################################### PACMAN ##########################################

# # ---- PIL.Image.new(mode, size, color)
# im = Image.new('RGB', (400, 400), (250, 0, 0))
# img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

# draw = ImageDraw.Draw(img)
# draw.pieslice((0, 0, taille-1, taille-1), start=25, end=325, fill=(255, 255, 0), outline=(0, 0, 0))
# draw.pieslice((7, 7, taille-8, taille-8), start=25, end=325, fill=(0, 0, 0), outline=(0, 0, 0))
# draw.pieslice((0, 0, taille-1, taille-1), start=25, end=325, fill=(255, 255, 0), outline=(0, 0, 0))

# img.save('./img/pacman2.png', 'PNG')


################################### FANTOME ############################################

### Normal

# colors = {
#     'bleu' : (47, 237, 209),
#     'orange' : (255, 152, 2),
#     'rouge' : (211, 0, 0),
#     'rose' : (255, 139, 218)
# }
# x_axis = 17.25
# taille_mini = 59
# color_mini = (0, 0, 0)
# compteur = -1

# for nom, color in colors.items():
#     img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

#     draw = ImageDraw.Draw(img)
#     # -3 = x
#     #Corps
#     draw.pieslice((0, 0, taille-1, taille-1), start=180, end=360, fill=color)
#     draw.rectangle((0, taille/2-1, taille-1, taille-15),fill=color)
#     draw.polygon(((0, taille-15), (4, taille-1), (6, taille-1), (15, taille-15)), fill=color)
#     draw.polygon(((15, taille-15), (24, taille-1), (26, taille-1), (34.5, taille-15)), fill=color)
#     draw.polygon(((34.5, taille-15), (44, taille-1), (46, taille-1), (54, taille-15)), fill=color)
#     draw.polygon(((54, taille-15), (64, taille-1), (66, taille-1), (69, taille-15)), fill=color)
#     draw.line([0, taille-14, taille-1, taille-14], fill=color, width=3)

#     draw.pieslice((5, 5, taille_mini+4, taille_mini+4), start=180, end=360, fill=color_mini)
#     draw.rectangle((5, taille_mini/2-4, taille_mini+4, taille_mini-11),fill=color_mini)
#     draw.polygon(((5, taille_mini-11), (5.5, taille_mini+3), (8, taille_mini+3), (17, taille_mini-11)), fill=color_mini)
#     draw.polygon(((14, taille_mini-9), (24, taille_mini+3), (26, taille_mini+3), (35, taille_mini-10)), fill=color_mini)
#     draw.polygon(((31, taille_mini-10), (44, taille_mini+3), (46, taille_mini+3), (54, taille_mini-10)), fill=color_mini)
#     draw.polygon(((50, taille_mini-10), (63.5, taille_mini+3), (63.5, taille_mini+3), (63.5, taille_mini-10)), fill=color_mini)
#     draw.line([5, taille_mini-9, taille_mini+4, taille_mini-9], fill=color_mini, width=3)

#     # Yeux
#     draw.ellipse((x_axis-6, 11, x_axis+12, 36), fill=color)
#     draw.ellipse(((x_axis*3)-12, 11, (x_axis*3)+6, 36), fill=color)
#     draw.ellipse((x_axis-1, 22, x_axis+7, 32), fill=(0,0,0))
#     draw.ellipse(((x_axis*3)-7, 22, (x_axis*3)+1, 32), fill=(0,0,0))

#     img.save(f'img/creep2{nom}.png', 'PNG')












#################################### PACMAN ##########################################

# ---- PIL.Image.new(mode, size, color)
# im = Image.new('RGB', (400, 400), (250, 0, 0))
taille = 100
color1 = (77,127,23)
color2 = (107,177,32)
color3 = (154,254,46)

tours = {
    'poison' :          [(77,127,23),   (107,177,32),     (154,254,46)],
    'mitrailleuse' :    [(24,57,43),   	(32,76,57),       (41,95,72)],
    'eclair' :          [(119,170,255), (153,204,255),    (187,238,255)],
    'grenade' :         [(163,32,32),   (220,105,0),      (235,140,0)],
    'mine' :            [(71,15,15),    (124,27,27),      (178,39,39)],
    'canon' :           [(53,62,69),    (85,95,104),      (86,129,138)]
}

for nom, tour in tours.items():
    img = Image.new('RGBA', (taille, taille), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    draw.ellipse((10, 5, 40, 35),   outline=None, fill=tour[0], width=50)
    draw.ellipse((0, 15, 35, 45),   outline=None, fill=tour[2], width=50)
    draw.ellipse((5, 30, 40, 65),   outline=None, fill=tour[0], width=50)
    draw.ellipse((12, 45, 57, 85),  outline=None, fill=tour[2], width=50)
    draw.ellipse((15, 60, 40, 85),  outline=None, fill=tour[1], width=50)
    draw.ellipse((58, 55, 87, 85),  outline=None, fill=tour[0], width=50)
    draw.ellipse((34, 79, 60, 99),  outline=None, fill=tour[0], width=50)
    draw.ellipse((40, 65, 70, 90),  outline=None, fill=tour[1], width=50)
    draw.ellipse((75, 43, 95, 63),  outline=None, fill=tour[2], width=50)
    draw.ellipse((45, 45, 75, 75),  outline=None, fill=tour[2], width=50)
    draw.ellipse((55, 30, 85, 60),  outline=None, fill=tour[0], width=50)
    draw.ellipse((75, 30, 90, 45),  outline=None, fill=tour[1], width=50)
    draw.ellipse((60, 15, 85, 40),  outline=None, fill=tour[0], width=50)
    draw.ellipse((30, 10, 60, 40),  outline=None, fill=tour[2], width=50)
    draw.ellipse((37, 20, 67, 50),  outline=None, fill=tour[1], width=50)
    draw.ellipse((37, 20, 67, 50),  outline=None, fill=tour[2], width=50)
    draw.ellipse((70, 5, 85, 20),   outline=None, fill=tour[2], width=50)
    draw.ellipse((75, 15, 95, 35),  outline=None, fill=tour[1], width=50)
    draw.ellipse((50, 5, 70, 25),   outline=None, fill=tour[0], width=50)

    draw.pieslice((15, 15, taille-14, taille-14), start=25, end=325, fill=(255, 255, 0), outline=(0, 0, 0), width=3)

    img.save(f'img/tour_{nom}.png', 'PNG')