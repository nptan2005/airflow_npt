from iso8583.specs import default

# Khởi tạo spec từ mặc định
jcb_spec = default.copy()
# jcb_spec = {}

# jcb_spec['h'] = {
#     'len_type': 0,  # Fixed length
#     'max_len': 4,   # RDW header
#     'desc': 'Record Descriptor Word (RDW)',
#     'data_enc': 'b',  # Binary encoded
#     'len_enc': 'b',  # Binary encoded
#     'type': 'b'  # Binary type
# }

# jcb_spec["t"] =  { 
#     "data_enc": "ascii",
#     "len_enc": "ascii",
#     "len_type": 0,
#     "max_len": 4,
#     "desc": "MTI"
# } 

jcb_spec["p"] = {
    "data_enc": "b",
    # "len_enc": "ascii",
    # "len_count": "nibbles",
    "len_type": 0,
    "max_len": 8,
    "desc": "Primary Bit Map"
}

jcb_spec["1"] = {
    "data_enc": "b",
    # "len_enc": "ascii",
    # "len_count": "nibbles",
    "len_type": 0,
    "max_len": 8,
    "desc": "Secondary Bit Map"
}

jcb_spec["2"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2,
    "max_len": 19,
    "desc": "Primary Account Number (PAN)"
}

jcb_spec["3"] = {
    "data_enc": "b",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 6,
    'type': 'n',  # Numeric
    "desc": "Processing Code"
}

jcb_spec["4"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "left_pad": "0",
    "max_len": 12,
    'type': 'n',  # Numeric
    "desc": "Amount, Transaction"
}

# Bit 5 = Transaction Amount (Bit 4) * Conversion Rate for Settlement Currency / Conversion Rate for Transaction Currency
jcb_spec["5"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "left_pad": "0",
    "max_len": 12,
    'type': 'n',  # Numeric
    "desc": "Amount, Reconciliation (Settlement)"
}


jcb_spec["6"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "left_pad": "0",
    "max_len": 12,
    'type': 'n',  # Numeric
    "desc": "Amount, Cardholder Billi"
}

jcb_spec["7"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 10,
    'type': 'n',  # Numeric
    "desc": "Transmission date and time"
} 

jcb_spec["9"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    'type': 'n',  # Numeric
    "desc": "Conversion Rate, Reconciliation(Settlement)"
}

jcb_spec["8"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    "desc": "Amount, cardholder billing fee"
} 

jcb_spec["10"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    'type': 'n',  # Numeric
    "desc": "Conversion Rate, Cardholder Billing"
}

jcb_spec["11"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 6,
    "desc": "System trace audit number"
} 

jcb_spec["12"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 12,
    'type': 'n',  # Numeric
    "desc": "Date and Time, Local Transaction"
}

jcb_spec["13"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    "desc": "Date local transaction"
} 

jcb_spec["14"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    'type': 'n',  # Numeric
    "desc": "Date, Expiration"
}

jcb_spec["15"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    "desc": "Settlement date"
} 
jcb_spec["16"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    'type': 'n',  # Numeric
    "desc": "Date, Conversion"
} 
jcb_spec["17"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    "desc": "Capture date"
} 
jcb_spec["18"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    "desc": "Merchant type, or merchant category code"
} 
jcb_spec["19"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    "desc": "Acquiring institution (country code)"
} 
jcb_spec["20"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    "desc": "PAN extended (country code)"
} 
jcb_spec["21"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    "desc": "Forwarding institution (country code)"
} 

jcb_spec["22"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 12,
    'type': 'an',  
    "desc": "Point of Service Data Code"
}

jcb_spec["23"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    'type': 'n',  # Numeric
    "desc": "Card Sequence Number"
} 

jcb_spec["24"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    'type': 'n',  # Numeric
    "desc": "Function Code"
}

jcb_spec["25"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    'type': 'ans',  # Numeric
    "desc": "Message Reason Code"
} 

jcb_spec["26"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 4,
    'type': 'n',  # Numeric
    "desc": "Card Acceptor Business Code (MCC)"
}

jcb_spec["27"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 1,
    "desc": "Authorizing identification response length"
} 
jcb_spec["28"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    "desc": "Amount, transaction fee"
} 
jcb_spec["29"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    "desc": "Amount, settlement fee"
} 
jcb_spec["30"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 24,
    'type': 'n',  # Numeric
    "desc": "Amounts, Original"
} 

