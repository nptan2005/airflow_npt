from decimal import Decimal
from .tvr_data import TVRData
class ISO8583Utils:
    
    @staticmethod
    def calculate_rdw(self,message_length, byte_length: int):
        """
        Tính toán RDW (Record Descriptor Word) cho ISO 8583.

        Args:
        message_length (int): Độ dài của message (không bao gồm RDW).
        byte_length (int): Độ dài của RDW (2, 4, hoặc 8 bytes).

        Returns:
        str: Chuỗi nhị phân của RDW.
        """
        # Tính toán số bit cần thiết dựa trên số byte
        bit_length = byte_length * 8

        # Chuyển đổi độ dài từ thập phân sang nhị phân và đảm bảo độ dài bit phù hợp
        rdw_binary = format(message_length, f'0{bit_length}b')

        return rdw_binary
    # calculate_rdw

    @staticmethod
    def generate_rdw(self,message_length:int,byte_length: int)->bytes:
        """
        Tạo chuỗi RDW (Record Descriptor Word) cho ISO 8583.

        Args:
            message_length (int): Độ dài của message (không bao gồm RDW).
            byte_length (int): Độ dài của RDW (2, 4, hoặc 8 bytes).
        Returns:
            bytes: Chuỗi RDW được mã hóa.
        """
        # print(f' độ dài input: {message_length}')
        binary_length = self.__calculate_rdw(message_length,byte_length)
        # print()
        # print(f'Binary: {binary_length}')
        # Tính toán số lượng ký tự hexadecimal cần thiết
        hex_digits = byte_length * 2
        hex_length = hex(int(binary_length, 2))[2:].zfill(hex_digits).upper()
        # print(f'Hex: {hex_length}')
        # Chuyển đổi hexadecimal sang chuỗi bytes
        rdw = bytes.fromhex(hex_length)
        # print(f'RDW: {rdw} | len {len(rdw)}')
        return rdw
    # generate_rdw


    @staticmethod
    def write_iso8583_header(self,data: bytes) -> bytes:
        # Tính toán chiều dài của chuỗi
        if "h" in self.fields:
            headerField = self.fields["h"]
            if headerField.field_length > 0:
                length = len(data)

                # Chuyển đổi chiều dài thành bytes (4 bytes, big-endian)
                header = self.__generate_rdw(length,headerField.field_length)

                return header + data
        return data
    # write_iso8583_header
    
    @staticmethod
    def bytes_to_hex(data:bytes)-> str:
        return data.hex().upper()
    # bytes_to_hex

    @staticmethod
    def bytes_to_int(data:bytes) -> int:
        return  int.from_bytes(data, byteorder='big')
    # bytes_to_int

    @staticmethod
    def bytes_to_accii(data:bytes, decodeType:str = 'ascii') -> str:
        """
        decodeType:str = 'ascii'
        decodeType:str = 'latin-1'
        decodeType:str = 'utf-8'
        """
        return data.decode(decodeType).strip()
    # bytes_to_accii

    @staticmethod
    def bytes_to_binary(data:bytes, fill_len:int=64) -> str:
        # bin(int(data.hex().upper(), 16))[2:].zfill(64) 
        return bin(ISO8583Utils.hex_to_int(ISO8583Utils.bytes_to_hex(data)))[2:].zfill(fill_len) 
    # bytes_to_binary

    @staticmethod
    def hex_to_bytes(data:str)-> bytes:
        return bytes.fromhex(data)
    # hex_to_bytes

    @staticmethod
    def hex_to_int(data:str)-> int:
        return int(data, 16)
    # hex_to_int

    @staticmethod
    def hex_to_ascii(hex_str:str) -> str:
        bytes_object = bytes.fromhex(hex_str)
        ascii_str = bytes_object.decode("ascii", errors="ignore")
        return ascii_str
    # hex_to_ascii

    @staticmethod
    def string_to_binary(input_string):
        binary_string = ''.join(format(int(char), '04b') for char in input_string)
        return binary_string
    # string_to_binary



    @staticmethod
    def lenOfIsoMessage(inputStr):
        message_length = len(inputStr.encode('ascii'))
        return message_length
    # lenOfIsoMessage

    @staticmethod
    def is_byte(data):
        return isinstance(data, bytes)
    # is_byte

    @staticmethod
    def is_hex(data):
        try:
            int(data, 16)
            return True
        except ValueError:
            return False
    # is_hex
        
    @staticmethod
    def is_empty(data):
        if data is None:
            return True
        if len(data) == 0:
            return True
    # is_empty
       
    @staticmethod 
    def dict_has_data(d: dict) -> bool:
        return any(d.values())
    # dict_has_data

    @staticmethod
    def decodeTagValue(raw_data, valueType, tag = None):
        if valueType == "H":
            if ISO8583Utils.is_hex(raw_data):
                return raw_data  # Keep as hex
            elif ISO8583Utils.is_byte(raw_data):
                return ISO8583Utils.bytes_to_hex(raw_data) 
            else:
                return raw_data
        elif valueType == "N":
            if ISO8583Utils.is_hex(raw_data):
                return ISO8583Utils.hex_to_int(raw_data)  # Convert hex to integer
            elif ISO8583Utils.is_byte(raw_data):
                return ISO8583Utils.bytes_to_int(raw_data)
            else:
                return raw_data
        elif valueType == "M":
            if ISO8583Utils.is_hex(raw_data):
                return float(ISO8583Utils.hex_to_int(raw_data))   # Assume money is stored in cents need /100. else keep org values
            elif ISO8583Utils.is_byte(raw_data):
                return float(ISO8583Utils.bytes_to_int(raw_data))
            else:
                return raw_data
        elif valueType == "A": # Convert hex to ASCII string
            if ISO8583Utils.is_hex(raw_data):
                return ISO8583Utils.hex_to_ascii(raw_data)
            elif ISO8583Utils.is_byte:
                return ISO8583Utils.hex_to_ascii(ISO8583Utils.bytes_to_hex(raw_data))
        elif valueType == "BCD":
            return raw_data.hex()
            # BCD length
            # elif field_spec["len_enc"] == "bcd":
            #     try:
            #         enc_field_len = int(s[idx : idx + len_type].hex(), 10)
        elif  valueType == "TVR" and tag == "9505":
            tvr = TVRData(raw_data)
            return tvr.parse()
        else:
            return raw_data  # Default: keep raw data
    # decodeTagValue
    
    @staticmethod    
    def get_currency_symbol(currency_code):
        # Chuyển đổi mã tiền tệ thành ký hiệu
        if currency_code == 840:
            return "USD"
        elif currency_code == 978:
            return "EUR"
        elif currency_code == 704:
            return "VND"
        else:
            return "Unknown Currency"
    # get_currency_symbol
        
    @staticmethod
    def format_amount(hex_amount, hex_currency_code):
        # Chuyển đổi hex của số tiền (9F02)
        amount = Decimal(int(hex_amount, 16)) / Decimal(100)
            
        # Chuyển đổi mã tiền tệ từ hex (5F2A)
        currency_code = int(hex_currency_code, 16)

        # Lấy ký hiệu tiền tệ dựa trên mã ISO 4217
        currency = ISO8583Utils.get_currency_symbol(currency_code)

        return f"{currency} {amount:.2f}"
    # format_amount
    
    