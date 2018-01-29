class Value:
    def __get__(self, *args):
        return self.num
    
    def __set__(self, obj, value):
        self.num = (1.0 - obj.commission) * value
