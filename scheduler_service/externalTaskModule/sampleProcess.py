class SampleProcess:
    def __init__(self):
        self.message = 'abc'
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Dọn dẹp tài nguyên.
        """
        self.message = None

    def sampleClassMethod(self) -> str:
        """
        Phương thức samplePropertyMethod.


        Returns:
            str: Thông điệp đã được in.
        """
        # print('abc')
        # print(self.message)
        return 'test'
    
    @property
    def sampleProperty(self):
        return self.message
    
    def sampleMethod(message):
        return message
    
    def sampleClassMethodWithParam(self,message):
        return message
    
    def sampleMethodNoneParam():
        return 'test sampleMethodNoneParam'
    
    def sampleMethodNoneParamClassIns(self):
        print('test sampleMethodNoneParam')
    
    # @property
    # def sampleStatement(self) -> str:
    #     return 'abc'
    
