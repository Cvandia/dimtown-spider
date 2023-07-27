from .AnimeAvatar import AnimeAvatar

class MaleAvatar(AnimeAvatar):
    '''
    `男生头像`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "mantx"

    async def get_maleavatar_list(self, page:int = 1) -> list:
        '''
        获取男生头像列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 男生头像列表
        '''
        return await super().get_img_list(page)
    
    async def get_maleavatar_title(self, page:int = 1) -> list:
        '''
        获取男生头像标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 男生头像标题
        '''
        return await super().get_title_list(page)
    
    async def get_maleavatar_img(self, url:str) -> list:
        '''
        获取男生头像图片列表
        
        参数:
        - url: 男生头像链接
        
        返回:
        - list: 男生头像图片列表
        '''
        return await super().get_animeavatar_img(url)
    