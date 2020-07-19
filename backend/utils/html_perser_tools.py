import re

from bs4 import BeautifulSoup

"""
html文本解析器
"""


class CloudSkyHtmlParser:
    # 噪音文本
    noises = [' ', '\n\n\n', '\n\n', 'VR房源', '随时看房', '户型分间', '咨询经纪人首付']

    # 根据 css 选择器类名获取文本
    def get_texts_by_class_name(self, html, class_names):
        target_texts = []
        soup = BeautifulSoup(html, 'lxml')
        for class_name in class_names:
            text_data = soup.find_all(class_=[class_name])
            if text_data:
                data = self.erase_noises(text_data[0].get_text())
                target_texts.append(data)
            else:
                target_texts.append("element_{}_not_found".format(class_name))
        return target_texts

    # 根据 css 类名获取图片
    def get_img_by_class_name(self, html, class_names):
        target_imgs = []
        soup = BeautifulSoup(html, 'lxml')
        for class_name in class_names:
            img_data = soup.find_all(class_=[class_name])
            if img_data:
                if img_data[0].get('src'):
                    img_data = img_data[0].get('src')
                else:
                    if img_data[0].img and img_data[0].img.get('origin-src'):
                        img_data = img_data[0].img.get('origin-src')
                    else:
                        img_data = ''
                target_imgs.append(img_data)
            else:
                target_imgs.append("element_{}_not_found".format(class_name))
        return list(set(target_imgs))

    # 降噪，去除无意义字符
    def erase_noises(self, text):
        for noise in self.noises:
            text = text.replace(noise, '')
        return text

    def match_positive_number(self, text):
        if '.' in text:
            number = re.findall(".+?(\d+.\d+).+?", text)
            number = number[0] if number else -1
            return float(number)
        else:
            number = re.findall(".+?(\d+).+?", text)
            number = number[0] if number else -1
            return float(number)
