import re
from gne.utils import config
from lxml.html import HtmlElement
from gne.defaults import AUTHOR_PATTERN


class AuthorExtractor:
    def __init__(self):
        self.author_pattern = AUTHOR_PATTERN  # 初始化写好的作者匹配规则

    def extractor(self, element: HtmlElement, author_xpath=''):
        # 【GET】连续按键索引取值时，可设置值不存在时的默认值为{}，这样后面的索引就不会报错了。
        author_xpath = author_xpath or config.get('author', {}).get('xpath')  # 获取自定义的规则
        # 首先，用自定义的规则匹配作者
        if author_xpath:
            author = ''.join(element.xpath(author_xpath))
            return author
        # 其次，用写好的规则匹配作者
        text = ''.join(element.xpath('.//text()'))  # 获取全部文本
        for pattern in self.author_pattern:  # 遍历模式逐个匹配
            author_obj = re.search(pattern, text)
            if author_obj:
                return author_obj.group(1)
        # 最后，都没匹配到返回空字符串
        return ''