jcb_spec["31"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2, #LLVAR
    "max_len": 23,
    'type': 'n',  # Numeric
    "desc": "Acquirer Reference Data"
}

jcb_spec["32"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2, #LLVAR
    "max_len": 11,
    'type': 'n',  # Numeric
    "desc": "Acquiring Institution ID Code"
}

jcb_spec["33"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2, #LLVAR
    "max_len": 11,
    'type': 'n',  # Numeric
    "desc": "Forwarding Institution ID Code"
}

jcb_spec["34"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 28,
    "desc": "Primary account number, extended"
} 
jcb_spec["35"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2,
    "max_len": 37,
    "desc": "Track 2 data"
} 
jcb_spec["36"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 104,
    "desc": "Track 3 data"
} 
jcb_spec["37"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 12,
    'type': 'ans',  
    "desc": "Retrieval reference number"
} 

jcb_spec["38"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0, #Fixed
    "max_len": 6,
    'type': 'ans',  
    "desc": "Approval Code"
}

jcb_spec["39"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 2,
    "desc": "Response code"
} 
jcb_spec["40"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    'type': 'n',  # Numeric
    "desc": "Service Code"
} 
jcb_spec["41"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    'type': 'ans', 
    "desc": "Card Acceptor Terminal ID"
} 

jcb_spec["42"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0, #Fixed
    "max_len": 15,
    "left_pad": " ",
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Card Acceptor ID Code"
}

jcb_spec["43"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2, #LLVAR
    "max_len": 99,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Card Acceptor Name/Location"
}
jcb_spec["45"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 76,
    "desc": "Track 1 data"
} 
jcb_spec["46"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 999,
    "desc": "Additional data (ISO)"
} 
jcb_spec["47"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 999,
    "desc": "Additional data (national)"
} 
jcb_spec["48"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data"
}


jcb_spec["49"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0, #
    "max_len": 3,
    'type': 'n',  # Numeric
    "desc": "Currency Code, Transaction"
}

jcb_spec["50"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    "desc": "Currency Code, Reconciliation (Settlement)"
} 
jcb_spec["51"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 3,
    'type': 'n',  # Numeric
    "desc": "Currency Code, Cardholder Billing"
} 
jcb_spec["54"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 120,
    'type': 'ans',  
    "desc": "Amounts, Additional"
} 
jcb_spec["55"] =  { 
    "data_enc": "b",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 255,
    "desc": "Integrated Circuit Card (ICC) System-Related Data"
} 
jcb_spec["60"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 60,
    "desc": "Transaction description"
} 
jcb_spec["61"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 999,
    "desc": "Additional data"
} 
jcb_spec["62"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data 2"
} 
jcb_spec["63"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 100,
    "desc": "Card acceptor's terminal identification"
} 

jcb_spec["71"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0, #
    "max_len": 8,
    "left_pad": "0",
    'type': 'n',  # Numeric
    "desc": "Message Number"
}

jcb_spec["72"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3,
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Data Record"
} 

jcb_spec["90"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 42,
    "desc": "Network management information"
} 
jcb_spec["93"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2,
    "max_len": 11,
    "desc": "Network management information"
} 

jcb_spec["94"] = {
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2, #LLVAR
    "max_len": 11,
    'type': 'n',  # Numeric
    "desc": "Transaction Originator Institution ID Code"
}

jcb_spec["95"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 42,
    "desc": "Receipt number"
} 
jcb_spec["97"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 17,
    'type': 'an',  # Alphabetic, Numeric
    "desc": "Amount, Net Reconciliation"
} 
jcb_spec["98"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 25,
    "desc": "Authorization code"
} 
jcb_spec["100"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 2,
    "max_len": 11,
    'type': 'n',  # Numeric
    "desc": "Receiving institution identification code"
} 
jcb_spec["102"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 16,
    "desc": "Acquirer reference"
} 
jcb_spec["123"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data 3"
} 
jcb_spec["124"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data 4"
} 
jcb_spec["125"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data 5"
} 
jcb_spec["126"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 3, #LLLVAR
    "max_len": 999,
    'type': 'ans',  # Alphabetic, Numeric, Special characters
    "desc": "Additional Data 6"
} 
jcb_spec["128"] =  { 
    "data_enc": "ascii",
    "len_enc": "ascii",
    "len_type": 0,
    "max_len": 8,
    "desc": "Message reason code"
} 


