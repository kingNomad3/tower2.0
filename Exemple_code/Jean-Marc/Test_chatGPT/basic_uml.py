from PIL import Image, ImageDraw, ImageFont

def draw_class_diagram(classes):
    image_width = 800
    image_height = 600
    image = Image.new("RGB", (image_width, image_height), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()

    class_width = 200
    class_height = 100
    x_margin = 50
    y_margin = 50
    y_spacing = 150

    current_y = y_margin

    for class_name, attributes in classes.items():
        # Draw class box
        draw.rectangle(
            [x_margin, current_y, x_margin + class_width, current_y + class_height],
            outline="black",
        )

        # Write class name
        class_name_text = f"Class: {class_name}"
        text_width, text_height = draw.textsize(class_name_text, font)
        draw.text(
            (x_margin + (class_width - text_width) / 2, current_y + 10),
            class_name_text,
            font=font,
            fill="black",
        )

        # Write attributes
        attribute_text = "\n".join(attributes)
        draw.text(
            (x_margin + 10, current_y + 40),
            attribute_text,
            font=font,
            fill="black",
        )

        current_y += y_spacing

    image.show()

# Example classes and attributes
uml_classes = {
    "Person": ["-name: str", "-age: int", "+get_info(): str"],
    "Car": ["-brand: str", "-model: str", "+start_engine(): None"],
    "Book": ["-title: str", "-author: str", "+get_summary(): str"],
}

draw_class_diagram(uml_classes)
