from .AnimeAvatar import AnimeAvatar

class FemaleAvatar(AnimeAvatar):
    '''
    `女生头像`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "lolitx"

    async def get_femaleavatar_list(self, page:int = 1) -> list:
        '''
        获取女生头像列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 女生头像列表
        '''
        return await super().get_img_list(page)
    
    async def get_femaleavatar_title(self, page:int = 1) -> list:
        '''
        获取女生头像标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 女生头像标题'''
        return await super().get_title_list(page)
    
    async def get_femaleavatar_img(self, url:str) -> list:
        '''
        获取女生头像图片列表
        
        参数:
        - url: 女生头像链接
        
        返回:
        - list: 女生头像图片列表'''
        return await super().get_animeavatar_img(url)
    