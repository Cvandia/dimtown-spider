from bs4 import BeautifulSoup, Tag
from dataclasses import dataclass
import httpx
import asyncio


@dataclass
class Article:
    """文章类
    Attributes:
        title(str): 标题
        url(str): 链接
        img_urls(list): 图片链接列表
    """

    title: str
    url: str
    img_urls: list[str]


class RequestError(Exception):
    """请求错误"""

    pass


class HandleFileError(Exception):
    """文件处理错误"""


class WebChangeError(Exception):
    """网站结构变化错误"""


class Spider:
    def __init__(self) -> None:
        self.base_url = "https://dimtown.com/"
        self.api_url: str = ""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Origin": "https://dimtown.com",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
        }

    async def _get_resp(self, url: str, params=None) -> httpx.Response:
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                return await client.get(
                    url, params=params, headers=self.headers, timeout=60
                )
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            raise RequestError("请求连接失败, 请检查网络连接或者网站是否正常")

    async def _post_resp(self, url: str, data=None):
        async with httpx.AsyncClient(follow_redirects=True) as client:
            return await client.post(url, data=data, headers=self.headers, timeout=60)

    async def _save_html(self, url: str, file_name: str) -> bool:
        resp = await self._get_resp(url)
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(resp.text)
            return True
        except Exception:
            raise HandleFileError("保存失败")

    def _get_soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "html.parser")

    async def _parse_article_list(self, url: str) -> list[Tag]:
        resp = await self._get_resp(url)
        soup = self._get_soup(resp.text)
        ul = soup.find("ul", class_="update_area_lists cl")
        if isinstance(ul, Tag):
            return ul.find_all("li")
        raise WebChangeError("网站结构变化")

    async def get_article_urls(self, page: int = 1) -> list:
        """获取文章链接列表
        Args:
            page(int): 页码
        Returns:
            list: 文章链接列表
        """
        url = f"{self.api_url}/page/{page}"
        li_list = await self._parse_article_list(url)
        return [li.find("a")["href"] for li in li_list]

    async def get_articles(self, page: int = 1) -> list[Article]:
        """获取文章列表
        Args:
            page(int): 页码
        Returns:
            list: 文章列表
        """
        url = f"{self.api_url}/page/{page}"
        li_list = await self._parse_article_list(url)
        article_urls = [li.find("a")["href"] for li in li_list]
        article_titles = [li.find("a")["title"] for li in li_list]
        tasks = [self.get_img_url(url) for url in article_urls]
        img_urls = await asyncio.gather(*tasks, return_exceptions=False)
        return [
            Article(article_titles[i], article_urls[i], img_urls[i])
            for i in range(len(article_titles))
        ]

    async def get_article_titles(self, page: int = 1) -> list:
        """获取文章标题列表
        Args:
            page(int): 页码
        Returns:
            list: 文章标题列表
        """
        url = f"{self.api_url}/page/{page}"
        li_list = await self._parse_article_list(url)
        return [li.find("a")["title"] for li in li_list]

    async def get_img_url(self, url: str) -> list:
        """获取文章url对应的图片链接
        Args:
            url(str): 文章链接
        Returns:
            list: 图片链接列表
        """
        async with asyncio.Semaphore(10):
            try:
                resp = await self._get_resp(url)
            except RequestError:
                return []
            soup = self._get_soup(resp.text)
            div = soup.find("div", class_="content")
            if isinstance(div, Tag):
                return [
                    img["src"] for p in div.find_all("p") for img in p.find_all("img")
                ]
            raise WebChangeError("网站结构变化")

    async def _download_img(self, url: str, file_name: str) -> bool:
        resp = await self._get_resp(url)
        try:
            with open(file_name, "wb") as f:
                f.write(resp.content)
            return True
        except Exception:
            raise HandleFileError("下载失败")


class SelectedPixiv(Spider):
    """精选PIXIV插画"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}pzmt"


class SelectedIllustrations(Spider):
    """精选插画"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}jxmt"


class AnimeAvatar(Spider):
    """动漫头像"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}comictx"

    async def get_img_url(self, url: str) -> list:
        resp = await self._get_resp(url)
        soup = self._get_soup(resp.text)
        div = soup.find("div", class_="content")
        if isinstance(div, Tag):
            return [img["src"] for img in div.find_all("img")]
        raise WebChangeError("网站结构变化")


class ArtAlbum(Spider):
    """美图专辑"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}tujihuace"


class Cosplay(Spider):
    """cosplay"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}cosplay"


class CoupleAvatar(AnimeAvatar):
    """情侣头像"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}loverstx"


class FemaleAvatar(AnimeAvatar):
    """女生头像"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}lolitx"


class Figure(Spider):
    """手办"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}shouban"


class Hanfu(Spider):
    """汉服"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}hanfu"


class JK(Spider):
    """JK"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}jk"


class LoliTa(Spider):
    """萝莉塔"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}lolita"


class MaleAvatar(AnimeAvatar):
    """男生头像"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}mantx"


class PcPic(Spider):
    """pc壁纸"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}bz"


class PhonePic(Spider):
    """手机壁纸"""

    def __init__(self) -> None:
        super().__init__()
        self.api_url = f"{self.base_url}sjbz"


class Search(AnimeAvatar):
    """搜索"""

    def __init__(self, key_words) -> None:
        super().__init__()
        self.key_words = key_words
        self.api_url = f"{self.base_url}/page/1?s={self.key_words}"

    async def get_article_urls(self, page: int = 1) -> list:
        url = self.api_url.replace("1", str(page))
        li_list = await self._parse_article_list(url)
        return [li.find("a")["href"] for li in li_list]

    async def get_article_titles(self, page: int = 1) -> list:
        url = self.api_url.replace("1", str(page))
        li_list = await self._parse_article_list(url)
        return [li.find("a")["title"] for li in li_list]

    async def get_img_url(self, url: str) -> list:
        resp = await self._get_resp(url)
        soup = self._get_soup(resp.text)
        div = soup.find("div", class_="kz-post_tags_list")
        if isinstance(div, Tag):
            a_all = div.find_all("a")
            for a in a_all:
                if "头像" in a.get_text():
                    return await super().get_img_url(url)
            return await super(AnimeAvatar, self).get_img_url(url)
        raise WebChangeError("网站结构变化")

    async def get_articles(self, page: int = 1) -> list[Article]:
        url = self.api_url.replace("1", str(page))
        li_list = await self._parse_article_list(url)
        article_urls = [li.find("a")["href"] for li in li_list]
        article_titles = [li.find("a")["title"] for li in li_list]
        tasks = [self.get_img_url(url) for url in article_urls]
        img_urls = await asyncio.gather(*tasks, return_exceptions=False)
        return [
            Article(article_titles[i], article_urls[i], img_urls[i])
            for i in range(len(article_titles))
        ]
