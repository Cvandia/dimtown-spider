# 测试程序

from dimtown import Search, ReturnImage, Cosplay
import asyncio
import httpx

# keyword = input("请输入关键词：\n")
# sc = Search(keyword)
cs = Cosplay()
loop = asyncio.new_event_loop()

async def main():
    # 获取图片列表
    list_ = await cs.get_img_list()
    # 获取图片链接
    img_list = await cs.get_img_url(list_[0])

    print("图片链接：")
    print(img_list)
    # 保存图片
    async with httpx.AsyncClient() as client:
        try:
            for img in img_list:
                img_path = img.split("/")[-1]
                resp = await client.get(img)
                with open(f"{img_path}", "wb") as f:
                    f.write(resp.content)
        except Exception as e:
            print(e)

loop.run_until_complete(main())
loop.close()