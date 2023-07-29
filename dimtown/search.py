from .AnimeAvatar import AnimeAvatar
from bs4 import BeautifulSoup


class Search(AnimeAvatar):
    """
    `搜索`相关图片
    """

    def __init__(self, key_words) -> None:
        super().__init__()
        self.key_words = key_words
        self.api_url = self.base_url

    async def _save_html(self, file_name: str) -> bool:
        """
        保存网页

        参数:
        - file_name: 文件名

        返回:
        - bool: 是否保存成功
        """
        await super()._save_html(self.api_url, file_name)

    async def get_search_list(self, page: int = 1) -> list:
        """
        获取搜索列表

        参数:
        - page: 页数

        返回:
        - list: 搜索列表
        """
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url, params={"s": self.key_words})
        except Exception:
            raise Exception('page not found')
        soup = BeautifulSoup(resp.text, "html.parser")
        ul =  soup.find("ul", class_="update_area_lists cl")
        li_list = ul.find_all("li")
        phonepic_list = []
        for li in li_list:
            a = li.find("a")
            phonepic_list.append(a["href"])
        return phonepic_list

    async def get_search_title(self, page: int = 1) -> list:
        """
        获取搜索标题

        参数:
        - page: 页数

        返回:
        - list: 搜索标题
        """
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url, params={"s": self.key_words})
        except Exception:
            raise Exception('page not found')
        soup = BeautifulSoup(resp.text, "html.parser")
        ul =  soup.find("ul", class_="update_area_lists cl")
        li_list = ul.find_all("li")
        phonepic_list = []
        for li in li_list:
            a = li.find("a")
            phonepic_list.append(a["title"])
        return phonepic_list

    async def get_search_img(self, url: str) -> list:
        """
        获取搜索图片列表

        参数:
        - url: 搜索链接

        返回:
        - list: 搜索图片列表
        """
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp, "html.parser")
        div = soup.find("div", class_="kz-post_tags_list")
        a_all = div.find_all("a")
        for a in a_all:
            tags = a.get_text()
            if "头像" in tags:
                return await super().get_animeavatar_img(url)
        return await super().get_img_list(url)
