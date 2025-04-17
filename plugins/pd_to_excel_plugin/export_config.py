import yaml

class ExportConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = None

    def load_config(self):
        """Load YAML configuration file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as file:
                self.config_data = yaml.safe_load(file)
                return self.config_data
        except Exception as e:
            raise Exception(f"Lỗi khi đọc file config: {e}")

    def get_template(self, template_name):
        """Lấy cấu hình template theo tên."""
        if not self.config_data:
            self.load_config()
        template = self.config_data.get('export_template', {}).get(template_name, None)
        if not template:
            raise Exception(f"Template '{template_name}' không tồn tại trong file config.")
        return template
