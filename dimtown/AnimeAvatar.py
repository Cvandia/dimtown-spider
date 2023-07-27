from .utils import Spider
from bs4 import BeautifulSoup

class AnimeAvatar(Spider):
    '''
    `漫画头像`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "comictx"
    
    async def _save_html(self, file_name:str) -> bool:
        '''
        保存网页
        
        参数:
            - file_name: 文件名

        返回:
            - bool: 是否保存成功
            '''
        await super()._save_html(self.api_url, file_name)

    async def get_animeavatar_list(self, page:int = 1) -> list:
        '''
        获取漫画头像列表
        
        参数:
            - page: 页数

        返回:
            - list: 漫画列表'''
        return await super().get_img_list(page)
    
    async def get_animeavatar_title(self, page:int = 1) -> list:
        '''
        获取漫画头像标题

        参数:
            - page: 页数

        返回:
            - list: 漫画标题
        '''
        return await super().get_title_list(page)
    
    async def get_animeavatar_img(self, url:str) -> list:
        '''
        获取漫画头像图片列表
        
        参数:
            - url: 漫画头像链接
            
        返回:
            - list: 漫画头像图片列表
        '''
        resp = await self._get_resp(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        div = soup.find("div", class_="content")
        img_list = []
        for img in div.find_all("img"):
            img_list.append(img["src"])
        return img_list
