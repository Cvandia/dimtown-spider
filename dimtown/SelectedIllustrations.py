from .utils import Spider

class SelectedIllustrations(Spider):
    '''
    `精选插画`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "jxmt"

    async def _save_html(self, file_name:str) -> bool:
        '''
        保存网页
        
        参数:
        - file_name: 文件名
        
        返回:
        - bool: 是否保存成功
        '''
        await super()._save_html(self.api_url, file_name)

    async def get_selectedillustrations_list(self, page:int = 1) -> list:
        '''
        获取插画列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 插画列表
        '''
        return await super().get_img_list(page)
    
    async def get_selectedillustrations_title(self, page:int = 1) -> list:
        '''
        获取插画标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 插画标题
        '''
        return await super().get_title_list(page)

    async def get_selectedillustrations_img(self, url:str) -> list:
        '''
        获取插画图片列表
        
        参数:
        - url: 插画链接
        
        返回:
        - list: 插画图片列表
        '''
        return await super().get_img_url(url)
