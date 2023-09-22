# -*- coding: utf-8 -*-
# file: messageApi.py
# author: zhuyao
# email: zzyyhshs@163.com
import base64
import hashlib
import json
import os

import requests
from requests_toolbelt import MultipartEncoder


class UploadFileException(Exception):
    """
    上传文件错误
    """


class OverMaximumLengthException(Exception):
    """
    超出最大长度错误
    """


class NotFoundFuncException(Exception):
    """
    没有找到方法错误
    """


class MethodNotImplementedException(Exception):
    """
    方法未实现
    """


class By:
    text = "text"
    markdown = "markdown"
    image = "image"
    news = "news"
    file = "file"
    voice = "voice"
    template_card = "template_card"


class Articles(list):
    def __init__(self):
        self.max_len = 8
        super(Articles, self).__init__()

    def add(self, title: str, description: str, url: str, picurl: str = None) -> None:
        """
        :params title: 标题
        :params description: 描述
        :params url: 点击跳转的链接，例子：www.qq.com
        :params picurl: 图片链接，例子："http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
        return:
        """
        if len(self) >= self.max_len:
            raise OverMaximumLengthException("超出最大长度")
        data = dict()
        data["title"] = title
        data["description"] = description
        data["url"] = url
        if picurl is not None:
            data["picurl"] = picurl
        self.append(data)


class QYWeiXinRobotBase:
    URL = "https://qyapi.weixin.qq.com"

    def __init__(self, key):
        self._robot_key = key

    def upload_file(self, file_abs_path, file_type):
        """
        上传 临时素材资源
        接口文档地址：https://work.weixin.qq.com/api/doc/90000/90136/91770

        上传的文件限制：
            所有类型的文件大小均要求大于5个字节

            普通文件(file)：文件大小不超过20M
            语音(voice)：文件大小不超过2M，播放长度不超过60s，仅支持AMR格式

        :param file_abs_path: 需要上传文件的绝对路径
        :param file_type: 文件类型，分别有语音(voice)和普通文件(file)
        :return: media_id
        """
        # 用户收到文件时显示的文件名
        file_name = os.path.basename(file_abs_path)

        m = MultipartEncoder(
            fields={'media': (file_name, open(file_abs_path, 'rb'))},
        )

        headers = dict()
        headers['Content-Type'] = m.content_type

        file_upload_result = requests.post(
            "%s/cgi-bin/webhook/upload_media?key=%s&type=%s" % (self.URL, self._robot_key, file_type),
            headers=headers,
            data=m,
        )
        response_result = json.loads(file_upload_result.text)
        if response_result['errcode'] == 0:
            return response_result["media_id"]
        else:
            raise UploadFileException(f"上传文件错误，文件名称：{file_name}；错误信息：{file_upload_result.text}。")

    def send_message(self, message, message_type):
        """
        接口文档地址：https://work.weixin.qq.com/api/doc/90000/90136/91770
        :param key: robot key
        :param massage:
        :param massage_type:
        :return:
        """
        headers = dict()
        headers['Content-Type'] = 'application/json'

        content = dict()
        content['msgtype'] = message_type
        content[message_type] = message
        print("发送的消息：", content)
        result = requests.post(
            "%s/cgi-bin/webhook/send?key=%s" % (self.URL, self._robot_key),
            headers=headers,
            json=content)
        print("发送的结果：", result.text)


class QYWeiXinMessageRobot(QYWeiXinRobotBase):

    @staticmethod
    def get_base64(file_path):
        with open(file_path, 'rb') as data:
            base64_str = base64.b64encode(data.read()).decode()
        return base64_str

    @staticmethod
    def get_md5(file_path):
        with open(file_path, 'rb') as data:
            md5hash = hashlib.md5(data.read())
            md5 = md5hash.hexdigest()
        return md5

    def send_message_by_text(self, content, mentioned_list=None, mentioned_mobile_list=None):
        """
        :param content: 文本内容，最长不超过2048个字节，必须是utf8编码
        :param mentioned_list: userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
        :param mentioned_mobile_list: 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人
        :return:
        """
        data = dict()
        data['content'] = content
        data['mentioned_list'] = mentioned_list
        data['mentioned_mobile_list'] = mentioned_mobile_list
        self.send_message(message=data, message_type=By.text)

    def send_message_by_markdown(self, content):
        """
        :param content: markdown内容，最长不超过4096个字节，必须是utf8编码

        目前支持的markdown语法是如下的子集：
            - 标题 （支持1至6级标题，注意#与文字中间要有空格）
                # 标题一
                ## 标题二
                ### 标题三
                #### 标题四
                ##### 标题五
                ###### 标题六
            - 加粗
                **bold**
            - 链接
                [这是一个链接](http://work.weixin.qq.com/api/doc)
            - 行内代码段（暂不支持跨行）
                `code`
            - 引用
                > 引用文字
            - 字体颜色(只支持3种内置颜色)
                <font color="info">绿色</font>
                <font color="comment">灰色</font>
                <font color="warning">橙红色</font>
        """
        data = dict()
        data['content'] = content
        self.send_message(message=data, message_type=By.markdown)

    def send_message_by_image(self, image_path):
        """
        :param image_path: 图片路径
        """
        data = dict()
        data['base64'] = self.get_base64(image_path)
        data['md5'] = self.get_md5(image_path)
        self.send_message(message=data, message_type=By.image)

    def send_message_by_news(self, articles):
        data = dict()
        data["articles"] = articles
        self.send_message(message=data, message_type=By.news)

    def send_message_by_file(self, file_path):
        media_id = self.upload_file(file_abs_path=file_path, file_type='file')
        data = dict()
        data['media_id'] = media_id
        self.send_message(message=data, message_type=By.file)

    def send_message_by_voice(self, voice_path):
        media_id = self.upload_file(file_abs_path=voice_path, file_type='voice')
        data = dict()
        data['media_id'] = media_id
        self.send_message(message=data, message_type=By.voice)

    def send_message_by_template_card(self):
        """TODO 待实现"""

