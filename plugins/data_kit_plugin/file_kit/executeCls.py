import importlib
import inspect
"""
    Ex:

                    use case test 1
                        with ExecuteCls(
                                classExecuteName="externalTaskModule.sampleProcess", doTask="sampleMethod"
                            ) as e:
                            print(e.do_it('test'))

                    use case test 2
                        with ExecuteCls(
                                classExecuteName="externalTaskModule.sampleProcess", doTask="sampleMethodNoneParam"
                            ) as e:
                            print(e.do_it_no_param)

                    use case test 3
                        #  Thực thi phương thức samplePropertyMethod
                        with ExecuteCls(
                            classExecuteName="externalTaskModule.sampleProcess", doTask="sampleClassMethod"
                        ) as e:
                            # Gọi phương thức do_cls_method() để lấy đối tượng method
                            method = e.do_cls_method  # Lấy đối tượng method
                            # Gọi phương thức doItWithPropertyMethod() để lấy đối tượng method
                            result = method  # Gọi phương thức method
                            print(f"Kết quả: {result}") 
                            print(e.logNote)

                    use case test 4
                        with ExecuteCls(
                            classExecuteName="externalTaskModule.sampleProcess", doTask="sampleClassMethod"
                        ) as e:

                            print(e.do_cls_method('abc'))
                            print(e.logNote)
                    use case test 5
                        with ExecuteCls(
                            classExecuteName="externalTaskModule.sampleProcess", doTask="sampleMethodNoneParamClassIns"
                        ) as e:

                            print(e.doItNoneParamWithClassIntance)
                            print(e.log_note)
                    use case test 6

                        #  Thực thi phương thức samplePropertyMethod
                        with ExecuteCls(
                            classExecuteName="externalTaskModule.sampleProcess", doTask="sampleProperty"
                        ) as e:
                            # Gọi phương thức do_cls_property() để lấy đối tượng method
                            method = e.do_cls_property  # Lấy đối tượng method
                            # Gọi phương thức do_cls_property() để lấy đối tượng method
                            # result = method  # Gọi phương thức method
                            print(f"Kết quả: {method}") 
                            print(e.log_note)

                    use case test 7

                        #  Thực thi phương thức sampleClassMethodWithParam
                        with ExecuteCls(
                            classExecuteName="externalTaskModule.sampleProcess", doTask="sampleClassMethodWithParam"
                        ) as e:
                            # Gọi phương thức do_cls_method() để lấy đối tượng method
                            method = e.do_cls_method('tan text')  # Lấy đối tượng method
                            # Gọi phương thức do_cls_method() để lấy đối tượng method
                            # result = method  # Gọi phương thức method
                            print(f"Kết quả: {method}") 
                            print(e.log_note)
"""

class ExecuteCls:
    """
    Class  executeCls dynamic execute other python class.
    """

    def __init__(self, classExecuteName: str, doTask: str):
        """
        init executeTask.

        Args:
            classExecuteName (str): name of Class: EX: moduel.my_class.
            doTask (str): method name, which need execute in your class.
        """
        self.classExecuteName = classExecuteName
        self.doTask = doTask
        self.module = None
        self.classObj = None
        self.instance = None
        self.method = None
        self._logNote = ''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        cleanup.
        """
        self.module = None
        self.classObj = None
        self.method = None
        self._logNote = None
        self.instance = None

    @property
    def log_note(self):
         return self._logNote


    def importDynamicClass(self, className):
        module = importlib.import_module(className)
        className = className.split(".")[1]
        return getattr(module, className)

    def do_cls_method(self, *args, **kwargs):
        """
        doItWithClassInstance
        Execute func/method. 
        instant of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.instance = self.classObj()  # Create an instance of the class
            self.method = getattr(self.instance,  self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method(*args, **kwargs)

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"

    def do_it(self, *args, **kwargs):
        """
        Execute func/method. 
        not instance of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.method = getattr(self.classObj, self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method(*args, **kwargs)

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"

    @property
    def do_cls_inst_no_param(self):
        """
        do It None Param With Class Instance
        Execute func/method.
        Instance of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.instance = self.classObj()  # Create an instance of the class
            self.method = getattr(self.instance,  self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method()

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"

    @property
    def do_it_no_param(self):
        """
        Execute func/method.
        not instant of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.method = getattr(self.classObj, self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method()

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"

    

    @property
    def do_cls_method(self):
        """
        Execute func/method.
        Instance of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.instance = self.classObj()  # Create an instance of the class
            self.method = getattr(self.instance,  self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method()

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"

    @property
    def do_cls_property(self):
        """
        Execute func/method.
        Instance of class
        """
        try:
            self.classObj = self.importDynamicClass(self.classExecuteName)
            # print(self.classObj)
            # print(self.doTask)
            self.instance = self.classObj()  # Create an instance of the class
            self.method = getattr(self.instance,  self.doTask, None)
            # print(self.method)

            if self.method is None:
                raise ValueError(f"Method {self.doTask} is not define.")
            return self.method

        except Exception as e:
                self._logNote += f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error when execute {self.doTask}: {e}"



