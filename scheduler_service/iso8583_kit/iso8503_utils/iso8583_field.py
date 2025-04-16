"""
•  h: Header - Thường chứa thông tin tiêu đề của thông điệp.

•  t: MTI (Message Type Indicator) - Chỉ báo loại thông điệp, xác định loại giao dịch.

•  p: Primary Bitmap - Bitmap chính, xác định các trường dữ liệu có mặt trong thông điệp.

•  s: Secondary Bitmap - Bitmap phụ, xác định các trường dữ liệu bổ sung có mặt trong thông điệp.
"""
import copy
class ISO8583Field:
    def __init__(self, field_number:int, field_type:str, field_length:int, data_type:str=None, prefix:str=None):
        """
        field_number: bit
        field_type: kiểu dữ liệu
        field_length: max len của field
        data_type: Diễn giải field
        field_type: N, A, B, S, Z
            •  N: Numeric - Chỉ chứa các ký tự số (0-9).
            •  A: Alphanumeric - Chứa các ký tự chữ và số (A-Z, a-z, 0-9).
            •  B: Binary - Chứa dữ liệu nhị phân.
            •  S: Special - Chứa các ký tự đặc biệt
            •  Z: Track Data - Chứa dữ liệu track (thường được sử dụng cho dữ liệu thẻ từ).
        field_length: max len
        data_type: description of bit
        prefix: # L, LL, LLL
            •  define 1 len
            •  define 2 len
            •  define 3 len
        """
        self.field_number = field_number
        self.field_type = field_type  # N, A, B, S, Z
        self.field_length = field_length
        self.data_type = data_type  # Kiểu dữ liệu (nếu cần)
        self.prefix = prefix  #L, LL, LLL
        self._encodeValue = None
        self._decodeValue = None

    @property
    def encodeValue(self):
        return self._encodeValue
    
    @encodeValue.setter
    def encodeValue(self,value):
        self._encodeValue = value

    @property
    def decodeValue(self):
        return self._decodeValue
    
    @decodeValue.setter
    def decodeValue(self, value):
        self._decodeValue = value

    def __deepcopy__(self, memo):
        # Tạo một bản sao mới của đối tượng
        deepCopyCls = ISO8583Field(
        self.field_number,
        self.field_type,
        self.field_length,
        self.data_type,
        self.prefix
        )
        deepCopyCls.encodeValue = copy.deepcopy(self.encodeValue, memo)
        deepCopyCls.decodeValue = copy.deepcopy(self.decodeValue, memo)
        return deepCopyCls
# ISO8583Field