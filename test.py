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