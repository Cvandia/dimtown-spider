from typing import Any
import httpx

try:
    import ujson as json
except ModuleNotFoundError:
    import json
from bs4 import BeautifulSoup, Tag
import PIL.Image as Image
from typing import AsyncGenerator, Iterator


class ReturnImage(list, Image.Image):
    '''
    返回图片类
    '''
    def __init__(self, img_list: list) -> None:
        super().__init__(img_list)
        self.img_list = img_list

    async def __aiter__(self) -> AsyncGenerator[Image.Image, Any]:
        try:
            async with httpx.AsyncClient() as client:
                for img in self.img_list:
                    resp = await client.get(img)
                    img = Image.open(resp.content)
                    yield img
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            raise Exception("网络连接错误或超时")
    
    def __iter__(self) -> Iterator[str]:
        return iter(self.img_list)


class Spider:
    """
    爬虫基类
    """

    def __init__(self) -> None:
        self.base_url = "https://dimtown.com/"
        self.api_url: str = ""
        self.url: str = ""
        self.page: int = 1
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Origin": "https://dimtown.com",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
        }

    async def _get_resp(self, url: str, params=None) -> httpx.Response:
        """
        获取`get`响应

        参数:
        - url: 链接
        - params: 参数

        返回:
        - resp: 响应
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                resp = await client.get(
                    url, params=params, headers=self.headers, timeout=60
                )
                return resp
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            raise Exception("网络连接错误或超时")

    async def _post_resp(self, url: str, data=None):
        """
        获取`post`响应

        参数:
        - url: 链接
        - data: 数据

        返回:
        - resp: 响应
        """
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.post(url, data=data, headers=self.headers, timeout=60)
            return resp

    async def _save_html(self, url: str, file_name: str) -> bool:
        """
        保存网页

        参数:
        - url: 链接
        - file_name: 文件名

        返回:
        - bool: 是否保存成功
        """
        resp = await self._get_resp(url)
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(resp.text)
            return True
        except Exception:
            raise RuntimeError("保存失败")

    async def get_img_list(self, page: int = 1) -> list:
        """
        获取图片列表

        参数:
        - page: 页数

        返回:
        - list: 图片列表
        """
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url)
        except Exception:
            raise Exception("page not found")
        soup = BeautifulSoup(resp.text, "html.parser")
        ul = soup.find("ul", class_="update_area_lists cl")
        if isinstance(ul, Tag):
            li_list = ul.find_all("li")
        else:
            raise Exception("page not found")
        phonepic_list = []
        for li in li_list:
            a = li.find("a")
            phonepic_list.append(a["href"])
        if not phonepic_list:
            raise Exception("page not found")
        return phonepic_list

    async def get_title_list(self, page: int = 1) -> list:
        """
        获取标题列表

        参数:
        - page: 页数

        返回:
        - list: 标题列表
        """
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url)
        except Exception:
            raise Exception("page not found")
        soup = BeautifulSoup(resp.text, "html.parser")
        ul = soup.find("ul", class_="update_area_lists cl")
        if isinstance(ul, Tag):
            li_list = ul.find_all("li")
        else:
            raise Exception("page not found")
        phonepic_list = []
        for li in li_list:
            a = li.find("a")
            phonepic_list.append(a["title"])
        if not phonepic_list:
            raise Exception("page not found")
        return phonepic_list

    async def get_img_url(self, url: str) -> ReturnImage:
        """
        获取图片链接

        参数:
        - url: 链接

        返回:
        - list: 图片链接
        """
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", class_="content")
        if isinstance(div, Tag):
            p = div.find_all("p")
            img_list = []
            for i in p:
                imgs = i.find_all("img")
                for img in imgs:
                    img_list.append(img["src"])
            if not img_list:
                raise Exception("page not found")
            return ReturnImage(img_list)
        else:
            raise Exception("page not found")

    async def _download_img(self, url: str, file_name: str) -> bool:
        """
        下载图片

        参数:
        - url: 链接
        - file_name: 文件名

        返回:
        - bool: 是否下载成功
        """
        resp = await self._get_resp(url)
        try:
            with open(file_name, "wb") as f:
                f.write(resp.content)
            return True
        except Exception:
            raise RuntimeError("下载失败")

class SelectedPixiv(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "pzmt"


class SelectedIllustrations(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "jxmt"


class AnimeAvatar(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "comictx"

    async def get_img_url(self, url: str) -> ReturnImage:
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", class_="content")
        if isinstance(div, Tag):
            img_list = []
            for img in div.find_all("img"):
                img_list.append(img["src"])
            return ReturnImage(img_list)
        else:
            raise Exception("page not found")


class ArtAlbum(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "tujihuace"


class Cosplay(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "cosplay"


class CoupleAvatar(AnimeAvatar):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "loverstx"


class FemaleAvatar(AnimeAvatar):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "lolitx"


class Figure(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "shouban"


class Hanfu(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "hanfu"


class JK(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "jk"


class LoliTa(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "lolita"


class MaleAvatar(AnimeAvatar):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "mantx"


class PcPic(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "bz"


class PhonePic(Spider):
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "sjbz"


class Search(AnimeAvatar):
    def __init__(self, key_words) -> None:
        super().__init__()
        self.key_words = key_words
        self.api_url = self.base_url + "/page/1" + "?s=" + self.key_words

    async def get_img_list(self, page: int = 1) -> list:
        url = self.api_url.replace("1", str(page))
        try:
            resp = await self._get_resp(url, params={"s": self.key_words})
        except Exception:
            raise Exception("page not found")
        soup = BeautifulSoup(resp.text, "html.parser")
        ul = soup.find("ul", class_="update_area_lists cl")
        if isinstance(ul, Tag):
            li_list = ul.find_all("li")
            phonepic_list = []
            for li in li_list:
                a = li.find("a")
                phonepic_list.append(a["href"])
            if not phonepic_list:
                raise Exception("page not found")
            return phonepic_list
        else:
            raise Exception("page not found")

    async def get_title_list(self, page: int = 1) -> list:
        url = self.api_url.replace("1", str(page))
        try:
            resp = await self._get_resp(url, params={"s": self.key_words})
        except Exception:
            raise Exception("page not found")
        soup = BeautifulSoup(resp.text, "html.parser")
        ul = soup.find("ul", class_="update_area_lists cl")
        if isinstance(ul, Tag):
            li_list = ul.find_all("li")
            phonepic_list = []
            for li in li_list:
                a = li.find("a")
                phonepic_list.append(a["title"])
            if not phonepic_list:
                raise Exception("page not found")
            return phonepic_list
        else:
            raise Exception("page not found")

    async def get_img_url(self, url: str) -> ReturnImage:
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp, "html.parser")
        div = soup.find("div", class_="kz-post_tags_list")
        if isinstance(div, Tag):
            a_all = div.find_all("a")
            for a in a_all:
                tags = a.get_text()
                if "头像" in tags:
                    return await super().get_img_url(url)
            return await super(AnimeAvatar, self).get_img_url(url)
        else:
            raise Exception("page not found")
        