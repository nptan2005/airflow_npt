import os
import smtplib
import ssl
import uuid
import inspect
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import pandas as pd

import pretty_html_table

from . import ConnKitConstant
from core_config import configuration
from utilities import Logger

# from IPython.display import HTML, display

class EmailSender:
    def __init__(self, connection_name:str = ConnKitConstant.EMAIL_ACCT_DEFAULT,email_template:str = ConnKitConstant.EMAIL_TEMPLATE_DEFAULT):
        if not connection_name or not email_template:
            raise ValueError("ConnectionName and emailTemplate cannot be None")

        # Get configuration
        self._config = configuration.email[connection_name]

        self._host = self._config.host
        self._port = self._config.port
        self._email = self._config.email
        self._password = self._config.password
        self._isSSL = self._config.is_ssl
        self._isDebug = self._config.is_debug
        self._password_authen = self._config.password_authen
        self._data = {}  # Biến lưu trữ dữ liệu tạm thời
        
        self._imgTypeRange = ['png', 'jpge', 'gif']

        self._template = configuration.file_path[email_template].file_content
        self._cc = None
        self._bcc = None
        self._data_report = []
        self._attachment = None
        self._chart_img = None
        self._header = None

        # for log
        self._note = ''
        self.logger = Logger().logger

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._clear_attributes()
    def __del__(self):
        self._clear_attributes() 

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_config', '_host', '_port', '_email', '_password',
            '_isDebug', '_data', '_note', '_imgTypeRange', '_template',
            '_cc', '_bcc', '_data_report', '_attachment',
            '_chart_img','_header','logger',
            '_password_authen'
            ]
        for attr in attributes:
            setattr(self, attr, None)

    @property
    def cc(self):
        return self._cc 
    @cc.setter
    def cc(self,value):
        self._cc = value
    @property
    def bcc(self):
        return self._bcc
    @bcc.setter
    def bcc(self,value):
        self._bcc = value
    @property
    def data_report(self):
        return self._data_report
    @data_report.setter
    def data_report(self,value):
        self._data_report = value
    @property
    def attachment(self):
        return self._attachment
    @attachment.setter
    def attachment(self,value):
        self._attachment = value
    @property 
    def chart_img(self):
        return self._chart_img
    @chart_img.setter
    def chart_img(self,value):
        self._chart_img = value
    @property
    def header(self):
        return self._header
    @header.setter
    def header(self,value):
        self._header = value


    @property
    def note(self):
        return self._note

    def _plain_text_content(self, textMessage):
        # return f"</br></br><p style='color:#022C49; font-size: 9pt;margin:0in;margin-bottom:.0001pt;line-height:normal;'><i>{textMessage}</i></p>" if textMessage else ''
        return textMessage


    def _grid_content(self, df_arr):
        if not df_arr:  # Kiểm tra xem danh sách có trống không
            return ''
        
        grid_content = ''
        for df in df_arr:
            if df is not None and isinstance(df, pd.DataFrame):  # Kiểm tra xem đối tượng có phải là DataFrame không
                if not df.empty:  # Kiểm tra DataFrame có trống không
                    grid_content += pretty_html_table.build_table(df, 'green_light')
        
        return grid_content
    # end girdContent

    
    def _image_attachment(self, chart_img, embed_id):
        return f"</br></br><p style='position:fixed;color:#022C49; font-size: 9pt;margin:0in;margin-bottom:.0001pt;line-height:normal;'><img style='max-width: 600px;position:fixed;' alt='Chart' src='cid:{embed_id}' /></br></p>" if chart_img else ''
    # end imageAttachment

    
    def _check_attachment_email(self, attach_file):
        if not attach_file:
            return False, None
        
        path = Path(attach_file)
        if path.is_absolute() or path.parent != Path('.'):
            attact_file_path = path
        else:
            default_path = os.path.join(
                configuration.file_path[ConnKitConstant.EMAIL_ATTACH_PATH].root,
                configuration.file_path[ConnKitConstant.EMAIL_ATTACH_PATH].path
            )
            attact_file_path = Path(default_path) / path
        
        if attact_file_path.exists():
            return True, attact_file_path
        else:
            self.logger.info(f'Attachment file does not exist: {attact_file_path}')
            return False, None
    
    def _read_file(self, file_path, mode='rb'):
        try:
            with open(file_path, mode) as f:
                return f.read()
        except FileNotFoundError as f:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]File not found: {file_path}'
            self.logger.exception(f'File not found: {file_path}, {f}')
            return None
        except IOError as e:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Error reading file {file_path}'
            self.logger.exception(f'Error reading file {file_path}: {e}')
            return None
        
    def _build_body(self, textMessage):
        html = self._template
        report_grid = self._grid_content(self.data_report) if self.data_report else ''
        id_img = uuid.uuid1()
        chart_content = self._image_attachment(self.chart_img, id_img) if self.chart_img else ''
        
        body = html.format(
            title='Report',
            header='' if not self.header else self.header,
            body=report_grid,
            textMessage=textMessage if textMessage else '',
            chartImg=chart_content
        )
        
        return body, id_img

    def _build_msg(self, subject, receivers, text_message):

        body,id_img = self._build_body(text_message)

        is_attachment_file, self.attachment = self._check_attachment_email(self.attachment)
        is_chart_file, self.chart_img = self._check_attachment_email(self.chart_img)

        # msg = MIMEMultipart('alternative') if not (is_attachment_file or is_chart_file) else MIMEMultipart()
        msg = MIMEMultipart()
        msg['From'] = self._email
        msg['To'] = ', '.join(receivers)
        if self.cc:
            msg['Cc'] = ', '.join(self.cc)
            receivers += self.cc
        if self.bcc:
            receivers += self.bcc
        msg['Subject'] = subject


        content = MIMEText(body, 'html')
        # contentplain_text = MIMEText( text_message if text_message else '' , 'plain')
        msg.attach(content)
        # msg.attach(contentplain_text)

        if is_attachment_file and self.attachment:
            # set attachment mime and file name, the image type is png
            file_attacht_binary = self._read_file(self.attachment)
            attachMime = MIMEBase('application', 'octet-stream')
            attachMime.set_payload(file_attacht_binary)
            # encode with base64
            encoders.encode_base64(attachMime)
            attachMime.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(self.attachment)}')
            msg.attach(attachMime)
        # end attachement

        if is_chart_file and self.chart_img:
            # set attachment mime and file name, the image type is png
            file_path = str(self.chart_img)
            file_type = file_path.split('.')[-1]
            if file_type in self._imgTypeRange:
                file_img_binary = self._read_file(self.chart_img)
                imgMime = MIMEImage(file_img_binary)
                imgMime.add_header('Content-ID', '<{id_img}>')
                msg.attach(imgMime) 
        # end img 
        # end isAttachment


        
        
        return msg
    # end build_msg

    def send(self, subject, receivers, textMessage):
        msg = self._build_msg(subject, receivers, textMessage)
        try:
            if self._password_authen == False:
                with smtplib.SMTP(self._host, self._port) as server:
                    server.send_message(msg)
                    server.quit()
            elif self._isSSL == True:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self._host, self._port, context = context) as server:
                    server.login(self._email, self._password)
                    server.set_debuglevel(self._isDebug)
                    server.sendmail(self._email, receivers, msg.as_string())
                    server.quit()
            else:
                with smtplib.SMTP(self._host, self._port) as server:
                    server.login(self._email, self._password)
                    server.set_debuglevel(self._isDebug)
                    server.sendmail(self._email, receivers, msg.as_string())
                    server.quit()
        except Exception as e:
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}]Send email is Error'
            self.logger.exception(f'Send email is Error = {e}')