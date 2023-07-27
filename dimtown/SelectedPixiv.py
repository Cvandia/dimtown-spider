from .utils import Spider

class SelectedPixiv(Spider):
    '''
    `精选Pixiv`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "pzmt"
    
    async def _save_html(self, file_name:str) -> bool:
        '''
        保存网页
        
        参数:
        - file_name: 文件名
        
        返回:
        - bool: 是否保存成功
        '''
        await super()._save_html(self.api_url, file_name)
    
    async def get_pixiv_list(self, page:int = 1) -> list:
        '''
        获取pixiv列表
        
        参数:
        - page: 页数
        
        返回:
        - list: pixiv列表
        '''
        return await super().get_img_list(page)
    
    async def get_pixiv_title(self, page:int = 1) -> list:
        '''
        获取pixiv标题
        
        参数:
        - page: 页数
        
        返回:
        - list: pixiv标题
        '''
        return await super().get_title_list(page)

    async def get_pixiv_img(self, url:str) -> list:
        '''
        获取pixiv图片列表
        
        参数:
        - url: pixiv链接
        
        返回:
        - list: pixiv图片列表
        '''
        return await super().get_img_url(url)
