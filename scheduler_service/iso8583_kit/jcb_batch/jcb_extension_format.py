from .jcb_custom_field import JCBCustomField
from ..iso8503_utils import TLVField

# Bit 43: Card Acceptor Name/Location
bit43Format = {
    "s1": JCBCustomField(43, "s1", 25, "Card Acceptor Name", "A"),
    "s2": JCBCustomField(43, "s2", 45, "Address1: Street Address", "A"),
    "s3": JCBCustomField(43, "s3", 13, "Address2: City", "A"),
    "s4": JCBCustomField(43, "s4", 10, "ZIP code", "A"),
    "s5": JCBCustomField(43, "s5", 3, "State code", "A"),
    "s6": JCBCustomField(43, "s6", 3, "Country Code", "A")
}

# Bit 54: Amounts, Additional (For DCC transaction and ATM Access Fee transaction)
bit54Format = {
    "s1": JCBCustomField(54, "s1", 2, "Account Type", "A"), #fix value : 00
    "s2": JCBCustomField(54, "s2", 2, "Amount Type", "A"),
    "s3": JCBCustomField(54, "s3", 3, "Currency Code", "A"),
    "s4": JCBCustomField(54, "s4", 1, "Currency Code", "A"),
    "s5": JCBCustomField(54, "s5", 12, "Amount", "M"),
}

# Integrated Circuit Card (ICC) System-Related Data for Bit 55
bit55Format = {
    "9F26": TLVField(55, "9F26", 8, "Application Cryptogram(AC)", "H"),
    "9F27": TLVField(55, "9F27", 1, "Cryptogram Info. Data", "H"),
    "9F10": TLVField(55, "9F10", 32, "Issuer Application Data(IAD)", "H", prefix="LL"),
    "9F37": TLVField(55, "9F37", 4, "Unpredictable Number", "H"),
    "9F36": TLVField(55, "9F36", 2, "Application Transaction Counter", "N"),
    "95":   TLVField(55, "95", 5, "Terminal Verification Result (TVR)", "H"),
    "9A":   TLVField(55, "9A", 3, "Transaction Date (YYMMDD)", "A"),
    "9C":   TLVField(55, "9C", 1, "Transaction Type", "N"),
    "9F02": TLVField(55, "9F02", 6, "Amount, Authorized", "M"),  # Stored as cents, convert to dollars
    "5F2A": TLVField(55, "5F2A", 2, "Transaction Currency Code (Numeric)", "N"),
    "82":   TLVField(55, "82", 2, "Application Interchange Profile", "H"),
    "9F1A": TLVField(55, "9F1A", 2, "Terminal Country Code (Numeric)", "N"),
    "9F03": TLVField(55, "9F03", 6, "Amount, Other", "M"),
    "9F34": TLVField(55, "9F34", 3, "Cardholder Verification Method (CVM) Result", "H"),
    "9F35": TLVField(55, "9F35", 1, "Terminal Type", "N"),
    "9F09": TLVField(55, "9F09", 2, "Terminal Application Version Number", "H"),
    "9F33": TLVField(55, "9F33", 3, "Terminal Capability", "H"),
    "9F1E": TLVField(55, "9F1E", 8, "Interface Device Serial Number", "H"),
    "4F":   TLVField(55, "4F", 16, "ICC Application ID", "H", prefix="LL"),
    "9F41": TLVField(55, "9F41", 4, "Transaction Sequence Counter", "N"),
    "84":   TLVField(55, "84", 16, "Dedicated File Name", "H", prefix="LL"),
    "9F6E": TLVField(55, "9F6E", 4, "Device Information", "H"),
    "9F7C": TLVField(55, "9F7C", 32, "Partner Discretionary Data(PDD)", "A", prefix="LL"),
    "9505": TLVField(55, "9505", 999, "Terminal Verification Results (TVR)", "TVR"),
}


# Bit 97: Amount, Net Reconciliation (fix len)
bit97Format = {
    "s1": JCBCustomField(97, "s1", 1, "Credit/Debit Indicator", "A"), 
    "s2": JCBCustomField(97, "s2", 16, "Net Amount in Reconciliation Currency", "M"),
}
