from typing import TextIO
from . import ISO8583Field
import textwrap
class ISO8583Print:
    
    @staticmethod
    def print_tvr_field(tvr: dict[str, str],
        stream: TextIO,
        indent:int
        ) -> None:
        if indent > 24:
            indent = 24
        else:
            indent += 1
        for bit_description, bit_value in tvr.items():
            stream.write(f"{' ' * indent}{bit_description:<47}: {'Yes' if bit_value == '1' else 'No':<3} ({repr(bit_value)})\n")

    # print_tvr_field

    @staticmethod
    def print_tlv_field(tlv: dict[str, any],
        stream: TextIO,
        indent: int,
        ) -> None:
        if indent > 10:
            indent = 10
        else:
            indent += 1
       
        stream.write(f"{' ' * indent}{'Tag':12}: {tlv['Tag']}\n")
        if 'Description' in tlv:
            stream.write(f"{' ' * indent}{'Description':12}: {tlv['Description']}\n")
        stream.write(f"{' ' * indent}{'Length':12}: {tlv['Length']}\n")
        if isinstance(tlv['Value'],dict):
            stream.write(f"{' ' * indent}{'Value':12}:\n")
            ISO8583Print.print_tvr_field(tlv['Value'],stream,indent)
        elif isinstance(tlv['Value'],list):
            ISO8583Print.print_list_additional(tlv['Value'],stream,indent)
        else:
            stream.write(f"{' ' * indent}{'Value':12}: {repr(tlv['Value'])}\n")

    # print_tlv_field

    @staticmethod
    def print_custom_field(data: dict[str, any],
        stream: TextIO,
        indent: int,
        ) -> None:
        if indent > 10:
            indent = 10
        else:
            indent += 1
       
        stream.write(f"{' ' * indent}{'Field':12}: {data['Field']}\n")
        if 'Description' in data:
            stream.write(f"{' ' * indent}{'Description':12}: {data['Description']}\n")
        stream.write(f"{' ' * indent}{'Length':12}: {data['Length']}\n")
        if isinstance(data['Data'],dict):
            stream.write(f"{' ' * indent}{'Data':12}:\n")
            ISO8583Print.print_tvr_field(data['Data'],stream,indent)
        elif isinstance(data['Data'],list):
            ISO8583Print.print_list_additional(data['Data'],stream,indent)
        else:
            stream.write(f"{' ' * indent}{'Data':12}: {repr(data['Data'])}\n")

    # print_custom_field

    @staticmethod
    def print_dict(dictData: dict[any, any],
        stream: TextIO,
        indent: int,
        ) -> None:
        if indent > 24:
            indent = 24
        else:
            indent += 1
        for key, item in dictData.items():
            stream.write(f"{' ' * indent}{key:12s}        : {item}\n")

    # print_dict

    @staticmethod
    def print_list_additional(listData: list,
        stream: TextIO,
        indent: int,
        ) -> None:
        indent+=24
        _field_num = 0
        for data_element in listData:
            if indent > 24:
                indent =24
            if isinstance(data_element,dict):
                _field_num += 1
                stream.write(f"{' ' * indent}>>>Additional Field: {_field_num}\n")
                ISO8583Print.print_dict(data_element,stream,indent)
                stream.write(f"{' ' * indent}{'-' * 25}\n")
            else:
                stream.write(f"{' ' * indent}{data_element}\n")
    # print_dict_additional
    @staticmethod
    def msg_to_stream(msg:str,stream: TextIO) -> None:
        stream.write(msg)
        stream.write("\n")
    # msg_to_stream

    @staticmethod
    def format_with_indent(data, width, indent):
        # Dòng đầu tiên có indent riêng, các dòng tiếp theo có indent khác
        wrapper = textwrap.TextWrapper(
            width=width, 
            initial_indent=" " * indent,  # Thụt lề dòng đầu tiên
            subsequent_indent=" " * indent  # Thụt lề các dòng tiếp theo
        )
        return wrapper.fill(data)  
    # format_with_indent  
    @staticmethod
    def print_iso_field(field: ISO8583Field,
    stream: TextIO,
    line_width: int
    ) -> None:
        field_name = f"|Bit{field.field_number:4d}"
        indent = len(field_name)
        stream.write(field_name)

        if field.data_type:
            desc = field.data_type
            stream.write(f" | {desc:<49}")
            indent += 49 + 1

        stream.write("| ")

        if isinstance(field.decodeValue, list) and all(isinstance(item, dict) for item in field.decodeValue):
            stream.write("\n")
            _field_num = 0
            for item in field.decodeValue:
                _field_num +=1
                if all(k in item for k in ["Tag", "Length", "Value","Description"]):
                    stream.write(f"{' ' * 10}|{'-' * 70}|\n")
                    stream.write(f"{' ' * 10}|{' ' * 24} TLV Field Number: {str(_field_num):3s}{' ' * 24}|\n")
                    stream.write(f"{' ' * 10}|{'-' * 70}|\n")
                    stream.write(f"{' ' * 10}|{' Name':11s}|{' Value':58}|\n")
                    stream.write(f"{' ' * 10}|{'-' * 70}|\n")
                    ISO8583Print.print_tlv_field(item, stream, indent)
                elif all(k in item for k in ["Field", "Length", "Data","Description"]):
                    stream.write(f"{' ' * 10}>>>Custom Field Number: {_field_num}\n")
                    ISO8583Print.print_custom_field(item, stream, indent)
                stream.write(f"{' ' * 10}{'-' * 50}\n")
        else:
            rep = repr(field.decodeValue)

            if len(rep) + indent > line_width:
                rep = ISO8583Print.format_with_indent(data=rep, width=line_width,indent=indent)
                stream.write(f"\n{rep}\n")
            else:
                stream.write(f"{rep}\n")
    # print_iso_field
    
    @staticmethod
    def print_raw_iso_field(field: ISO8583Field,
    stream: TextIO,
    line_width: int
    ) -> None:
        indent = 5
        
        stream.write(f"Bit{field.field_number:4d}")

        if field.data_type:
            desc = field.data_type
            stream.write(f" | {desc:<50}")
            indent += 50 + 1

        stream.write(": ")
        
        rep = repr(field.encodeValue)

        if len(rep) + indent > line_width:
            stream.write(f"\n{' ' * indent}{rep}\n")
        else:
            stream.write(f"{rep}\n")
    # print_raw_iso_field