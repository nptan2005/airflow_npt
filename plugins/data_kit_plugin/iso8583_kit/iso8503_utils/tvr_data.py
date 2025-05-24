class TVRData:
    def __init__(self, hex_tvr):
        """
        Tag: 9505
        TVR (Terminal Verification Results) chứa kết quả các kiểm tra bảo mật và xác thực được thực hiện bởi thiết bị terminal khi xử lý giao dịch thẻ. TVR là một chuỗi 5 bytes (40 bits), trong đó mỗi bit biểu diễn một trạng thái kiểm tra cụ thể (như xác thực offline, xác minh PIN, kiểm tra mã số quốc gia).

            Mô tả bit flag trong TVR (theo EMV):

                •	Byte 1:
                    •	Bit 8: Offline Data Authentication Was Not Performed
                    •	Bit 7: SDA Failed
                    •	Bit 6: ICC Data Missing
                    •	Bit 5: Card Appears on Terminal Exception File
                    •	Bit 4: DDA Failed
                    •	Bit 3: CDA Failed
                    •	Bit 2: RFU (Reserved for Future Use)
                    •	Bit 1: RFU
                •	Byte 2:
                    •	Bit 8: ICC and Terminal Have Different Application Versions
                    •	Bit 7: Expired Application
                    •	Bit 6: Application Not Yet Effective
                    •	Bit 5: Requested Service Not Allowed for Card Product
                    •	Bit 4: New Card
                •	Byte 3:
                    •	Bit 8: Cardholder Verification Was Not Successful
                    •	Bit 7: Unrecognised CVM
                    •	Bit 6: PIN Try Limit Exceeded
                    •	Bit 5: PIN Entry Required and PIN Pad Not Present or Not Working
                    •	Bit 4: PIN Entry Required, PIN Pad Present, But PIN Was Not Entered
                    •	Bit 3: Online PIN Entered
                	•	Bit 2-1: RFU
                •	Byte 4:
                    •	Bit 8: Transaction Exceeds Floor Limit
                    •	Bit 7: Lower Consecutive Offline Limit Exceeded
                    •	Bit 6: Upper Consecutive Offline Limit Exceeded
                    •	Bit 5: Transaction Selected Randomly for Online Processing
                    •	Bit 4: Merchant Forced Transaction Online
                •	Byte 5:
                    •	Bit 8: Default TDOL Used
                    •	Bit 7: Issuer Authentication Failed
                    •	Bit 6: Script Processing Failed Before Final GENERATE AC
                    •	Bit 5: Script Processing Failed After Final GENERATE AC
        """
        # Chuyển TVR từ hex sang nhị phân
        if not hex_tvr:
            raise ValueError("hex_tvr is empty")
        try:
            self.tvr_bin = bin(int(hex_tvr, 16))[2:].zfill(40)  # 5 bytes = 40 bits
        except ValueError as e:
            raise ValueError(f"Invalid hex value: {hex_tvr}") from e
       
    
    def parse(self):
        # Mapping chi tiết từng bit trong TVR
        parsed_tvr = {
            # Byte 1 (Bits 1-8)
            "Offline Data Authentication Not Performed": self.tvr_bin[0],
            "SDA Failed": self.tvr_bin[1],
            "ICC Data Missing": self.tvr_bin[2],
            "Card on Terminal Exception File": self.tvr_bin[3],
            "DDA Failed": self.tvr_bin[4],
            "CDA Failed": self.tvr_bin[5],
            "RFU Byte 1 Bit 2": self.tvr_bin[6],
            "RFU Byte 1 Bit 1": self.tvr_bin[7],
            # Byte 2 (Bits 9-16)
            "ICC and Terminal Different Application Versions": self.tvr_bin[8],
            "Expired Application": self.tvr_bin[9],
            "Application Not Yet Effective": self.tvr_bin[10],
            "Service Not Allowed for Card Product": self.tvr_bin[11],
            "New Card": self.tvr_bin[12],
            "RFU Byte 2 Bit 3": self.tvr_bin[13],
            "RFU Byte 2 Bit 2": self.tvr_bin[14],
            "RFU Byte 2 Bit 1": self.tvr_bin[15],
            # Byte 3 (Bits 17-24)
            "Cardholder Verification Not Successful": self.tvr_bin[16],
            "Unrecognized CVM": self.tvr_bin[17],
            "PIN Try Limit Exceeded": self.tvr_bin[18],
            "PIN Entry Required and PIN Pad Not Present": self.tvr_bin[19],
            "PIN Pad Present But PIN Not Entered": self.tvr_bin[20],
            "Online PIN Entered": self.tvr_bin[21],
            "RFU Byte 3 Bit 2": self.tvr_bin[22],
            "RFU Byte 3 Bit 1": self.tvr_bin[23],
            # Byte 4 (Bits 25-32)
            "Transaction Exceeds Floor Limit": self.tvr_bin[24],
            "Lower Consecutive Offline Limit Exceeded": self.tvr_bin[25],
            "Upper Consecutive Offline Limit Exceeded": self.tvr_bin[26],
            "Transaction Randomly Selected for Online": self.tvr_bin[27],
            "Merchant Forced Transaction Online": self.tvr_bin[28],
            "RFU Byte 4 Bit 3": self.tvr_bin[29],
            "RFU Byte 4 Bit 2": self.tvr_bin[30],
            "RFU Byte 4 Bit 1": self.tvr_bin[31],
            # Byte 5 (Bits 33-40)
            "Default TDOL Used": self.tvr_bin[32],
            "Issuer Authentication Failed": self.tvr_bin[33],
            "Script Processing Failed Before Final AC": self.tvr_bin[34],
            "Script Processing Failed After Final AC": self.tvr_bin[35],
            "RFU Byte 5 Bit 4": self.tvr_bin[36],
            "RFU Byte 5 Bit 3": self.tvr_bin[37],
            "RFU Byte 5 Bit 2": self.tvr_bin[38],
            "RFU Byte 5 Bit 1": self.tvr_bin[39],
        }
        return parsed_tvr
# end class TVR