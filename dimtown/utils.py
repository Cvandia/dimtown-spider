import httpx

try:
    import ujson as json
except ModuleNotFoundError:
    import json
from bs4 import BeautifulSoup

class Spider:
    '''
    爬虫基类
    '''
    def __init__(self) -> None:
        self.base_url = "https://dimtown.com/"
        self.api_url = None
        self.url = None
        self.page = 1
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            "Origin": "https://dimtown.com",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "empty",
        }

    async def _get_resp(self, url:str, params=None) -> httpx.Response:
        '''
        获取`get`响应
        
        参数:
        - url: 链接
        - params: 参数
            
        返回:
        - resp: 响应
        '''
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                resp = await client.get(
                    url, params=params, headers=self.headers, timeout=60
                    )
                return resp
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout):
            raise Exception("网络连接错误或超时")

    async def _post_resp(self, url:str, data=None):
        '''
        获取`post`响应
        
        参数:
        - url: 链接
        - data: 数据

        返回:
        - resp: 响应
        '''
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.post(
                url, data=data, headers=self.headers, timeout=60
                )
            return resp

    async def _save_html(self, url:str, file_name:str) -> bool:
        '''
        保存网页
        
        参数:
        - url: 链接
        - file_name: 文件名
        
        返回:
        - bool: 是否保存成功
        '''
        resp = await self._get_resp(url)
        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(resp.text)
            return True
        except Exception:
            raise RuntimeError("保存失败")

    async def get_img_list(self, page:int = 1) -> list:
        '''
        获取图片列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 图片列表
        '''
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url)
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
    
    async def get_title_list(self, page:int = 1) -> list:
        '''
        获取标题列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 标题列表
        '''
        url = self.api_url + "/page/" + str(page)
        try:
            resp = await self._get_resp(url)
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

    async def get_img_url(self, url:str) -> list:
        '''
        获取图片链接
        
        参数:
        - url: 链接
        
        返回:
        - list: 图片链接
        '''
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", class_="content")
        p = div.find_all("p")
        img_list = []
        for i in p:
            imgs = i.find_all("img")
            for img in imgs:
                img_list.append(img["src"])
        return img_list
    