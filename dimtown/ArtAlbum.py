from .utils import Spider

class ArtAlbum(Spider):
    '''
    `画册`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "tujihuace"

    async def _save_html(self, file_name:str) -> bool:
        await super()._save_html(self.api_url, file_name)

    async def get_artalbum_list(self, page:int = 1) -> list:
        '''
        获取画册列表
        
        参数:
        - page: 页数

        返回:
        - list: 画册列表
        '''
        return await super().get_img_list(page)
    
    async def get_artalbum_title(self, page:int = 1) -> list:
        '''
        获取画册标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 画册标题
        '''
        return await super().get_title_list(page)

    async def get_artalbum_img(self, url:str) -> list:
        '''
        获取画册图片列表
        
        参数:
        - url: 画册链接
        
        返回:
        - list: 画册图片列表'''
        return await super().get_img_url(url)