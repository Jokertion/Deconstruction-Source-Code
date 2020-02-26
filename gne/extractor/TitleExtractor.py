import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import TITLE_HTAG_XPATH, TITLE_SPLIT_CHAR_PATTERN


class TitleExtractor:
    def extract_by_xpath(self, element, title_xpath):
        # 按照用户给定的xpath规则提取
        if title_xpath:
            title_list = element.xpath(title_xpath)
            if title_list:
                return title_list[0]
            else:
                return ''
        return ''

    def extract_by_title(self, element):
        # 按照<title> 提取
        """
        直接提取 <title> 标签中的内容
        W3C标准中HTML结构:

        <!DOCTYPE html>
        <html>
          <head>
            <meta charset="UTF-8">
            <title>网页标题</title>
          </head>
          <body>
            <h1>网页正文</h1>
          </body>
        </html>
        :param element:
        :return:
        """
        title_list = element.xpath('//title/text()')
        if not title_list:
            return ''
        # 切除<title>中标题后面的来源部分，按 _ | - 切割
        # 例如：多艘国际邮轮被卷入新冠肺炎疫情风波 该谁负责？_网易新闻
        title = re.split(TITLE_SPLIT_CHAR_PATTERN, title_list[0])
        if title:
            return title[0]
        else:
            return ''

    def extract_by_htag(self, element):
        #  按照各种h标签提取标题
        title_list = element.xpath(TITLE_HTAG_XPATH)
        if not title_list:
            return ''
        return title_list[0]

    def extract(self, element: HtmlElement, title_xpath: str = ''):
        title_xpath = title_xpath or config.get('title', {}).get('xpath')
        title = self.extract_by_xpath(element, title_xpath) or self.extract_by_title(element) or self.extract_by_htag(
            element)
        return title.strip()
