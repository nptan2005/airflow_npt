import pandas as pd
import xlsxwriter
import openpyxl
from openpyxl.styles import Font, Alignment
from typing import Optional,Dict,List,Tuple
import inspect
from .dataConstant import DataConstant
from core_config import export_configuration
from utilities import Logger


class DataExport:
    def __init__(self,export_data,
                 export_name,
                 file_name, 
                 template:str,
                 file_extension:str = 'xlsx'):
        if template:
            self._template = export_configuration.export_template[template]
            self._file_type = self._template.file_extension
        else:
            self._template = export_configuration.export_template[DataConstant.DEFAULT]
            self._file_type = file_extension

        self._file_name = file_name
        self._sep = self._template.separate
        self._export_data = export_data
        self._export_name = export_name
        self._is_successful = False
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
            '_file_name', '_file_type',  '_sep', '_export_data',
            '_export_name','_is_successful','_note',
            "_template",'logger'
        ]
        for attr in attributes:
            setattr(self, attr, None)

    def get_sheet_config(self,key):
        return self._template.sheets.get(key)
    
    def get_sheet_name(self, key):
        sheet_config = self.get_sheet_config(key)
        return getattr(sheet_config, 'sheet_name', key)
    
    def get_sheet_title_name(self, key):
        sheet_config = self.get_sheet_config(key)
        return getattr(sheet_config, 'sheet_title_name', None)
    
    def get_sheet_is_header(self, key):
        sheet_config = self.get_sheet_config(key)
        return getattr(sheet_config, 'is_header', True)
    
    def get_sheet_is_format(self, key):
        sheet_config = self.get_sheet_config(key)
        return getattr(sheet_config, 'is_format', False)
    
    def _apply_header_config(self, df: pd.DataFrame, header_config: Optional[Dict[str, str]]) -> pd.DataFrame:
        if header_config and isinstance(header_config, dict):
            rename_dict = {col: header_config.get(col, col) for col in df.columns}
            df = df.rename(columns=rename_dict)
        return df
    # end _apply_header_config

    def _data_export_dict(self) -> Dict[str,pd.DataFrame]:
        # df_config = self._export_data.copy()
        data_dict =  {}
        for key in self._export_name:
            try:
                config = self.get_sheet_config(key)
                if config:
                    index = self._export_name.index(key)

                    if 0 <= index < len(self._export_data):
                        df = self._export_data[index]

                        # Apply header mapping
                        if config.column_mapping:
                            df = self._apply_header_config(df, config.column_mapping)
                        self._export_data[index] = df
                        
                        data_dict[key] = df


            except Exception as e:
                self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Transform data for key {key} encountered an error'
                self.logger.exception(f'Transform data for key {key} encountered an error, {e}')
        
        return data_dict
    # end _data_export_dict

    @property
    def export_data(self):
        return self._export_data

    @property
    def export_name(self):
        return self._export_name

    @property
    def file_type(self):
        return self._file_type

    @property
    def file_name(self):
        return self._file_name
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self,value):
        self._title = value


    @property
    def is_successful(self) -> bool:
        return self._is_successful

    @property
    def note(self):
        return self._note.strip()

    def _export_to_excel(self):
        if not self.export_data or (len(self.export_data) == 1 and self.export_data[0].shape[0] == 0):
            self.logger.info(f'==> Data empty, Rows of Data = 0 => Not Export Empty file')
            self._is_successful = True
            return
        
        if len(self.export_data) > 1 and (not self.export_name or len(self.export_data) != len(self.export_name)):
            self.logger.info(f'==> Config incorrect - Sheet Array None or not map Data => Not Export Empty file')
            return
        export_data_dict = self._data_export_dict()
        try:
            file_name = f"{self.file_name}.{self.file_type}"
            with pd.ExcelWriter(file_name, engine='xlsxwriter', datetime_format='dd/mm/yyyy hh:mm:ss', date_format='dd/mm/yyyy') as writer:
                for key in self._export_name:
                    df = export_data_dict.get(key)
                    if df is None:
                        self.logger.info(f'==> Sheet Name [{key}] not found in data dictionary.')
                        continue
                    if df.shape[0] > 0 and df.shape[1] > 0:
                        sheet_name = self.get_sheet_name(key)
                        if not sheet_name:
                            self.logger.info(f'==> Sheet name for key [{key}] is None, skipping sheet.')
                            continue
                        sheet_title_name = self.get_sheet_title_name(key)
                        start_row = 0
                        freeze = 1
                        if sheet_title_name is not None and sheet_title_name != '':
                            start_row = 1
                            freeze += start_row

                        
                        df.to_excel(writer, sheet_name=sheet_name,startrow=start_row, index=False)
                        workbook  = writer.book
                        worksheet = writer.sheets[sheet_name]
                        worksheet.freeze_panes(freeze, 1)

                        # start format excel
                        if sheet_title_name is not None and sheet_title_name != '':
                            title_format = workbook.add_format({
                                'bold': True,
                                'font_size': 13,
                                'align': 'center',
                                'valign': 'vcenter',
                                'fg_color': '#c1e8c1',  
                                'font_color': '#0b3601'   
                            })
                            worksheet.merge_range(0, 0, 0, len(df.columns)-1, sheet_title_name, title_format)
                        is_header = self.get_sheet_is_header(key)
                        if is_header:
                            # format header
                            header_format = workbook.add_format({
                                'bold': True,
                                'font_size': 12,
                                'text_wrap': True,
                                'valign': 'center',
                                'fg_color': '#E0F7E0',  
                                'font_color': '#0b3601',  
                                'border': 1
                            })
                            # Ghi tiêu đề các cột vào file Excel
                            for col_num, value in enumerate(df.columns):
                                worksheet.write(start_row, col_num, value, header_format)
                        # end header format
                        is_format = self.get_sheet_is_format(key)
                        if is_format:
                        # # format row
                            even_row_format = workbook.add_format({'bg_color': '#FFFFFF','border': 1,'font_size': 11}) 
                            odd_row_format = workbook.add_format({'bg_color': '#d4fcf5','border': 1,'font_size': 11}) 
                            
                            even_date_format = workbook.add_format({'num_format': 'dd/mm/yyyy','bg_color': '#FFFFFF','font_size': 11, 'border': 1})
                            odd_date_format = workbook.add_format({'num_format': 'dd/mm/yyyy','bg_color': '#d4fcf5','font_size': 11, 'border': 1})
                            even_datetime_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss','bg_color': '#FFFFFF', 'font_size': 11,'border': 1})
                            odd_datetime_format = workbook.add_format({'num_format': 'dd/mm/yyyy hh:mm:ss','bg_color': '#d4fcf5','font_size': 11, 'border': 1})
                            
                            for index, row in df.iterrows():
                                row_format = even_row_format if index % 2 == 0 else odd_row_format
                                date_format = even_date_format if index % 2 == 0 else  odd_date_format
                                datetime_format = even_datetime_format if index % 2 == 0 else  odd_datetime_format
                                for col_num, cell_data in enumerate(row):
                                    if pd.api.types.is_datetime64_any_dtype(df.iloc[:, col_num]):  # Kiểm tra cột có phải là datetime
                                        format_to_apply = datetime_format if df.iloc[:, col_num].dtype == 'datetime64[ns]' else date_format
                                        worksheet.write(index + start_row + 1, col_num, cell_data, format_to_apply)
                                    else:
                                        worksheet.write(index + start_row + 1, col_num, cell_data, row_format)
                            
                            # end format
                            
                            # format row size
                            for col_num, value in enumerate(df.columns):
                                column_len = max(df[value].astype(str).map(len).max(), len(value)) + 2
                                worksheet.set_column(col_num, col_num, column_len)
                        # end is format

                        self.logger.info(f'==> Sheet Name [{key}] => Data counter: {df.shape[0]}')
                    else:
                        self.logger.info(f'==> Sheet Name [{key}]: Data empty, Shape of Data => {df.shape[0]},{df.shape[1]} => Not create this sheet')
            self._is_successful = True
        except Exception as e:
            self._is_successful = False
            self._note += f'==> File Name {file_name} [{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Process with Error'
            self.logger.exception(f'==> File Name {file_name}Process with Error, {e}')

    def _export_to_csv(self):
        if not self.export_data or (len(self.export_data) == 1 and self.export_data[0].shape[0] == 0):
            self._note += f'==> Data empty, Rows of Data = 0 => Not Export Empty file'
            self._is_successful = True
            return
        
        if len(self.export_data) > 1 and (not self.export_name or len(self.export_data) != len(self.export_name)):
            self.logger.info(f'==> Config incorrect - Array None or not map Data => Not Export Empty file')
            return

        try:
            file_name = ''
            for i, df in enumerate(self.export_data):
                num = f'_{i}' if i > 0 else ''
                file_name = f"{self.file_name}{num}_{self.export_name[i]}.{self.file_type}"
                is_header = self.get_sheet_is_header(self.export_name[i])
                if df is not None and df.shape[0] > 0 and df.shape[1] > 0:
                    df.to_csv(file_name, sep=self._sep, index=False, header=is_header, encoding='utf-8')
                    self.logger.info(f'==> Data [{i}] {self.export_name[i]} => Data counter: {df.shape[0]}')
                else:
                    self.logger.info(f'==> Data [{i}] {self.export_name[i]}: Data empty, Shape of Data => {df.shape[0]},{df.shape[1]} => Not create this file')
            self._is_successful = True
        except Exception as e:
            self._is_successful = False
            self._note += f'==> File Name {file_name} [{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Process with Error'
            self.logger.exception(f'==> File Name {file_name} Process with Error |Class Writer -> _export_to_csv Error, {e}')

    def _export_to_any_file(self):
        if not self.export_data or (len(self.export_data) == 1 and self.export_data[0].shape[0] == 0):
            self.logger.info(f'==> Data empty, Rows of Data = 0 => Not Export Empty file')
            self._is_successful = True
            return
        
        if len(self.export_data) > 1 and (not self.export_name or len(self.export_data) != len(self.export_name)):
            self.logger.info(f'==> Config incorrect - Array None or not map Data => Not Export Empty file')
            return
        
        try:
            file_name = ''
            for i, df in enumerate(self.export_data):
                num = f'_{i}' if i > 0 and self.export_data[i] is None else ''
                file_name = f"{self.file_name}{num}_{self.export_data[i]}.{self.file_type}"
                if df is not None and df.shape[0] > 0 and df.shape[1] > 0:
                    self._data_frame_export(df, self.file_type, file_name)
                    self.logger.info(f'==> Data [{i}] {self.export_data[i]} => Data counter: {df.shape[0]}')
                else:
                    self.logger.info(f'==> Data [{i}] {self.export_data[i]}: Data empty, Shape of Data => {df.shape[0]},{df.shape[1]} => Not create this file')
            self._is_successful = True
        except Exception as e:
            self._is_successful = False
            self._note += f'==> File Name {file_name} [{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Process with Error'
            self.logger.exception(f'==> File Name {file_name}Process with Error: {e}')

    def _data_frame_export(self, data, file_format, file_path):
        export_functions = {
            DataConstant.RPT_CSV_FILE_TYPE: lambda: data.to_csv(file_path, sep=self._sep, index=False, header=True, encoding='utf-8'),
            DataConstant.RPT_TEXT_FILE_TYPE: lambda: data.to_csv(file_path, sep=self._sep, index=False, header=False, encoding='utf-8'),
            DataConstant.RPT_EXCEL_FILE_TYPE: lambda: data.to_excel(file_path),
            DataConstant.RPT_JSON_FILE_TYPE: lambda: data.to_json(file_path, orient='records', lines=True),
        }
        export_functions.get(file_format.lower(), lambda: data.to_csv(file_path, sep=self._sep, index=False, header=False, encoding='utf-8'))()

    
    def to_file(self):
        """Export DataFrame to any file format."""
        try:
            if self.file_type == DataConstant.RPT_EXCEL_FILE_TYPE:
                self._export_to_excel()
            elif self.file_type == DataConstant.RPT_CSV_FILE_TYPE:
                self._export_to_csv()
            else:
                self._export_to_any_file()
        except Exception as e:
            self._is_successful = False
            self._note += f'[{self.__class__.__name__}][{inspect.currentframe().f_code.co_name}] Error'
            self.logger.exception(e)
