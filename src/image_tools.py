import os
from pathlib import Path
from traceback import format_exc

import requests
from PIL import Image, ImageDraw, ImageFont
from loguru import logger as log


def add_watermark(img_path: str, watermark: str, output_path: str = None):
    """为图片加上简单的水印
    References: https://www.tutorialspoint.com/python_pillow/python_pillow_creating_a_watermark.htm

    Args:
        img_path: 需要加水印的图像路径
        watermark: 水印内容
        output_path: 加完水印后的图像路径, 默认为同个文件夹下，水印后的图像名称前加上watermarked_

    Returns:
        加水印是否成功
    """

    try:
        # Get output path
        p = Path(img_path)
        if output_path is None:
            output_path = os.path.join(p.parent, f'watermarked_{p.name}')

        # Create an Image Object from an Image
        im = Image.open(img_path)
        width, height = im.size

        # Find optimised font size
        if 250 >= width:
            size = 10
        elif 500 >= width >= 250:
            size = 20
        elif 1500 >= width > 500:
            size = 36
        elif 4000 > width > 1500:
            size = 64
        else:
            size = 100

        if size >= height:
            size = int(height / 2)

        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('arial.ttf', size)
        text_width, text_height = draw.textsize(watermark, font)

        # calculate the x,y coordinates of the text
        margin = 10
        x = width - text_width - margin
        y = height - text_height - margin

        # draw watermark in the bottom right corner
        draw.text((x, y), watermark, font=font)

        # Save watermarked image
        im.save(output_path)
        log.success(f'Add watermark in {img_path} success, save to {output_path}')
        return False
    except Exception as e:
        log.error(f'Add watermark in {img_path} error, detail: {e}')
        return False


def download_image(image_url: str, local_path: str) -> bool:
    """从网络上下载图片并保存到本地指定位置

    Args:
        image_url: 远程图片url
        local_path: 保存到本地的图片位置

    Returns:
        是否下载保存成功(bool)
    """
    try:
        with open(local_path, 'wb') as handle:
            response = requests.get(image_url, stream=True)
            if not response.ok:
                log.error(f'Download image from {image_url} failed, bad response:{response.json()}')
                return False
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)
        log.success(f'Download image from {image_url} OK, save to {local_path}')
        return True
    except Exception as e:
        log.error(f'Download image from {image_url} failed, detail: {e}, {format_exc}')
        return False
