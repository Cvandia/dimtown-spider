from .utils import Spider

class HanFu(Spider):
    '''
    `汉服`图片获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "hanfu"
    
    async def _save_html(self, file_name:str) -> bool:
        await super()._save_html(self.api_url, file_name)

    async def get_hanfu_list(self, page:int = 1) -> list:
        '''
        获取汉服列表

        参数:
        - page: 页数

        返回:
        - list: 汉服列表
        '''
        return await super().get_img_list(page)
    
    async def get_hanfu_title(self, page:int = 1) -> list:
        '''
        获取汉服标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 汉服标题
        '''
        return await super().get_title_list(page)
    
    async def get_hanfu_img(self, url:str) -> list:
        '''
        获取汉服图片列表
        
        参数:
        - url: 汉服链接
        
        返回:
        - list: 汉服图片列表
        '''
        return await super().get_img_url(url)
    