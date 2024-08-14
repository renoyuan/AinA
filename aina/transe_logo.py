from PIL import Image, ImageDraw, ImageFont

class Transform:
    FILL = " "  # 星号作为填充字符
    EMPTY = "="  # 空格作为非填充字符
    NARROW = 2  # 像素间隔
    FONT_SIZE = 45  # 字体大小
    IMG_HEIGHT = 50  # 图像高度
    COLOR_ALLOWANCE = 100  # 颜色允许的偏差值

    @staticmethod
    def transform(input_text):
        # 创建一个新图像，并设置尺寸
        image_width = len(input_text) * Transform.FONT_SIZE
        image = Image.new("RGB", (image_width, Transform.IMG_HEIGHT), "white")
        draw = ImageDraw.Draw(image)

        # 加载字体
        font = ImageFont.truetype("arial.ttf", Transform.FONT_SIZE)  # 使用系统中的 Arial 字体

        # 在图像上绘制文字
        draw.text((0, 0), input_text, fill="black", font=font)

        # 初始化输出字符串
        output_string = ""

        # 获取图像尺寸
        width, height = image.size

        # 遍历每个像素
        for i in range(0, height, Transform.NARROW):
            for j in range(0, width, Transform.NARROW):
                # 获取像素的RGB值
                r, g, b = image.getpixel((j, i))

                # 计算距离白色的平方差
                rc = (255 - r) ** 2 + (255 - g) ** 2 + (255 - b) ** 2

                # 根据平方差选择字符
                char = Transform.FILL if rc < Transform.COLOR_ALLOWANCE else Transform.EMPTY

                # 将字符添加到输出字符串
                output_string += char

            # 每一行字符后添加换行符
            output_string += "\n"

        return output_string

if __name__ == "__main__":
    text = "aina"
    result = Transform.transform(text)
    print(result)