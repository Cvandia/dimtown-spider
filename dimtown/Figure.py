from .utils import Spider

class Figure(Spider):
    '''
    `手办`图片获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "shouban"
    
    async def get_figure_list(self, page:int = 1) -> list:
        '''
        获取手办列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 手办列表
        '''
        return await super().get_img_list(page)
    
    async def get_figure_title(self, page:int = 1) -> list:
        '''
        获取手办标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 手办标题
        '''
        return await super().get_title_list(page)
    
    async def get_figure_img(self, url:str) -> list:
        '''
        获取手办图片列表
        
        参数:
        - url: 手办链接
        
        返回:
        - list: 手办图片列表
        '''
        return await super().get_img_url(url)
