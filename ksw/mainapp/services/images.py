from PIL import Image


def crop_center(pil_img: Image, crop_width: int, crop_height: int) -> Image:
    """Обрезает изображение по центру"""

    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_square(image_path: str, square_size: int = 200) -> Image:
    """Вырезает квадратное изображение и сжимает его до указанного размера"""

    pil_img = Image.open(image_path)

    if pil_img.height != pil_img.width:
        pil_img = crop_center(pil_img, min(pil_img.size), min(pil_img.size))
    if pil_img.height > square_size:
        pil_img.thumbnail((square_size, square_size))

    return pil_img


def crop_rect(image_path: str, width_ratio: int, rect_height: int = 300) -> Image:
    """Вырезает прямоугольное изображение и сжимает его до указанного размера"""

    pil_img = Image.open(image_path)
    new_img_width = int(pil_img.height * width_ratio)

    if pil_img.width != new_img_width:
        pil_img = crop_center(pil_img, new_img_width, pil_img.height)
    if pil_img.height > rect_height:
        pil_img.thumbnail((rect_height, rect_height))

    return pil_img
