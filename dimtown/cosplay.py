from .utils import Spider

class CosPlay(Spider):
    '''
    `CosPlay`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "cosplay"
    
    async def _save_html(self, file_name:str) -> bool:
        await super()._save_html(self.api_url, file_name)
    
    async def get_cosplay_list(self, page:int = 1) -> list:
        '''
        获取cosplay列表
        
        参数:
        - page: 页数
        
        返回:
        - list: cosplay列表
        '''
        return await super().get_img_list(page)
    
    async def get_cosplay_title(self, page:int = 1) -> list:
        '''
        获取cosplay标题
        
        参数:
        - page: 页数
        
        返回:
        - list: cosplay标题
        '''
        return await super().get_title_list(page)

    async def get_cosplay_img(self, url:str) -> list:
        '''
        获取cosplay图片列表
        
        参数:
        - url: cosplay链接
        
        返回:
        - list: cosplay图片列表
        '''
        return await super().get_img_url(url)
