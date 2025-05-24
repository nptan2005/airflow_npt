import os
import smtplib
import ssl
import uuid
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional, Dict, Union, Any
import pandas as pd
import pretty_html_table

from airflow.utils.session import provide_session
from sqlalchemy.orm import Session

# Giả sử models.py và email_service.py nằm cùng cấp trong plugin
from email_template_manager_plugin.models import DBEmailTemplate

# Import cấu hình email connection từ Airflow (thay vì core_config của bạn trực tiếp)
# Điều này giúp plugin độc lập hơn và sử dụng cách quản lý connection của Airflow.
from airflow.hooks.base import BaseHook
from pydantic import BaseModel, EmailStr, field_validator, Field


# Pydantic model cho cấu hình SMTP (để parse extra từ Airflow connection)
class SmtpConfig(BaseModel):
    host: str
    port: int
    login: Optional[str] = None  # Tên đăng nhập (email)
    password: Optional[str] = None  # Mật khẩu
    use_ssl: bool = Field(default=False)
    use_tls: bool = Field(
        default=False
    )  # Thường thì SSL và TLS không dùng cùng lúc, SSL ngầm, TLS tường minh
    # password_authen: bool = Field(default=True) # Mặc định là cần xác thực nếu có login/pass
    # is_debug: bool = Field(default=False) # Không dùng trực tiếp từ đây

    @field_validator("use_ssl", "use_tls", mode="before")
    def parse_bool_str(cls, v):
        if isinstance(v, str):
            return v.lower() in ["true", "1", "yes", "t"]
        return bool(v)


