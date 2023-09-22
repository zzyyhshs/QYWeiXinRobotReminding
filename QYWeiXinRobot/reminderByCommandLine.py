# -*- coding: utf-8 -*-
# file: reminderByCommandLine.py
# author: zhuyao
# email: zzyyhshs@163.com
import calendar
import datetime
import os
import sys
import argparse

sys.path.append(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0])

from QYWeiXinRobot import *


def MyStr(value):
    return value.replace('\\n', '\n')


def get_argv():
    """
    获取cmd命令行参数
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key", required=True,
                        dest="key",
                        help="robot的key")
    parser.add_argument("-t", "--type", required=True,
                        dest="type",
                        help="发送提示的消息类型，当前支持的类型有：text、markdown、image、news、file、voice、template_card")
    parser.add_argument("-c", "--content",
                        dest="content",
                        help="发送的消息内容，发送text、markdown类型时为你要发送的内容，发送image、file、voice类型时为文件的路径。")
    parser.add_argument("-a", "--articles", nargs="+", action="append",
                        dest="articles",
                        help="发送news类型消息内容，使用格式 -a title description url picurl，发送的上限为8个")
    parser.add_argument("-u", "--user", nargs="+",
                        dest="user",
                        help="userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果获取不到userid，"
                             "可以使用mentioned_mobile_list，仅发送text类型消息时有效")
    parser.add_argument("-m", "--mobile", nargs="+",
                        dest="mobile",
                        help="手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人，仅发送text类型消息时有效")
    parser.add_argument("-L", "--lastday", action="store_true",
                        dest="lastday",
                        help="是否启用仅每月最后一天执行，默认不启用，如果需要启用在命令行中携带-L即可")
    return parser.parse_args()


class Reminder:
    ROBOT_MSG_TYPE = dict()
    # 文本
    ROBOT_MSG_TYPE[By.text] = robot_send_message_by_text
    # markdown
    ROBOT_MSG_TYPE[By.markdown] = robot_send_message_by_markdown
    # 图片
    ROBOT_MSG_TYPE[By.image] = robot_send_message_by_image
    # 图文
    ROBOT_MSG_TYPE[By.news] = robot_send_message_by_news
    # 文件
    ROBOT_MSG_TYPE[By.file] = robot_send_message_by_file
    # 语音
    ROBOT_MSG_TYPE[By.voice] = robot_send_message_by_voice
    # 模板卡片
    ROBOT_MSG_TYPE[By.template_card] = None

    def __init__(self, argv):
        self.argv = argv
        self._func = None
        self._args = list()
        self._kwargs = dict()
        self.last_day = self.argv.lastday

        self._func = self.get_message_func(argv.type)
        self._kwargs["key"] = argv.key

        if argv.type == By.text:
            if argv.content is not None:
                self._kwargs["text"] = MyStr(argv.content)
            if argv.user is not None:
                self._kwargs["mentioned_list"] = argv.user
            if argv.mobile is not None:
                self._kwargs["mentioned_mobile_list"] = argv.mobile
        elif argv.type == By.markdown:
            if argv.content is not None:
                self._kwargs["markdown"] = MyStr(argv.content)
                print(argv.content)
        elif argv.type == By.image:
            if argv.content is not None:
                self._kwargs["image_path"] = argv.content
        elif argv.type == By.news:
            if argv.articles is not None:
                articles = Articles()
                for article in argv.articles:
                    articles.add(*article)
                self._kwargs["articles"] = articles
        elif argv.type == By.file:
            if argv.content is not None:
                self._kwargs["file_path"] = argv.content
        elif argv.type == By.voice:
            if argv.content is not None:
                self._kwargs["voice_path"] = argv.content
        elif argv.type == By.template_card:
            pass

    @classmethod
    def get_message_func(cls, func_type):
        if func_type not in cls.ROBOT_MSG_TYPE:
            raise NotFoundFuncException(f"没有发送该类型消息的方法：{func_type}")
        func = cls.ROBOT_MSG_TYPE.get(func_type)
        if func is None:
            raise MethodNotImplementedException(f"当前方法尚未实现：{func_type}")
        return func

    def send(self):
        # 如果启用那么对当前天进行判断
        if self.last_day:
            print("开启控制：日期为每月最后一天时才进行发送。")
            now = datetime.datetime.now()
            # 获取当前年
            year = now.year
            # 获取当前月
            month = now.month
            # 获取今天是几号
            day = now.day
            # 获取当前年月的最后一天是几号
            last_day = calendar.monthrange(year, month)[1]
            # 当今天不等于这个月最后一天时，不执行
            if day != last_day:
                print(f"今天（{year}年{month}月{day}日）不为月底，不发送消息。")
                return
        self._func(*self._args, **self._kwargs)


def main():
    argv = get_argv()
    reminder = Reminder(argv)
    reminder.send()


if __name__ == '__main__':
    argv = get_argv()
    for k, v in argv._get_kwargs():
        print(k, v)
