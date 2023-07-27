from .AnimeAvatar import AnimeAvatar

class CoupleAvatar(AnimeAvatar):
    '''
    `情侣头像`获取
    '''
    def __init__(self) -> None:
        super().__init__()
        self.api_url = self.base_url + "loverstx"
    
    async def get_coupleavatar_list(self, page:int = 1) -> list:
        '''
        获取情侣头像列表
        
        参数:
        - page: 页数
        
        返回:
        - list: 情侣头像列表
        '''
        return await super().get_img_list(page)
    
    async def get_coupleavatar_title(self, page:int = 1) -> list:
        '''
        获取情侣头像标题
        
        参数:
        - page: 页数
        
        返回:
        - list: 情侣头像标题
        '''
        return await super().get_title_list(page)
    
    async def get_coupleavatar_img(self, url:str) -> list:
        return await super().get_animeavatar_img(url)
    