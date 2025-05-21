from ..iso8503_utils import ISO8583Field
from ..iso8503_utils import ISO8583Utils
class JCBCustomField:
    def __init__(self, bit, tag, length, description, valueType):
        """
        Format:
        tag: s1,s2,s3,s4,s5
        length:
        description
        valueType
        value
        """
        self.bit = bit
        self.tag = tag
        self.length = length
        self.description = description
        self.valueType = valueType  # H: Hex, N: Number, M: Money, A: ASCII, etc.

    
    def parse_value(self, raw_data):
        if self.bit == 43 and self.valueType == "A":
            return raw_data.decode('ascii').strip() #loai khoang trang
        return ISO8583Utils.decodeTagValue(raw_data,self.valueType,self.tag)
# JCBCustomField





# Định nghĩa các trường cho ISO8583
iso8583fields = {
"t": ISO8583Field(0, "B", 4, "MTI"),
"1": ISO8583Field(1, "B", 16, "Bitmap"),
"2": ISO8583Field(2, "N", 19, "Primary account number (PAN)", "LL"),
"3": ISO8583Field(3, "N", 6, "Processing code"),
"4": ISO8583Field(4, "N", 12, "Transaction amount"),
"5": ISO8583Field(5, "N", 12, "Amount, settlement"),
"6": ISO8583Field(6, "N", 12, "Amount, cardholder billing"),
"7": ISO8583Field(7, "N", 10, "Transmission date and time"),
"8": ISO8583Field(8, "N", 8, "Amount, cardholder billing fee"),
"9": ISO8583Field(9, "N", 8, "Conversion rate, settlement"),
"10": ISO8583Field(10, "N", 8, "Conversion rate, cardholder billing"),
"11": ISO8583Field(11, "N", 6, "System trace audit number"),
"12": ISO8583Field(12, "N", 12, "Time, local transaction"),
"13": ISO8583Field(13, "N", 4, "Date, local transaction"),
"14": ISO8583Field(14, "N", 4, "Date, expiration"),
"15": ISO8583Field(15, "N", 4, "Date, settlement"),
"16": ISO8583Field(16, "N", 4, "Date, conversion"),
"17": ISO8583Field(17, "N", 4, "Date, capture"),
"18": ISO8583Field(18, "N", 4, "Merchant type"),
"19": ISO8583Field(19, "N", 3, "Acquiring institution country code"),
"20": ISO8583Field(20, "N", 3, "PAN extended country code"),
"21": ISO8583Field(21, "N", 3, "Forwarding institution country code"),
"22": ISO8583Field(22, "N", 12, "Point of service entry mode"),
"23": ISO8583Field(23, "N", 3, "Application PAN sequence number"),
"24": ISO8583Field(24, "N", 3, "Function code"),
"25": ISO8583Field(25, "N", 2, "Point of service condition code"),
"26": ISO8583Field(26, "N", 2, "Point of service capture code"),
"27": ISO8583Field(27, "N", 1, "Authorizing identification response length"),
"28": ISO8583Field(28, "A", 8, "Amount, transaction fee"),
"29": ISO8583Field(29, "A", 8, "Amount, settlement fee"),
"30": ISO8583Field(30, "A", 8, "Amount, transaction processing fee"),
"31": ISO8583Field(31, "A", 8, "Amount, settlement processing fee"),
"32": ISO8583Field(32, "N", 11, "Acquiring institution identification code", "LL"),
"33": ISO8583Field(33, "N", 11, "Forwarding institution identification code", "LL"),
"34": ISO8583Field(34, "A", 28, "Primary account number, extended", "LL"),
"35": ISO8583Field(35, "Z", 37, "Track 2 data", "LL"),
"36": ISO8583Field(36, "Z", 104, "Track 3 data", "LLL"),
"37": ISO8583Field(37, "A", 12, "Retrieval reference number"),
"38": ISO8583Field(38, "A", 6, "Authorization identification response"),
"39": ISO8583Field(39, "A", 2, "Response code"),
"40": ISO8583Field(40, "A", 3, "Service restriction code"),
"41": ISO8583Field(41, "A", 8, "Card acceptor terminal identification"),
"42": ISO8583Field(42, "A", 15, "Card acceptor identification code"),
"43": ISO8583Field(43, "A", 40, "Card acceptor name/location"),
"44": ISO8583Field(44, "A", 25, "Additional response data", "LL"),
"45": ISO8583Field(45, "A", 76, "Track 1 data", "LL"),
"46": ISO8583Field(46, "A", 999, "Additional data - ISO", "LLL"),
"47": ISO8583Field(47, "A", 999, "Additional data - national", "LLL"),
"48": ISO8583Field(48, "A", 999, "Additional data - private", "LLL"),
"49": ISO8583Field(49, "N", 3, "Currency code, transaction"),
"50": ISO8583Field(50, "N", 3, "Currency code, settlement"),
"51": ISO8583Field(51, "N", 3, "Currency code, cardholder billing"),
"52": ISO8583Field(52, "B", 16, "Personal identification number data"),
"53": ISO8583Field(53, "N", 18, "Security related control information"),
"54": ISO8583Field(54, "A", 120, "Additional amounts", "LLL"),
"55": ISO8583Field(55, "B", 255, "ICC data – EMV having multiple tags", "LLL"),
"56": ISO8583Field(56, "A", 999, "Reserved ISO", "LLL"),
"57": ISO8583Field(57, "A", 999, "Reserved national", "LLL"),
"58": ISO8583Field(58, "A", 999, "Reserved national", "LLL"),
"59": ISO8583Field(59, "A", 999, "Reserved national", "LLL"),
"60": ISO8583Field(60, "A", 999, "Reserved national", "LLL"),
"61": ISO8583Field(61, "A", 999, "Reserved private", "LLL"),
"62": ISO8583Field(62, "A", 999, "Reserved private", "LLL"),
"63": ISO8583Field(63, "A", 999, "Reserved private", "LLL"),
"64": ISO8583Field(64, "B", 16, "Message authentication code field"),
"65": ISO8583Field(65, "B", 16, "Bitmap, extended"),
"66": ISO8583Field(66, "N", 1, "Settlement code"),
"67": ISO8583Field(67, "N", 2, "Extended payment code"),
"68": ISO8583Field(68, "N", 3, "Receiving institution country code"),
"69": ISO8583Field(69, "N", 3, "Settlement institution country code"),
"70": ISO8583Field(70, "N", 3, "Network management information code"),
"71": ISO8583Field(71, "N", 4, "Message number"),
"72": ISO8583Field(72, "A", 999, "Data record", "LLL"),
"73": ISO8583Field(73, "N", 6, "Date, action"),
"74": ISO8583Field(74, "N", 10, "Credits, number"),
"75": ISO8583Field(75, "N", 10, "Credits, reversal number"),
"76": ISO8583Field(76, "N", 10, "Debits, number"),
"77": ISO8583Field(77, "N", 10, "Debits, reversal number"),
"78": ISO8583Field(78, "N", 10, "Transfer number"),
"79": ISO8583Field(79, "N", 10, "Transfer, reversal number"),
"80": ISO8583Field(80, "N", 10, "Inquiries number"),
"81": ISO8583Field(81, "N", 10, "Authorizations number"),
"82": ISO8583Field(82, "N", 12, "Credits, processing fee amount"),
"83": ISO8583Field(83, "N", 12, "Credits, transaction fee amount"),
"84": ISO8583Field(84, "N", 12, "Debits, processing fee amount"),
"85": ISO8583Field(85, "N", 12, "Debits, transaction fee amount"),
"86": ISO8583Field(86, "N", 16, "Credits, amount"),
"87": ISO8583Field(87, "N", 16, "Credits, reversal amount"),
"88": ISO8583Field(88, "N", 16, "Debits, amount"),
"89": ISO8583Field(89, "N", 16, "Debits, reversal amount"),
"90": ISO8583Field(90, "N", 42, "Original data elements"),
"91": ISO8583Field(91, "A", 1, "File update code"),
"92": ISO8583Field(92, "A", 2, "File security code"),
"93": ISO8583Field(93, "A", 5, "Response indicator"),
"94": ISO8583Field(94, "A", 7, "Service indicator"),
"95": ISO8583Field(95, "A", 42, "Replacement amounts"),
"96": ISO8583Field(96, "B", 8, "Message security code"),
"97": ISO8583Field(97, "N", 17, "Amount, net settlement"),
"98": ISO8583Field(98, "A", 25, "Payee"),
"99": ISO8583Field(99, "N", 11, "Settlement institution identification code", "LL"),
"100": ISO8583Field(100, "N", 11, "Receiving institution identification code", "LL"),
"101": ISO8583Field(101, "A", 17, "File name"),
"102": ISO8583Field(102, "A", 28, "Account identification 1", "LL"),
"103": ISO8583Field(103, "A", 28, "Account identification 2", "LL"),
"104": ISO8583Field(104, "A", 100, "Transaction description", "LLL"),
"105": ISO8583Field(105, "A", 999, "Reserved for ISO use", "LLL"),
"106": ISO8583Field(106, "A", 999, "Reserved for ISO use", "LLL"),
"107": ISO8583Field(107, "A", 999, "Reserved for ISO use", "LLL"),
"108": ISO8583Field(108, "A", 999, "Reserved for ISO use", "LLL"),
"109": ISO8583Field(109, "A", 999, "Reserved for ISO use", "LLL"),
"110": ISO8583Field(110, "A", 999, "Reserved for ISO use", "LLL"),
"111": ISO8583Field(111, "A", 999, "Reserved for ISO use", "LLL"),
"112": ISO8583Field(112, "A", 999, "Reserved for national use", "LLL"),
"113": ISO8583Field(113, "A", 999, "Reserved for national use", "LLL"),
"114": ISO8583Field(114, "A", 999, "Reserved for national use", "LLL"),
"115": ISO8583Field(115, "A", 999, "Reserved for national use", "LLL"),
"116": ISO8583Field(116, "A", 999, "Reserved for national use", "LLL"),
"117": ISO8583Field(117, "A", 999, "Reserved for national use", "LLL"),
"118": ISO8583Field(118, "A", 999, "Reserved for national use", "LLL"),
"119": ISO8583Field(119, "A", 999, "Reserved for national use", "LLL"),
"120": ISO8583Field(120, "A", 999, "Reserved for private use", "LLL"),
"121": ISO8583Field(121, "A", 999, "Reserved for private use", "LLL"),
"122": ISO8583Field(122, "A", 999, "Reserved for private use", "LLL"),
"123": ISO8583Field(123, "A", 999, "Reserved for private use", "LLL"),
"124": ISO8583Field(124, "A", 999, "Reserved for private use", "LLL"),
"125": ISO8583Field(125, "A", 999, "Reserved for private use", "LLL"),
"126": ISO8583Field(126, "A", 999, "Reserved for private use", "LLL"),
"127": ISO8583Field(127, "A", 999, "Reserved for private use", "LLL"),
"128": ISO8583Field(128, "B", 16, "Message authentication code") 
}
