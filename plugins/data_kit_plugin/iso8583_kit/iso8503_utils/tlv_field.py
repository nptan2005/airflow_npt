from decimal import Decimal
from .iso8583_utils import ISO8583Utils
class TLVField:
    def __init__(self, bit, tag, length, description, valueType, prefix=None, hexLength=None, value=None):
        self.bit = bit
        self.tag = tag
        self.length = length
        self.description = description
        self.valueType = valueType  # H: Hex, N: Number, M: Money, A: ASCII, etc.
        self.prefix = prefix  # Prefix if applicable
        self.hexLength = hexLength  # If length is hex-encoded (e.g., LLVAR)
        self.value = value  # The actual value stored
    
    def parse_value(self, raw_data):
        return ISO8583Utils.decodeTagValue(raw_data,self.valueType,self.tag)
        
    def parse_amount(self,hex_amount, hex_currency_code):
        # Chuyển đổi hex của số tiền (9F02)
        amount = Decimal(int(hex_amount, 16)) / Decimal(100)
        
        # Chuyển đổi mã tiền tệ từ hex (5F2A)
        currency_code = int(hex_currency_code, 16)

        # Lấy ký hiệu tiền tệ dựa trên mã ISO 4217
        currency = ISO8583Utils.get_currency_symbol(currency_code)

        return f"{currency} {amount:.2f}"


    def __repr__(self):
        return f"TLVField({self.bit}, {self.tag}, {self.length}, {self.description}, {self.valueType})"


# end class TLVField: 