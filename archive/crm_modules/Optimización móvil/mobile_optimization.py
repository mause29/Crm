def optimize_for_mobile(html_content):
    # Agregar viewport y responsive design básico
    optimized_html = html_content.replace(
        "<head>", "<head><meta name='viewport' content='width=device-width, initial-scale=1'>"
    )
    return optimized_html

def compress_images(image_path):
    from PIL import Image
    img = Image.open(image_path)
    img.save(image_path, optimize=True, quality=70)
    return image_path
