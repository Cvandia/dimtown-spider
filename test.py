# 测试程序

from dimtown import Search
import asyncio
sc = Search("鬼灭之刃")
loop = asyncio.get_event_loop()
list_ = loop.run_until_complete(sc.get_search_list())
print(list_)
img_list = loop.run_until_complete(sc.get_search_img(list_[0]))
print(img_list)