from ..iso8503_utils import ISO8583Field
# pcode
bit3 = {
    "000000": "Retail",
    "200000": "Refund",
    "120000": "Manual Cash",
    "010000": "ATM",
    "190000": "Sender DEBITs to receiver",
    "290000": "Sender CREDITs to receiver"
}
# Point of Service Data Code (page 100)
bit22 = {
    # Card Data Input Capability
    "p1" : {
        "0": "Card Data Input Capability"
    }
}
# function code
bit24 = {
    "200": "Presentment"
}
# Amounts, Original (page 106)
bit30 = {
    "Outgoing" : {
        "s1": ""
    },
    "Incoming" : {
        "s1": ""
    }
}
# Acquirer Reference Data
bit31 = {
    "s1": ""
}
# Card Acceptor Name/Location
bit43 = {
    "s1": ""
}
# Additional amounts
bit54 = {
    "s1": ""
}

# Data Record
bit72 = {
    "s1": ""
}
# Amount, Net Reconciliation
bit97 = {
    "s1":""
}

# Định nghĩa các trường cho JCB
JCBfields = {
"h": ISO8583Field(0, "B", 4, "Header"),
"t": ISO8583Field(0, "B", 4, "MTI"),
"p": ISO8583Field(0, "B", 8, "Bit Map, Primary"),
"s": ISO8583Field(1, "B", 8, "Bit Map, Secondary"),
"2": ISO8583Field(2, "N", 19, "Primary Account Number (PAN)", "LL"),
"3": ISO8583Field(3, "N", 6, "Processing code"),
"4": ISO8583Field(4, "N", 12, "Amount, Transaction"),
"5": ISO8583Field(5, "N", 12, "Amount, Reconciliation (Settlement)"),
"6": ISO8583Field(6, "N", 12, "Amount, Cardholder Billing"),
"7": ISO8583Field(7, "N", 10, "Transmission date and time"),
"8": ISO8583Field(8, "N", 8, "Amount, cardholder billing fee"),
"9": ISO8583Field(9, "N", 8, "Conversion Rate, Reconciliation(Settlement)"),
"10": ISO8583Field(10, "N", 8, "Conversion Rate, Cardholder Billing"),
"11": ISO8583Field(11, "N", 6, "System trace audit number"),
"12": ISO8583Field(12, "N", 12, "Time local transaction"),
"13": ISO8583Field(13, "N", 4, "Date local transaction"),
"14": ISO8583Field(14, "N", 4, "Date, Expiration"),
"15": ISO8583Field(15, "N", 4, "Settlement date"),
"16": ISO8583Field(16, "N", 4, "Date, Conversion"),
"17": ISO8583Field(17, "N", 4, "Capture date"),
"18": ISO8583Field(18, "N", 4, "Merchant type, or merchant category code"),
"19": ISO8583Field(19, "N", 4, "Acquiring institution (country code)"),
"20": ISO8583Field(20, "N", 3, "PAN extended (country code)"),
"21": ISO8583Field(21, "N", 3, "Forwarding institution (country code)"),
"22": ISO8583Field(22, "AN", 12, "Point of Service Data Code"),
"23": ISO8583Field(23, "N", 3, "Card Sequence Number"),
"24": ISO8583Field(24, "N", 3, "Function code"),
"25": ISO8583Field(25, "ANS", 4, "Message Reason Code"),
"26": ISO8583Field(26, "N", 4, "Card Acceptor Business Code (MCC)"),
"27": ISO8583Field(27, "N", 1, "Authorizing identification response length"),
"28": ISO8583Field(28, "A", 8, "Amount, transaction fee"),
"29": ISO8583Field(29, "A", 8, "Amount, settlement fee"),
"30": ISO8583Field(30, "N", 24, "Amounts, Original"),
"31": ISO8583Field(31, "N", 23, "Acquirer Reference Data","LL"),
"32": ISO8583Field(32, "N", 11, "Forwarding Institution ID Code","LL"),
"33": ISO8583Field(33, "N", 11, "Forwarding institution identification code","LL"),
"34": ISO8583Field(34, "NS", 28, "Primary account number, extended"),
"35": ISO8583Field(35, "Z", 37, "Track 2 data", "LL"),
"36": ISO8583Field(36, "Z", 104, "Track 3 data","LLL"),
"37": ISO8583Field(37, "ANS", 12, "Retrieval reference number"),
"38": ISO8583Field(38, "ANS", 6, "Authorization identification response"),
"39": ISO8583Field(39, "AN", 2, "Response code"),
"40": ISO8583Field(40, "N", 3, "Service Code"),
"41": ISO8583Field(41, "ANS", 8, "Card Acceptor Terminal ID"),
"42": ISO8583Field(42, "ANS", 15, "Card Acceptor ID Code"),
"43": ISO8583Field(43, "ANS", 99, "Card Acceptor Name/Location", "LL"),
"44": ISO8583Field(44, "AN", 25, "Additional response data","LL"),
"45": ISO8583Field(45, "AN", 76, "Track 1 data"),
"46": ISO8583Field(46, "AN", 999, "Additional data (ISO)","LLL"),
"47": ISO8583Field(47, "AN", 999, "Additional data (national)","LLL"),
"48": ISO8583Field(48, "ANS", 999, "Additional data (private)", "LLL"),
"49": ISO8583Field(49, "N", 3, "Currency Code, Transaction"),
"50": ISO8583Field(50, "N", 3, "Currency Code, Reconciliation (Settlement)"),
"51": ISO8583Field(51, "N", 3, "Currency Code, Cardholder Billing"),
"54": ISO8583Field(54, "ANS", 120, "Amounts, Additional","LLL"),
"55": ISO8583Field(55, "B", 255, "Integrated Circuit Card (ICC) System-Related Data","LLL"),
"60": ISO8583Field(60, "S", 60, "Transaction description"),
"61": ISO8583Field(61, "A", 999, "Additional data","LLL"),
"62": ISO8583Field(62, "ANS", 999, "Additional Data 2","LLL"),
"63": ISO8583Field(63, "A", 100, "Card acceptor's terminal identification"),
"71": ISO8583Field(71, "N", 8, "Message Number"),
"72": ISO8583Field(72, "ANS", 999, "Data Record","LLL"),
"90": ISO8583Field(90, "A", 42, "Network management information"),
"93": ISO8583Field(93, "N", 11, "Network management information","LL"),
"94": ISO8583Field(94, "N", 11, "Transaction Originator Institution ID Code","LL"),
"95": ISO8583Field(95, "Z", 42, "Receipt number"),
"97": ISO8583Field(97, "AN", 17, "Amount, Net Reconciliation"),
"98": ISO8583Field(98, "A", 25, "Authorization code"),
"100": ISO8583Field(100, "N", 11, "Receiving institution identification code", "LL"),
"102": ISO8583Field(102, "A", 16, "Acquirer reference"),
"123": ISO8583Field(123, "ANS", 999, "Additional Data 3","LLL"),
"124": ISO8583Field(124, "ANS", 999, "Additional Data 4","LLL"),
"125": ISO8583Field(125, "ANS", 999, "Additional Data 5","LLL"),
"126": ISO8583Field(126, "ANS", 999, "Additional Data 6","LLL"),
"128": ISO8583Field(128, "A", 8, "Message reason code"),
# Thêm trường RDW vào fields 
# "1": ISO8583Field(1, "B", 4, "RDW"), 
}









