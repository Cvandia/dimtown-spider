# 测试程序

from dimtown import Cosplay
import asyncio

# keyword = input("请输入关键词：\n")
# sc = Search(keyword)
cs = Cosplay()


async def main():
    # 获取文章链接列表
    list_ = await cs.get_article_urls()
    print(f"文章链接列表：{list_[0:5]}")
    # 获取图片链接
    img_list = await cs.get_img_url(list_[0])
    print(f"图片链接：{img_list[0:5]}")
    # articles = await cs.get_articles(page=1)
    # for article in articles:
    #     print(article.title)
    #     print(article.url)
    #     print(article.img_urls)
    #     print("#" * 50)


asyncio.run(main())
