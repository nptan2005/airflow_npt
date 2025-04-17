import os

from multiAlgoCoder import generateKey

def main():
    try:
        key_name = input("Nhập key Name: ")
        password = input("Nhập mật khẩu để mã hóa: ")
        rs = generateKey.encode_str(password, key_name)
        print(f'test decode = {generateKey.decode_str(rs)}')
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()