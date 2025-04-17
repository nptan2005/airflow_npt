import os
import paramiko
import stat
from . import ConnKitConstant
from core_config import configuration
from utilities import Logger

class SftpConn:
    def __init__(self,connectionName:str = ConnKitConstant.SFTP_CONN_DEFAULT,source_path:str=None, destination_path:str=None):
        if connectionName is None:
            raise ValueError("ConnectionName cannot be None")
        self._connectionName = connectionName

        # get config
        self._config = configuration.sftp[self._connectionName]
        
        self._os_type = ''
        self._logger = Logger('paramiko').logger
        self._logger.setLevel(50)
        try:
            self._transport = paramiko.Transport((self._config.host, self._config.port))
            self._transport.connect(username=self._config.username, password=self._config.password)
            self._sftp_conn = paramiko.SFTPClient.from_transport(self._transport)
            self._os_type = self.detect_remote_os(self._config.host,self._config.port,self._config.username,self._config.password)
        except paramiko.AuthenticationException as e:
            self._logger.exception(f"Authentication {self._connectionName} SFTP is fail: {e}")
            raise
            self._sftp_conn =  None
        except Exception as e:
            self._logger.exception(f"===> Connection {self._connectionName} SFTP is Error: {e}")
            raise
            self._sftp_conn =  None
        # init var
        self._source_path = source_path
        self._destination_path = destination_path
        self._is_successful = False

    def __enter__(self):
        return self
    
    def __del__(self):
        self._clear_attributes()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_sftp_conn', '_connectionName', '_config', '_transport', '_sftp_conn',
            '_source_path','_destination_path','_is_successful','_os_type',
            '_logger'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    
    @property
    def is_successful(self) -> bool:
        return self._is_successful

    @property
    def sftp_conn(self):
        return self._sftp_conn
    
    @property
    def sftp_close(self):
        self._sftp_conn.close()

    @property
    def close(self):
        self._sftp_conn.close()

    def detect_remote_os(self,host: str, port: int, username: str, password: str) -> str:
        """Kiểm tra hệ điều hành của máy chủ SFTP."""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, port, username=username, password=password)
            
            # Chạy lệnh `uname` để xác định hệ điều hành trên server
            stdin, stdout, stderr = ssh.exec_command("uname")
            os_type = stdout.read().decode().strip().lower()
            
            ssh.close()
            
            if 'linux' in os_type:
                return 'linux'
            elif 'windows' in os_type:
                return 'windows'
            else:
                return 'unknown'
        
        except:
            # self._logger.exception(f"Unknow error: {e}")
            return 'unknown'
        
    def adjust_remote_path(self,remote_path: str, os_type: str) -> str:
        """Thay đổi đường dẫn dựa trên hệ điều hành của SFTP server."""
        if os_type == 'windows':
            # Chuyển đổi đường dẫn sang dạng Windows với dấu `\`
            remote_path = remote_path.replace('/', '\\')
        elif os_type in ['linux','unknown']:
            # Chuyển đổi đường dẫn sang dạng Linux với dấu `/`
            remote_path = remote_path.replace('\\', '/')
        return remote_path
    # end adjust_remote_path

    def is_exist_file_in_server(self,path:str) -> bool:
        try:
            self._sftp_conn.stat(path)  # Nếu tệp tồn tại, stat() sẽ không gây lỗi
            return True
        except FileNotFoundError:
            self._logger.info(f'File {path} is not Exist on FTP Server')
            return False
        except Exception as e:
            self._logger.exception(f'Check file is Exist FTP Server is Error: {e}')
            return False
    
    def is_exist_dir_in_server(self,path: str) -> bool:
        """
        Kiểm tra xem thư mục có tồn tại trên SFTP server hay không.
        
        Args:
            sftp_conn (paramiko.SFTPClient): Kết nối SFTP.
            path (str): Đường dẫn thư mục trên SFTP server.
        
        Returns:
            bool: Trả về True nếu thư mục tồn tại, False nếu không tồn tại.
        """
        directory = os.path.dirname(path)
        try:
            
            # Lấy thông tin về đường dẫn
            file_info = self._sftp_conn.stat(directory)
            
            # Kiểm tra xem đường dẫn có phải là thư mục không
            if stat.S_ISDIR(file_info.st_mode):
                return True
            else:
                return False
        except FileNotFoundError:
            # Nếu đường dẫn không tồn tại, trả về False
            self._logger.info(f'Dir {directory} is not Exist on FTP Server')
            return False
        except Exception as e:
            self._logger.exception(f'===> Check Dir is Exist FTP Server is Error: {e}')
            return False
    
    def read_file_from_sftp(self):
        """Đọc file từ máy chủ SFTP."""

        try:
            if self.is_exist_file_in_server(self._source_path):
                with self.sftp_conn.open(self._source_path, "r") as f:
                    content = f.read().decode()  # Đọc file và chuyển đổi sang chuỗi
                    self._is_successful = True
                    return content
            else:
                self._is_successful = False
        except Exception as e:
            self._logger.exception(f"===> Read file {self._source_path} is error: {e}.")
            self._is_successful = False
            return None


    def move_file(self):
        """
        Di chuyển tệp từ vị trí này sang vị trí khác trên SFTP server.

        Args:
            sftp (paramiko.SFTPClient): Đối tượng SFTP client.
            source_path (str): Đường dẫn nguồn của tệp.
            destination_path (str): Đường dẫn đích đến của tệp.


        """
        try:
            self._source_path = self.adjust_remote_path(self._source_path, self._os_type)
            self._destination_path = self.adjust_remote_path(self._destination_path, self._os_type)
            if self.is_exist_file_in_server(self._source_path) and self.is_exist_dir_in_server(self._destination_path):
                self.sftp_conn.rename(self._source_path, self._destination_path)
                self._logger.info(f"===> Move file from '{self._source_path}' to '{self._destination_path}'.")
                self._is_successful = True
            else:
                self._is_successful = False
        except Exception as e:
            self._logger.exception(f"===> Move file from '{self._source_path}' to '{self._destination_path}' is Error: {e}.")
            self._is_successful = False

    def copy_file(self, source_path, destination_path):
        """
        Sao chép tệp từ đường dẫn nguồn sang đường dẫn đích trên SFTP server.

        Args:
            sftp (paramiko.SFTPClient): Đối tượng SFTP client.
            source_path (str): Đường dẫn nguồn của tệp.
            destination_path (str): Đường dẫn đích đến của tệp.

        """
        try:
            self._source_path = self.adjust_remote_path(self._source_path, self._os_type)
            self._destination_path = self.adjust_remote_path(self._destination_path, self._os_type)
            if self.is_exist_file_in_server(self._source_path) and self.is_exist_dir_in_server(self._destination_path):
                # Tải tệp từ SFTP về máy cục bộ
                local_temp_path = os.path.basename(self._source_path)
                self.sftp_conn.get(self._source_path, local_temp_path)

                # Tải tệp từ máy cục bộ lên SFTP
                self.sftp_conn.put(local_temp_path, self._destination_path)

                # Xóa tệp tạm thời trên máy cục bộ
                os.remove(local_temp_path)
                
                
                self._logger.info(f"===> Copy file '{source_path}' to '{destination_path}'.")
                self._is_successful = True
            else:
                self._is_successful = False
        except Exception as e:
            self._logger.exception(f"===> Copy file '{source_path}' to '{destination_path}' is Error: {e}.")
            self._is_successful = False

    def upload_file(self):
        """
        Tải tệp từ máy cục bộ lên SFTP server.

        Args:
            sftp (paramiko.SFTPClient): Đối tượng SFTP client.
            local_path (str): Đường dẫn của tệp trên máy cục bộ.
            remote_path (str): Đường dẫn của tệp trên SFTP server.

        Returns:
            bool: True nếu tải lên thành công, False nếu có lỗi.
        """
        try:
            self._destination_path = self.adjust_remote_path(self._destination_path, self._os_type)
            if not os.path.isfile(self._source_path):
                raise FileNotFoundError(f" ===> File is not exist: {self._source_path}")
            if self.is_exist_dir_in_server(self._destination_path):
                self.sftp_conn.put(self._source_path, self._destination_path)
                self._logger.info(f"===> Upload '{self._source_path}' to '{self._destination_path}'.")
                self._is_successful = True
            else:
                self._is_successful = False
        except Exception as e:
           self._logger.exception(f"===> Upload '{self._source_path}' to '{self._destination_path}' is Error {e}.")
           self._is_successful = False

    def delete_file(self):
        """
        Xóa tệp trên SFTP server.

        Args:
            sftp (paramiko.SFTPClient): Đối tượng SFTP client.
            remote_path (str): Đường dẫn của tệp trên SFTP server.

        """
        try:
            self._source_path = self.adjust_remote_path(self._source_path, self._os_type)
            if self.is_exist_file_in_server(self._source_path):
                self.sftp_conn.remove(self._source_path)
                self._logger.info(f"===> Delete '{self._source_path}' on SFTP server.")
                self._is_successful = True
            else:
                self._is_successful = True
        except Exception as e:
            self._logger.exception(f"===> Delete '{self._source_path}' on SFTP server is Error: {e}.")
            self._is_successful = False

    def download_file(self,is_delete_src:bool = False):
        """
        Tải tệp từ SFTP server về máy cục bộ.

        Args:
            sftp (paramiko.SFTPClient): Đối tượng SFTP client.
            remote_path (str): Đường dẫn của tệp trên SFTP server.
            local_path (str): Đường dẫn của tệp trên máy cục bộ.


        """
        try:
            self._source_path = self.adjust_remote_path(self._source_path, self._os_type)
            if self.is_exist_file_in_server(self._source_path):
                self.sftp_conn.get(self._source_path, self._destination_path)
                self._logger.info(f"Download '{self._source_path}' to '{self._destination_path}'.")
                self._is_successful = True
                if is_delete_src:
                    self.delete_file()
            
        except Exception as e:
            self._logger.exception(f"===> Download '{self._source_path}' to '{self._destination_path}' is Error: {e}")
            self._is_successful = False

   



