<div align="center">

<a href="https://dimtown.com"><img src="./ico/ico.png" width="180" alt="Logo"></a>

</div>

<div align="center">

# dimtown-spider

_⭐基于`httpx`的为[次元小镇](https://dimtown.com)的异步爬虫⭐_

</div>

<div align="center">
    <a href="https://www.python.org/downloads/release/python-390/"><img src="https://img.shields.io/badge/python-3.9+-blue"></a><a href=""><img src="https://img.shields.io/badge/QQ-1141538825-yellow"></a><a href="https://github.com/Cvandia/dimtown-spider/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-Apache License 2.0-blue"></a><a href="https://pypi.org/project/httpx/"><img src="https://img.shields.io/badge/httpx-0.23+-gree"></a>
</div>

## ⭐ 介绍

- 本项目采用 `Apache License 2.0` 开源协议。在使用这个项目之前，请确保你已经**仔细阅读并理解了协议的相关条款**。本项目**严禁**用于任何**商业用途**，并且只能用于学习和研究。如果在使用本项目的过程中产生任何问题或结果，**我们不承担任何责任**。同时，我们鼓励用户为这个项目的改进和发展提供反馈和建议。

## 🦈 安装

<details>
<summary>安装</summary>
 
 pip 安装

 `pip install dimtown-spider -U`
 
 poetry 安装

 `poetry add dimtown-spider`

</details>

## 🐟 使用

> 可见以下示例：

```python
# 测试程序

from dimtown import Search, ReturnImage
import asyncio

sc = Search("原神")
loop = asyncio.get_event_loop()
list_ = loop.run_until_complete(sc.get_img_list())
img_list = loop.run_until_complete(sc.get_img_url(list_[0]))
async def show_image(img_list: ReturnImage):
    for img in img_list:
        print(img)
    
    # 异步迭代器，显示图片
    async for img in img_list:
        img.show()
        await asyncio.sleep(1)

loop.run_until_complete(show_image(img_list))
```

## 🐖 注意事项
 - [x] 别爬太多
 - [x] 适度使用
 - [x] 健康生活

 ## 鸣谢

 > [httpx](https://pypi.org/project/httpx) ->一款同步异步兼容的网络请求库
