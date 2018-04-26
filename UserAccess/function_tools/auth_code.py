#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import random
import string
from PIL import Image, ImageDraw, ImageFont, ImageFilter


# class GenerateAuthCode(object):
#     """
#     生成随机验证码。
#     """
#     def random_char(self):
#         """
#         生成随机字母.
#         :return:
#         """
#         return chr(random.randint(65, 90))
#
#     def random_color1(self):
#         """
#         生成随机颜色1。
#         :return:
#         """
#         return random.randint(64, 255), random.randint(64, 255), random.randint(64, 255)
#
#     def random_color2(self):
#         """
#         生成随机颜色2.
#         :return:
#         """
#         return random.randint(32, 127), random.randint(32, 127), random.randint(32, 127)
#
#     def generate_code(self):
#         width = 60 * 4
#         height = 60
#         image = Image.new("RGB", (width, height), (255, 255, 255))  # 创建图片
#         font = ImageFont.truetype("COOPBL.TTF", 36)  # 创建字体
#         draw = ImageDraw.Draw(image)  # 创建画布
#         code = self.random_char()
#         for x in range(width):
#             for y in range(height):
#                 draw.point((x, y), fill=self.random_color1())  # 填充像素
#         for t in range(4):
#             draw.text((60 * t + 10, 10), code, font=font, fill=self.random_color2())  # 填充文字
#         img = image.filter(ImageFilter.BLUR)  # 模糊图像
#         # image.save("code.jpg", "jpeg")  # 保存
#         return img, code


class GenerateAuthCode(object):
    @staticmethod
    def get_random_char():
        """
        生成随机字符串,string模块包含各种字符串，以下为小写字母加数字.
        :return:
        """
        ran = string.ascii_lowercase+string.digits
        char = ''
        for i in range(4):
            char += random.choice(ran)
        return char

    @staticmethod
    def get_random_color():
        """
        返回一个随机的RGB颜色
        :return:
        """
        return random.randint(50, 150), random.randint(50, 150), random.randint(50, 150)

    def create_code(self):
        img = Image.new('RGB', (120, 50), (255, 255, 255))  # 创建图片，模式，大小，背景色
        draw = ImageDraw.Draw(img)  # 创建画布
        font = ImageFont.truetype("/static/user_access/font/COOPBL.TTF", 30)
        # font = ImageFont.truetype(os.path.join(settings.VERIFICATION_CODE_IMGS_DIR, "COOPBL.TTF"), 25)  # 设置字体
        code = self.get_random_char()
        for t in range(4):
            draw.text((30 * t + 5, 0), code[t], self.get_random_color(), font)  # 将生成的字符画在画布上
        for _ in range(random.randint(0, 50)):
            draw.point((random.randint(10, 120), random.randint(10, 80)), fill=self.get_random_color())  # 生成干扰点
        img = img.filter(ImageFilter.BLUR)  # 使用模糊滤镜使图片模糊
        return img, code
