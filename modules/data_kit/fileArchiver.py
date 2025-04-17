import os
from datetime import datetime
import shutil
import inspect


class FileArchiver:
    def __init__(self, source:str, destination:str):
        """"""
        self._source = source
        self._destination = destination
        self._note = ''
    
    def __enter__(self):
        return self
    
    def __del__(self):
        """"""
        del self._source
        del self._destination
        del self._note

    def __exit__(self, exc_type, exc_val, exc_tb):
        """"""
        self._source = None
        self._destination = None
        self._note = None
    
    @property
    def note(self):
        return self._note
    
    def _move_and_rename_file(self,source_path: str, destination_file_path: str):
        """
        Di chuyển và đổi tên file.

        Args:
            source_path (str): Đường dẫn đến file nguồn.
            destination_path (str): Đường dẫn đến thư mục đích.
        """

        # Kiểm tra xem file nguồn có tồn tại hay không
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"File don't exist: {source_path}")

        # Di chuyển và đổi tên file
        try:
            shutil.move(source_path, destination_file_path)
            # print(f"File move is ok!!: {destination_file_path}")
        except Exception as e:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] error: {e}'
            raise e
    # end move_and_rename_fil

    @property
    def archive_file(self) -> str:
        """
        sucessful return None
        """
        current_date = datetime.now().strftime("%Y%m%d")
        destination = self._destination
        if not os.path.isfile(self._source):
            return f"File '{self._source}' is not exist"
        try:
            if not os.path.exists(destination):
                os.makedirs(destination)
            
            # new destination 
            destination = os.path.join(destination,current_date)

            # check and create new destination folder
            if not os.path.exists(destination):
                os.makedirs(destination)


        except Exception as e:
            self._note = f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] process error {e}'
            return f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}][Archive] Check - init destination = '{destination}' is Error='{e}'"
        
        file_name = os.path.basename(self._source)
        file_base, file_ext = os.path.splitext(file_name)

        # archive file
        archived_file_name = f"{file_base}{file_ext}"
        archived_file_path = os.path.join(destination, archived_file_name)

        # move file
        try:
            self._move_and_rename_file(self._source, archived_file_path)
        except Exception as e:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] process error {e}'
            return f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Archive file '{self._source}' to '{archived_file_path}' is Error={e}"
        
        return None
    # end archiveFile

    @property
    def archiveFolder(self) -> str:
        """
        sucessful return None
        """
        if not os.path.isfile(self._source):
            return f"File '{self._source}' is not exist"
        
        try:
            if not os.path.exists(self._destination):
                os.makedirs(self._destination)

            self._move_and_rename_file(self._source, self._destination)

        except Exception as e:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Process error: {e}'
            return f"[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Archive folder '{self._source}' to '{self._destination}' is Error = {e}"
        
        return None
    # end archiveFolder


    