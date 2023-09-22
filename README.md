# 1. 项目名
QYWeiXinRobotReminding

# 2. 项目说明
- 对企业微信中的消息提醒机器人的api进行了封装，提供了更简易的调用方式
- 实现了通过命令行参数调用机器人进行发送消息的功能
- 可以结合jenkins灵活配置定时任务进行消息提醒

# 3. 本地安装
1. 安装 [python](https://www.python.org/downloads/) 环境
2. 安装依赖环境`pip install requirements.txt`

# 4. 结合jenkins使用
## 4.1. 如何配置
1. jenkins的node中部署python3的环境
2. 在node上安装python依赖环境`pip install requirements.txt`
3. 通过jenkins构建器配置Cron表达式设置定时执行时间[Cron表达式参考文档](https://en.wikipedia.org/wiki/Cron)
4. 在构建步骤中添加执行步骤
    - windows的node添加步骤`执行windows批处理命令`
    - linux的node添加步骤`执行shell`
5. 添加消息发送命令

## 4.2. 命令行参数说明
### 4.2.1. 如果想要发送消息，有2个必传参数
- **-k**：robot的32位key，鼠标移动到你创建的机器人上，就可以看到。大概长这个样子：8ede96f2-aaaa-bbbb-cccc-dddddddddddd
- **-t**：需要发送的消息类型，在企业微信机器人中当前仅支持7种类型：text、markdown、image、news、file、voice、template_card
### 4.2.2. 还有一些其他的参数，用来构建你要发送的消息
- **-c**：发送text、markdown、image、file、voice类型消息时需要用到的参数，用来构建你需要发送的消息内容
- **-a**：发送news类型消息时用到的参数，用来构建news类型的消息，只有当你发送news类型消息时才会用到
- **-u**：通过userid，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果获取不到userid，可以使用mentioned_mobile_list。只有消息类型为text时才能进行@操作（仅消息类型为text时才会用到）
- **-m**：通过手机号，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人。只有消息类型为text时才能进行@操作（仅消息类型为text时才会用到）
### 4.2.3. 一个特殊的参数，控制是否是每个月最后一天执行
- **-L**：是否启用仅每月最后一天执行，默认不启用，如果需要启用在命令行中携带-L即可。这个参数主要解决jenkins中的cron表达式，配置不出仅每个月最后一天执行，所实现的特殊参数。

## 4.3. 消息例子
### 4.3.1. 查看选项参数
```
python reminderByCommandLine.py -h
```
### 4.3.2. 发送文本类型消息
- 文本内容，最长不超过2048个字节，大约1024个字
```
# 1. 发送消息
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c 这是要发送的消息
# 2. 发送消息换行
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c "这是要发送的消息 \n 这是第二行的消息"
# 3. 发送消息，并@所有人
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c 这是要发送的消息 -m @all
# 4. 发送消息，并通过手机号@某个成员
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c 这是要发送的消息 -m 13111111111
# 5. 发送消息，并通过手机号@多个成员
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c 这是要发送的消息 -m 13111111111 13111111112
# 6. 使用userid的方式进行@操作和手机号的方式类似，参考上面的例子即可（-m换成-u，手机号换成userid）

```
### 4.3.3. 发送markdown类型消息
#### 目前支持的markdown语法是如下的子集
- 标题 （支持1至6级标题，注意#与文字中间要有空格）
  ```
  # 标题一
  ## 标题二
  ### 标题三
  #### 标题四
  ##### 标题五
  ###### 标题六
  ```
- 加粗
  ```
  **bold**
  ```
- 链接
  ```
  [这是一个链接](http://work.weixin.qq.com/api/doc)
  ```
- 行内代码段（暂不支持跨行）
  ```
  `code`
  ```
- 引用
  ```
  > 引用文字
  ```
- 字体颜色(只支持3种内置颜色)
  ```
  <font color="info">绿色</font>
  <font color="comment">灰色</font>
  <font color="warning">橙红色</font>
  ```
- 换行
  ```
  \n
  ```
- 正文
  ```
  这是正文
  ```
#### 例子
- markdown内容，最长不超过4096个字节，大约2048个字
```
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t markdown -c "# 标题一 \n **bold** \n <font color="info">绿色</font> \n `code` \n > 引用文字 \n [这是一个链接](http://work.weixin.qq.com/api/doc) \n 这是正文"
```
### 4.3.4. 发送image类型消息
```
# -c 后面为需要上传的图片路径
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t image -c /path/image.png
```
### 4.3.5. 发送news类型消息
- 标题：不超过128个字节（大约64个字），超过会自动截断
- 描述：不超过512个字节（大约256个字），超过会自动截断
- 链接：点击后跳转的链接
- 图片链接：图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。（非必传）
```
# 1. 发送1个图文消息
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t image -a 标题 描述 www.qq.com http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png
# 2. 发送多个图文消息
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t image -a 标题 描述 www.qq.com http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png -a 标题2 描述2 www.qq.com http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png
# 3. 不添加图片链接
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t image -a 标题 描述 www.qq.com
```
### 4.3.6. 发送file类型消息
- 普通文件(file)：文件大小不超过20M
```
# -c 后面为需要上传的文件路径
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t file -c /path/file.xlsx
```
### 4.3.7. 发送voice类型消息
- 语音(voice)：文件大小不超过2M，播放长度不超过60s，仅支持AMR格式
```
# -c 后面为需要上传的文件路径
python reminding.py -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t voice -c /path/voice.amr
```
### 4.3.8. 发送template_card类型消息
- 尚未实现命令行的调用方式

### 4.3.9. —L参数的使用
- 在jenkins中配置cron表达式为每个月最后几天执行任务`45 17 28-31 * *`，然后再通过-L参数控制仅最后一天发送消息。
```
python reminding.py -L -k 8ede96f2-aaaa-bbbb-cccc-dddddddddddd -t text -c 这是要发送的消息
```

# 5. 使用模块QYWeiXinRobot发送消息
```
from QYWeiXinRobot import *

# robot key
key = "8ede96f2-aaaa-bbbb-cccc-dddddddddddd"

# 发送文本消息
mentioned_list = ["@all"]
mentioned_mobile_list = []
text = "文本消息"
robot_send_message_by_text(key, text, mentioned_list, mentioned_mobile_list)

# 发送markdown消息
markdown = "markdown消息"
robot_send_message_by_markdown(key, markdown)

# 发送图片
image_path = "/path/image.png"
robot_send_message_by_image(key, image_path)

# 发送news消息
title = "标题"
description = "描述"
url = "www.qq.com"
picurl = "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"

articles = Articles()
articles.add(title, description, url, picurl)
robot_send_message_by_news(key, articles)

# 发送文件
file_path = "/path/file.xlsx"
robot_send_message_by_file(key, file_path)

# 发送录音
voice_path = "/path/voice.amr"
robot_send_message_by_voice(key, voice_path)
```
