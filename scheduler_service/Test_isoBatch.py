# import iso8583
import binascii
import configparser
import os


# import iso8583.specs
# from iso8583_kit import JCBfields
from iso8583_kit import JCBBatchDump
from utilities import Utils as utils


config = configparser.ConfigParser()


reportPath = os.path.join('Data','Import_Data')
path = 'ISO_BATCH'

  
# fileRead = 'JCB_240801_001.txt'
# fileRead = 'JCBretail20240802100918.TXT'
# fileRead = 'JCB_TEST_1240.txt'
# fileRead = 'JCB_250331_001.txt'
fileRead = 'JCB_250401_003.txt'
with JCBBatchDump(file_name=fileRead,is_dump_to_file=True,is_logger=False) as iso:
    iso.iso_dump()


# import iso8583
# from iso8583 import DecodeError
# from iso8583_kit import jcb_spec as spec

# try:
#     b = parsor.parse_msg_to_iso_str(a) 
#     c = b[1]
#     # print(c)
#     bitmap_raw = c[:8]  # Primary bitmap (8 bytes đầu tiên)
#     # print(f"Raw Bitmap: {bitmap_raw}")
#     # bitmap = [i for i, bit in enumerate(format(int.from_bytes(bitmap_raw, "big"), "064b")) if bit == "1"]
#     # print(f"Bitmap Fields: {bitmap}")

#     decoded, encoded = iso8583.decode(c, spec)
#     print("Thông điệp ISO8583 đã giải mã:")
#     print("{:<10} {:<50} {:<50}".format("Field", "Tên trường", "Giá trị"))
#     print("-" * 80)
#     for field, data in decoded.items():
#         print("{:<10} {:<50} {:<50}".format(field, spec.get(field, {}).get("desc", "N/A"), data))
        



# except DecodeError as e:
#     print(f"Filed 28: {c[84:92]}") 
#     # print("Cấu hình spec:", spec)
#     print("Thông tin lỗi chi tiết:")
#     print(e)
#     print(f"Dữ liệu bị lỗi tại: {c}")

    
# from iso8583 import EncodeError

# try:
#     # decoded["100"] = {"12345678901"}



#     decoded["39"] = "00"  # Cập nhật trường 39 với giá trị "00"
#     print(decoded)
#     print(decoded.get("100"))

#     encoded_message = iso8583.encode(decoded, spec)
#     print("Thông điệp sau khi mã hóa:", encoded_message)
# except EncodeError as e:
#     print(f"Lỗi mã hóa: {e}")



# print(b[1])

# Giải mã dữ liệu
# decoded, encoded = iso8583.decode(a, spec)

# In dữ liệu đã giải mã
# print(encoded)

