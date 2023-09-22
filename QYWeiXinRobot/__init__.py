# -*- coding: utf-8 -*-
# file: __init__.py
# author: zhuyao
# email: zzyyhshs@163.com
from QYWeiXinRobot.messageApi import *


def robot_send_message_by_text(key, text: str = None, mentioned_list: list = None, mentioned_mobile_list: list = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params text: 要发送的文本消息
    :params mentioned_list: 通过userid提醒用户，例子: ['userid_1', 'userid_2'] || ['@all']
    :params mentioned_mobile_list: 通过电话号码提醒，对应的用户，例子: ['123111111111', '123111111112'] || ['@all']
    return:
    发送文本消息
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_text(content=text, mentioned_list=mentioned_list, mentioned_mobile_list=mentioned_mobile_list)


def robot_send_message_by_markdown(key, markdown: str = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params markdown: 要发送的markdown消息
    return:
    发送markdown消息
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_markdown(content=markdown)


def robot_send_message_by_image(key, image_path: str = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params image_path: 图片路径
    return:
    发送图片
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_image(image_path=image_path)


def robot_send_message_by_news(key, articles: Articles = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params articles: 要发送的图文消息，可以通过Articles类的add方法进行简单的构建，当然你也可以自己实现
    return:
    发送news消息
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_news(articles=articles)


def robot_send_message_by_file(key, file_path: str = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params file_path: 文件路径
    return:
    发送文件
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_file(file_path=file_path)


def robot_send_message_by_voice(key, voice_path: str = None) -> None:
    """
    :params key: 机器人的webhook url最后的key值
    :params voice_path: 录音文件路径
    return:
    发送录音
    """
    robot = QYWeiXinMessageRobot(key)
    robot.send_message_by_voice(voice_path=voice_path)