class EmailTemplateSender:
    def __init__(self, airflow_smtp_conn_id: str, logger=None):
        self.airflow_smtp_conn_id = airflow_smtp_conn_id
        self.smtp_config: Optional[SmtpConfig] = self._load_smtp_config()

        self.logger = logger if logger else self._get_default_logger()
        self._note = ""
        self._img_type_range = ["png", "jpeg", "jpg", "gif"]  # Thêm jpeg, jpg

        # Các thuộc tính có thể set sau
        self.cc_recipients: List[EmailStr] = []
        self.bcc_recipients: List[EmailStr] = []
        self.data_frames_for_report: List[pd.DataFrame] = []
        self.attachment_paths: List[str] = []  # Danh sách đường dẫn file đính kèm
        self.chart_image_path: Optional[str] = (
            None  # Đường dẫn đến file ảnh chart (nếu có)
        )
        self.custom_header_text: Optional[str] = None  # Text cho phần header của email

    def _get_default_logger(self):
        # Tạo một logger đơn giản nếu không được cung cấp
        import logging

        logger = logging.getLogger(f"EmailTemplateSender_{self.airflow_smtp_conn_id}")
        if not logger.handlers:  # Tránh thêm handler nhiều lần
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def _load_smtp_config(self) -> Optional[SmtpConfig]:
        try:
            conn = BaseHook.get_connection(self.airflow_smtp_conn_id)
            # Airflow lưu trữ host, port, login, password trực tiếp.
            # Các cờ SSL/TLS thường nằm trong 'extra'.
            extra_options = conn.extra_dejson if conn.extra else {}

            config_data = {
                "host": conn.host,
                "port": conn.port,
                "login": conn.login or None,  # conn.login có thể là None
                "password": conn.password or None,  # conn.password có thể là None
                "use_ssl": extra_options.get(
                    "use_ssl", extra_options.get("ssl", False)
                ),  # Kiểm tra cả 'ssl'
                "use_tls": extra_options.get(
                    "use_tls", extra_options.get("tls", False)
                ),
            }
            return SmtpConfig(**config_data)
        except Exception as e:
            self.logger.error(
                f"Lỗi khi tải cấu hình SMTP từ Airflow connection '{self.airflow_smtp_conn_id}': {e}"
            )
            return None

    @provide_session
    def _get_template_from_db(
        self, template_name: str, session: Session = None
    ) -> Optional[DBEmailTemplate]:
        try:
            template = (
                session.query(DBEmailTemplate)
                .filter_by(template_name=template_name)
                .first()
            )
            if not template:
                self._note += (
                    f"Không tìm thấy email template '{template_name}' trong CSDL. "
                )
                self.logger.warning(
                    f"Không tìm thấy email template '{template_name}' trong CSDL."
                )
            return template
        except Exception as e:
            self._note += f"Lỗi khi truy vấn email template '{template_name}': {e}. "
            self.logger.error(
                f"Lỗi khi truy vấn email template '{template_name}': {e}", exc_info=True
            )
            return None

    def _render_template(self, html_template_str: str, context: Dict[str, Any]) -> str:
        """Render template với context. Hiện tại dùng str.format đơn giản."""
        # Bạn có thể thay thế bằng Jinja2 nếu cần logic phức tạp hơn
        # from jinja2 import Environment, select_autoescape
        # env = Environment(autoescape=select_autoescape(['html', 'xml']))
        # template = env.from_string(html_template_str)
        # return template.render(**context)

        # Thêm các giá trị mặc định vào context để tránh KeyError nếu placeholder thiếu
        default_context = {
            "title": context.get("subject", "Thông báo"),  # Lấy title từ subject nếu có
            "header": self.custom_header_text or "",
            "body": "",  # Sẽ được điền bởi _grid_content
            "textMessage": "",  # Sẽ được điền bởi text_message
            "chartImg": "",  # Sẽ được điền bởi _image_attachment
        }
        # Ghi đè các giá trị mặc định bằng context được truyền vào
        final_context = {**default_context, **context}

        return html_template_str.format(**final_context)

    def _grid_content(self) -> str:
        if not self.data_frames_for_report:
            return ""
        grid_html = ""
        for df in self.data_frames_for_report:
            if isinstance(df, pd.DataFrame) and not df.empty:
                grid_html += pretty_html_table.build_table(
                    df, "green_light"
                )  # Hoặc style khác
        return grid_html

    def _image_attachment_html(self, embed_id: str) -> str:
        return (
            f"<br><p><img style='max-width: 800px;' alt='Chart' src='cid:{embed_id}' /></p>"
            if self.chart_image_path
            else ""
        )

    def _build_mime_message(
        self,
        subject: str,
        to_recipients: List[EmailStr],
        html_body_rendered: str,
        embed_id_for_chart: str,
    ) -> MIMEMultipart:
        msg = MIMEMultipart("related")  # 'related' cho HTML và ảnh inline
        msg["From"] = (
            self.smtp_config.login if self.smtp_config else "unknown_sender@example.com"
        )
        msg["To"] = ", ".join(to_recipients)
        if self.cc_recipients:
            msg["Cc"] = ", ".join(self.cc_recipients)
        # BCC được xử lý ở tầng SMTP, không thêm vào header
        msg["Subject"] = subject

        msg_alternative = MIMEMultipart("alternative")
        # msg_alternative.attach(MIMEText("Vui lòng xem email này bằng trình duyệt hỗ trợ HTML.", 'plain')) # Fallback text
        msg_alternative.attach(MIMEText(html_body_rendered, "html", _charset="utf-8"))
        msg.attach(msg_alternative)

        # Đính kèm chart (nếu có)
        if self.chart_image_path:
            try:
                with open(self.chart_image_path, "rb") as fp:
                    img_data = fp.read()
                img_mime = MIMEImage(
                    img_data, name=os.path.basename(self.chart_image_path)
                )
                img_mime.add_header("Content-ID", f"<{embed_id_for_chart}>")
                img_mime.add_header(
                    "Content-Disposition",
                    "inline",
                    filename=os.path.basename(self.chart_image_path),
                )
                msg.attach(img_mime)
            except Exception as e:
                self._note += f"Lỗi khi đính kèm chart '{self.chart_image_path}': {e}. "
                self.logger.error(
                    f"Lỗi khi đính kèm chart '{self.chart_image_path}': {e}",
                    exc_info=True,
                )

        # Đính kèm các file khác
        for file_path_str in self.attachment_paths:
            try:
                path = Path(file_path_str)
                if path.is_file():
                    with open(path, "rb") as fp:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(fp.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition", f'attachment; filename="{path.name}"'
                    )
                    msg.attach(part)
                else:
                    self._note += f"File đính kèm không tồn tại: {file_path_str}. "
                    self.logger.warning(f"File đính kèm không tồn tại: {file_path_str}")
            except Exception as e:
                self._note += f"Lỗi khi đính kèm file '{file_path_str}': {e}. "
                self.logger.error(
                    f"Lỗi khi đính kèm file '{file_path_str}': {e}", exc_info=True
                )

        return msg

    def send_email_with_template(
        self,
        template_name: str,
        to_recipients: Union[List[EmailStr], EmailStr],
        context: Optional[Dict[str, Any]] = None,  # Dữ liệu để render vào template
        override_subject: Optional[str] = None,
    ) -> bool:
        self._note = ""  # Reset note cho mỗi lần gửi
        if not self.smtp_config:
            self._note = "Cấu hình SMTP không hợp lệ hoặc không tải được."
            self.logger.error(self._note)
            return False

        db_template = self._get_template_from_db(template_name)
        if not db_template:
            return False  # Lỗi đã được ghi nhận trong _get_template_from_db

        final_subject = override_subject if override_subject else db_template.subject

        # Chuẩn bị context để render
        render_context = context if context else {}
        render_context.setdefault(
            "subject", final_subject
        )  # Đảm bảo subject có trong context
        render_context.setdefault(
            "textMessage", render_context.get("text_message", "")
        )  # Cho textMessage

        # Render các phần của email
        grid_html = self._grid_content()
        chart_embed_id = str(uuid.uuid4())  # ID duy nhất cho chart image
        chart_html = self._image_attachment_html(chart_embed_id)

        # Thêm vào context để render vào template chính
        render_context["body"] = grid_html
        render_context["chartImg"] = chart_html

        try:
            rendered_html_body = self._render_template(
                db_template.body_html, render_context
            )
        except Exception as e:
            self._note += f"Lỗi khi render email template '{template_name}': {e}. "
            self.logger.error(
                f"Lỗi khi render email template '{template_name}': {e}", exc_info=True
            )
            return False

        if isinstance(to_recipients, str):
            to_recipients_list = [EmailStr(to_recipients)]
        elif isinstance(to_recipients, list):
            to_recipients_list = [EmailStr(r) for r in to_recipients]
        else:
            self._note = "Định dạng người nhận không hợp lệ."
            self.logger.error(self._note)
            return False

        all_recipients = list(
            set(to_recipients_list + self.cc_recipients + self.bcc_recipients)
        )
        if not all_recipients:
            self._note = "Không có người nhận nào được chỉ định."
            self.logger.error(self._note)
            return False

        mime_message = self._build_mime_message(
            final_subject, to_recipients_list, rendered_html_body, chart_embed_id
        )

        try:
            server: Optional[smtplib.SMTP] = None
            if self.smtp_config.use_ssl:
                context_ssl = ssl.create_default_context()
                server = smtplib.SMTP_SSL(
                    self.smtp_config.host, self.smtp_config.port, context=context_ssl
                )
            else:
                server = smtplib.SMTP(self.smtp_config.host, self.smtp_config.port)
                if self.smtp_config.use_tls:  # TLS tường minh sau khi kết nối
                    server.starttls(context=ssl.create_default_context())

            if self.smtp_config.login and self.smtp_config.password:
                server.login(self.smtp_config.login, self.smtp_config.password)

            # server.set_debuglevel(1 if self.smtp_config.is_debug else 0) # is_debug không có trong SmtpConfig
            server.sendmail(
                self.smtp_config.login or "fallback_sender@example.com",
                all_recipients,
                mime_message.as_string(),
            )
            server.quit()
            self._note = f"Email '{final_subject}' gửi thành công đến {', '.join(all_recipients)}."
            self.logger.info(self._note)
            return True
        except Exception as e:
            self._note += f"Lỗi khi gửi email: {e}. "
            self.logger.error(f"Lỗi khi gửi email: {e}", exc_info=True)
            return False
        finally:
            # Reset các thuộc tính có thể thay đổi cho lần gửi tiếp theo
            self.cc_recipients = []
            self.bcc_recipients = []
            self.data_frames_for_report = []
            self.attachment_paths = []
            self.chart_image_path = None
            self.custom_header_text = None

    @property
    def last_operation_note(self) -> str:
        return self._note
