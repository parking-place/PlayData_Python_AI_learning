class Gradients:
    grds = None
    
    _instance = None
    def __init__(self):
        import numpy as np
        
        if not Gradients._instance:
            Gradients._instance = self
        # 그라디언트 색상 설정
        self.grds = { None : ('#ff0000','#0000ff') }
        self.load_csv()
        
    @classmethod
    def getinstance(cls):
        if not cls._instance:
            cls._instance = Gradients()
        return cls._instance

    def get_gradient(self, name=None):
        return self.grds[name]
    
    def get_gradient_names(self):
        return list(self.grds.keys())
    
    def get_gradient_dict(self):
        return self.grds
    
    def update_gradient(self, name, start_color, end_color):
        self.grds[name] = (start_color, end_color)
        self.save_csv()
        
    def save_csv(self):
        import pandas as pd
        df = pd.DataFrame(self.grds).T
        df.columns = ['start_color', 'end_color']
        df.index.name = 'name'
        df.to_csv(r'./gradients.csv')
    
    def load_csv(self):
        import pandas as pd
        df = pd.read_csv(r'./gradients.csv')
        # nan to None
        df = df.where(pd.notnull(df), None)
        for i in range(len(df)):
            self.update_gradient(df['name'][i], df['start_color'][i], df['end_color'][i])
            
    def delinstance(self):
        self._instance = None