# Định nghĩa các trường từ cấu hình JCB
# jcb_spec["h"] = {"data_enc": "b", "len_enc": "b", "max_len": 0}  # Header
# jcb_spec["t"] = {"data_enc": "ascii", "len_enc": "ascii", "len_type": 0,"max_len": 4}  # MTI
# jcb_spec["p"] = {"data_enc": "b", "len_enc": "ascii","len_type": 0, "max_len": 8, "len_count": "nibbles"}  # Primary Bitmap
# # jcb_spec["s"] = {"data_enc": "b", "len_enc": "b", "max_len": 8}  # Secondary Bitmap
# jcb_spec[1] = {"data_enc": "b", "len_enc": "ascii", "len_type": 0, "max_len": 8, "len_count": "nibbles"}  # Secondary Bitmap
# # Định nghĩa các trường từ 2 - 128
# jcb_spec[2] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 2, "max_len": 19}
# jcb_spec[3] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 0, "max_len": 6}
# jcb_spec[4] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[5] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[6] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[7] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 10}
# jcb_spec[8] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[9] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[10] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[11] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 6}
# jcb_spec[12] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[13] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[14] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[15] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[16] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[17] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[18] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[19] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[20] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[21] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[22] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[23] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[24] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[25] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[26] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 4}
# jcb_spec[27] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 1}
# jcb_spec[28] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[29] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[30] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 24}
# jcb_spec[31] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 2, "max_len": 23}
# jcb_spec[32] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 2,  "max_len": 11}
# jcb_spec[33] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 2,  "max_len": 11}
# jcb_spec[34] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 28}
# jcb_spec[35] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 2, "max_len": 37}
# jcb_spec[36] = {"data_enc": "ascii", "len_enc": "ascii","len_type": 3, "max_len": 104}
# jcb_spec[37] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 12}
# jcb_spec[38] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 6}
# jcb_spec[39] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 2}
# jcb_spec[40] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[41] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[42] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 15}
# jcb_spec[43] = {"data_enc": "latin-1", "len_enc": "ascii","len_type": 2, "max_len": 99}
# jcb_spec[44] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 25, "prefix": "LL"}
# jcb_spec[45] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 76}
# jcb_spec[46] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[47] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[48] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[49] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[50] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[51] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 3}
# jcb_spec[54] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 120, "prefix": "LLL"}
# jcb_spec[55] = {"data_enc": "cp500", "len_enc": "cp500", "max_len": 255, "prefix": "LLL"}
# jcb_spec[60] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 60}
# jcb_spec[61] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[62] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[63] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 100}
# jcb_spec[71] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}
# jcb_spec[72] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999, "prefix": "LLL"}
# jcb_spec[90] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 42}
# jcb_spec[93] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 11, "prefix": "LL"}
# jcb_spec[94] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 99, "prefix": "LL"}
# jcb_spec[95] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 42}
# jcb_spec[96] = {"data_enc": "b", "len_enc": "ascii", "max_len": 8}
# jcb_spec[97] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 17}
# jcb_spec[98] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 25}
# jcb_spec[99] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 11, "prefix": "LL"}
# jcb_spec[100] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 11, "prefix": "LL"}
# jcb_spec[101] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 17}
# jcb_spec[102] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 28, "prefix": "LL"}
# jcb_spec[103] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 28, "prefix": "LL"}
# jcb_spec[104] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 100, "prefix": "LLL"}
# jcb_spec[105] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[106] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[107] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[108] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[109] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[110] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[111] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[112] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[113] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[114] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[115] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[116] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[117] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[118] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[119] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[120] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[121] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[122] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[123] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 999}
# jcb_spec[124] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 255, "prefix": "LLL"}
# jcb_spec[125] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 50, "prefix": "LL"}
# jcb_spec[126] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 6}
# jcb_spec[127] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 100}
# jcb_spec[128] = {"data_enc": "ascii", "len_enc": "ascii", "max_len": 8}