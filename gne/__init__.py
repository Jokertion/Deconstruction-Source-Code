from .utils import pre_parse, remove_noise_node, config
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor


class GeneralNewsExtractor:
    def extract(self,
                html,  # 目标网站的源代码
                title_xpath='',  # 新闻标题的 XPath，用于定向提取标题
                author_xpath='',  # 文章作者的 XPath，用于定向提取文章作者
                publish_time_xpath='',  # 文章发布时间的 XPath，用于定向提取文章发布时间
                host='', # 图片所在的域名，例如 https://www.kingname.info, 那么，当GNE 从新闻网站提取到图片的相对连接``/images/123.png``时，会把 host 拼接上去，变成``https://www.kingname.info/images/123.png``
                noise_node_list=None,  # 移除会导致干扰的标签。(XPath 的列表,列表中的 XPath 对应的标签，会在预处理时被直接删除掉，从而避免他们影响新闻正文的提取)
                with_body_html=False):  # 为 True时，返回的结果会包含字段 body_html，内容是新闻正文所在标签的 HTML 源代码，默认为False
        # 预解析html(剔除换行和无用节点)
        element = pre_parse(html)
        # 剔除用户自定义的干扰节点
        remove_noise_node(element, noise_node_list)
        # 正文抽取
        content = ContentExtractor().extract(element, host, with_body_html)
        # 标题抽取
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        # 发表时间抽取
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        # 作者抽取
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        # 汇总结果字典
        result = {'title': title,
                  'author': author,
                  'publish_time': publish_time,
                  'content': content[0][1]['text'],
                  'images': content[0][1]['images']}
        # 判断结果字典是否加入源码
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']
        return result
