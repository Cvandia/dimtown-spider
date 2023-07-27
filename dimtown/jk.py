from .utils import Spider

class JK(Spider):
    '''
    `JK图片`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "jk"
    
    async def _save_html(self, file_name:str) -> bool:
        await super()._save_html(self.api_url, file_name)
    
    async def get_jk_list(self, page:int = 1) -> list:
        '''
        获取jk列表
        
        参数:
        - page: 页数
        
        返回:
        - list: jk列表
        '''
        return await super().get_img_list(page)
    
    async def get_jk_title(self, page:int = 1) -> list:
        '''
        获取jk标题
        
        参数:
        - page: 页数
        
        返回:
        - list: jk标题
        '''
        return await super().get_title_list(page)

    async def get_jk_img(self, url:str) -> list:
        '''
        获取jk图片列表
        
        参数:
        - url: jk链接
        
        返回:
        - list: jk图片列表
        '''
        return await super().get_img_url(url)
