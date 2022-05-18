from PIL import Image


def crop_center(pil_img, crop_width: int, crop_height: int) -> Image:
    """
    Функция обрезает изображение по центру
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def crop_and_resize(image_path: str, square_size: int = None) -> Image:
    """
    Функция вырезает квадратное изображение и сжимает его до указанного размера
    """
    pil_img = Image.open(image_path)
    pil_img = crop_center(pil_img, min(pil_img.size), min(pil_img.size))
    if square_size and pil_img.height > square_size:
        pil_img.thumbnail((square_size, square_size))
    return pil_img
