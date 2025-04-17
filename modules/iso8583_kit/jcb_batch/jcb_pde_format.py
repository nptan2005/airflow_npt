from .jcb_custom_field import JCBCustomField
from datetime import datetime



pde3001Format = {
    "s0": JCBCustomField(3001, "s0", 3, " Card Product and Card Grade", "N")
}
# Khai báo cho PDE3002 Currency Exponents
pde3002Format = {
"s1": JCBCustomField(3002, "s1", 3, "Currency Code", "N"),
"s2": JCBCustomField(3002, "s2", 1, "Currency Exponent", "AN")
}

# Bit 3003: Clearing Data
pde3003Format = {
    "s1": JCBCustomField(3003, "s1", 2, "Interchange Type", "N"),
    "s2": JCBCustomField(3003, "s2", 15, "Interchange Type Name", "A"),
    "s3": JCBCustomField(3003, "s3", 6, "Central Processing Date", "N"),
    "s4": JCBCustomField(3003, "s4", 2, "Clearing Cut Off Cycle", "N"),
}

# Bit 3004: Sub-LCID
pde3004Format = {
    "s1": JCBCustomField(3004, "s1", 4, "Sub Licensee ID", "AN"),  # AN: Alphabetic, Numeric
}

# Bit 3005: Amounts, Transaction Fees
pde3005Format = {
    "s1": JCBCustomField(3005, "s1", 5, "Fee Code", "A"),
    "s2": JCBCustomField(3005, "s2", 3, "Product / Grade", "A"),
    "s3": JCBCustomField(3005, "s3", 4, "MCC", "A"),  # Same values in PDE 3001
    "s4": JCBCustomField(3005, "s4", 10, "Fee Incentive Info", "A"),
    "ss1": JCBCustomField(3005, "ss1", 1, "IC", "N"),  # 0: Not Applicable, 1: Applicable
    "ss2": JCBCustomField(3005, "ss2", 1, "3-D Secure", "N"),  # Values: 0, 1, 2, 3
    "ss3": JCBCustomField(3005, "ss3", 1, "Transaction Date", "N"),  # 0: Not Applicable, 1: Applicable
    "ss4": JCBCustomField(3005, "ss4", 1, "ATM Access Fee", "N"),  # 0: Not Applicable, 1: Applicable
    "ss5": JCBCustomField(3005, "ss5", 1, "Region Specific", "N"),  # 0: Not Applicable, 1: Applicable
    "ss6": JCBCustomField(3005, "ss6", 1, "Transaction Classification", "N"),  # 0: Not Applicable, 1: Applicable
    "ss7": JCBCustomField(3005, "ss7", 1, "Description", "N"),
    "s5": JCBCustomField(3005, "s4", 8, "Fee Rate", "N"),
    "s6": JCBCustomField(3005, "s6", 3, "Currency Code, Fee Price", "N"),
    "s7": JCBCustomField(3005, "s7", 8, "Fee Price", "N"),
    "s8": JCBCustomField(3005, "s8", 1, "Credit/Debit Indicatot", "A"),
    "s9": JCBCustomField(3005, "s9", 3, "Currency Code, Fee, Reconciliation", "N"),
    "s10": JCBCustomField(3005, "s10", 12, "Amount, fee, Reconciliation", "N"),
}

# Bit 3006: Additional Info
pde3006Format = {
    "s1": JCBCustomField(3006, "s1", 8, "Processing Info for Issuer (DE 18 of QR OIG)", "N"),
    "ss1": JCBCustomField(3006, "ss1", 1, "Pan Entry Mode Detail", "N"),  # 1: BAR Code, 2: QR Code
    "ss2": JCBCustomField(3006, "ss2", 1, "QR Processing Mode", "N"),  # 1: MPM, 2: CPM
    "ss3": JCBCustomField(3006, "ss3", 2, "Point of Initation Method", "N"),  # 11: Static QR Code, 12: Dynamic QR Code, 99: Other
    "ss4": JCBCustomField(3006, "ss4", 4, "RFU", "N"),  # Always set '0000'
    "s2": JCBCustomField(3006, "s2", 25, "Issuer Reference Number (DE 1 of QR OIG)", "ANS"),  # Value set by the Issuer
    "s3": JCBCustomField(3006, "s3", 14, "Data Time GMT (DE 7 of QR OIG)", "N"),  # Format: YYYYMMDDhhmmss
}

# Bit 3007: Reversal Indicator
pde3007Format = {
    "s1": JCBCustomField(3007, "s1", 1, "Reversal Indicator", "A"),  # Always set to 'R'
    "s2": JCBCustomField(3007, "s2", 6, "Central Processing Date of Original Transaction", "N"),  # Format: YYMMDD
}

# Bit 3008: Card Acceptor Additional Information
pde3008Format = {
    "s1": JCBCustomField(3008, "s1", 16, "Customer Service Phone Number", "ANS"),
    "s2": JCBCustomField(3008, "s2", 16, "Card Acceptor Phone Number", "ANS"),
    "s3": JCBCustomField(3008, "s3", 255, "Card Acceptor URL", "ANS"),  # Variable length up to 255 characters
}

# If the transaction is an Installment transaction
pde3008InstallmentFormat = {
    "s1": JCBCustomField(3008, "s1", 16, "Customer Service Phone Number for Retailer", "ANS"),
    "s2": JCBCustomField(3008, "s2", 16, "Customer Service Phone Number for Installment Provider", "ANS"),
    "s3": JCBCustomField(3008, "s3", 255, "Installment Number and Total Number of Installments", "ANS"),  # Example: "PAYMENT 2 of 3"
}

# Bit 3009: EC Security Level Indicator
pde3009Format = {
    "s1": JCBCustomField(3009, "s1", 2, "EC Security Level Indicator", "N"),
}

# Bit 3011: Original Acquirer Reference Data
pde3011Format = {
    "s1": JCBCustomField(3011, "s1", 23, "Original Acquirer Reference Number", "ANS"),  # Variable length up to 23 characters
}

# Bit 3012: Original Card Acceptor Terminal ID
pde3012Format = {
    "s1": JCBCustomField(3012, "s1", 15, "Original Card Acceptor Terminal ID", "ANS"),  # Variable length 9 to 15 characters
}

# Bit 3013: Original Card Acceptor ID Code
pde3013Format = {
    "s1": JCBCustomField(3013, "s1", 16, "Original Card Acceptor ID Code", "ANS"),  # Fixed length 16 characters
}

# Bit 3014: Modified Acquirer Reference Data
pde3014Format = {
    "s1": JCBCustomField(3014, "s1", 23, "Reference Number", "N"),
}

# Bit 3021: ATM Access Fee Amount, Reconciliation
pde3021Format = {
    "s1": JCBCustomField(3021, "s1", 1, "Debit/Credit Indicator", "A"),
    "s2": JCBCustomField(3021, "s2", 3, "Currency Code", "N"),
    "s3": JCBCustomField(3021, "s3", 12, "ATM Access Fee Amount, Reconciliation;", "N"),
}

# Bit 3030: Transit Flag
pde3030Format = {
    "s1": JCBCustomField(3030, "s1", 2, "Transit Flag used for Mass Transit Transaction. ", "N"),
}

# Bit 3201: Dispute Control Number
pde3201Format = {
    "s1": JCBCustomField(3201, "s1", 11, "Dispute Control Number", "ANS"),
}

# Bit 3202: Retrieval Request Data
pde3202Format = {
    "s1": JCBCustomField(3202, "s1", 6, "Retrieval Processing Date", "N"),
    "s2": JCBCustomField(3202, "s2", 11, "Dispute Control Number", "ANS"),
    "s3": JCBCustomField(3202, "s3", 4, "Retrieval Reason Code", "ANS"),
}

# Bit 3203: Retrieval Document
pde3203Format = {
    "s1": JCBCustomField(3203, "s1", 1, "Document Number for Retrieval", "A"),
}

# Bit 3205: First Chargeback Reference Number
pde3205Format = {
    "s1": JCBCustomField(3205, "s1", 12, "First Chargeback Reference Number", "ANS"),
}

# Bit 3206: Chargeback Support Documentation Dates
pde3206Format = {
    "s1": JCBCustomField(3206, "s1", 6, "Date for First Chargeback (ISS)", "N"),
    "s2": JCBCustomField(3206, "s2", 6, "Date for Representment (ACQ)", "N"),
}

# Bit 3207: First Chargeback Return Data
pde3207Format = {
    "s1": JCBCustomField(3207, "s1", 4, "Reason Code of First Chargeback", "ANS"),
    "s2": JCBCustomField(3207, "s2", 6, "Date of the First Chargeback (YYMMDD)", "N"),
    "s3": JCBCustomField(3207, "s3", 12, "Amount of the First Chargeback", "N"),
    "s4": JCBCustomField(3207, "s4", 3, "Currency Code of the First Chargeback", "N"),
    "s5": JCBCustomField(3207, "s5", 1, "Exponents; Decimal Place of Currency Code", "N"),
}

# Bit 3208: Representment Reference Number
pde3208Format = {
    "s1": JCBCustomField(3208, "s1", 12, "Representment Reference Number (ACQ)", "ANS"),
}

# Bit 3209: Second Chargeback Support Documentation Date
pde3209Format = {
    "s1": JCBCustomField(3209, "s1", 6, "Date for Second Chargeback (ISS)", "N"),
}

# Bit 3210: Representment Resubmission Data
pde3210Format = {
    "s1": JCBCustomField(3210, "s1", 4, "Reason Code of Representment", "ANS"),
    "s2": JCBCustomField(3210, "s2", 6, "Date of Representment (YYMMDD)", "N"),
    "s3": JCBCustomField(3210, "s3", 12, "Amount of Representment", "N"),
    "s4": JCBCustomField(3210, "s4", 3, "Currency Code for the Amount of Representment", "N"),
    "s5": JCBCustomField(3210, "s5", 1, "Exponents; Decimal Place of Currency Code", "N"),
}

# Bit 3211: Second Chargeback Reference Number
pde3211Format = {
    "s1": JCBCustomField(3211, "s1", 12, "Second Chargeback Reference Number (ISS)", "ANS"),
}

# Bit 3250: Documentation Indicator
pde3250Format = {
    "s1": JCBCustomField(3250, "s1", 1, "Indicator if Supporting Documents are available", "N"),
}

# Bit 3251: Sender Memo
pde3251Format = {
    "s1": JCBCustomField(3251, "s1", 100, "Comments from Sender;", "ANS"),
}

# Bit 3302: Amount, Other
pde3302Format = {
    "s1": JCBCustomField(3302, "s1", 30, "ITEM Name", "ANS"),
    "s2": JCBCustomField(3302, "s2", 50, "Comments", "ANS"),
    "s3": JCBCustomField(3302, "s3", 1, "Credit/Debit Indicator", "A"),
    "s4": JCBCustomField(3302, "s4", 12, "Amount, Other", "N"),
    "s5": JCBCustomField(3302, "s5", 3, "Currency Code for Amount, Other", "N"),
    "s6": JCBCustomField(3302, "s6", 12, "Amount, Other, Reconciliation", "N"),
    "s7": JCBCustomField(3302, "s7", 3, "Currency Code", "N"), #Currency Code for Other Reconciliation
}

# Example values for s1 and s2 based on cases

def pde3302_get_s1_s2_values(case_type):
    """
    s1: ITEM Name; Left justified, filled with trailing spaces
    s2: Comments; Left justified, filled with trailing spaces
    s3: Credit/Debit Indicator; C for credit, D for debit
    """
    s1 = ""
    s2 = ""

    if case_type == "Expense":
        s1 = "EXPENSES".ljust(30)
        s2 = "FEE COLLECTION".ljust(50)
    elif case_type == "Offset":
        current_date = datetime.now().strftime('%m%d')
        s1 = "EXPENSES".ljust(30)
        s2 = f"OFFSET_{current_date}".ljust(50)
    elif case_type == "Periodic Fee":
        invoice_number = 'x' * 12  # Đảm bảo chiều dài số
        s1 = "FEE INVOICE".ljust(30)
        s2 = f"INVOICE NO:{invoice_number}".ljust(50)
    elif case_type == "Pre-Arbitration":
        s1 = "PRE ARBITRATION".ljust(30)
        s2 = "DCN: xx-xxxxxx-xxx".ljust(50)
    elif case_type == "Arbitration":
        s1 = "ARBITRATION".ljust(30)
        s2 = "DCN: xx-xxxxxx-xxx".ljust(50)
    else:
        raise ValueError("Unknown case type")

    return s1, s2

    
# Bit 3501: Date and Time, Verification
pde3501Format = {
    "s1": JCBCustomField(3501, "s1", 12, "Date and Time of Interchange File accepted and verified by JCBI Settlement System (YYMMDDhhmmss)", "N"),
}

# Bit 3502: Total Message Count
pde3502Format = {
    "s1": JCBCustomField(3502, "s1", 8, "Total Processed Count", "N"),
    "s2": JCBCustomField(3502, "s2", 8, "Total Erroneous Count", "N"),
}

# Bit 3503: Total Net Amount, in Transaction Currency
pde3503Format = {
    "s1": JCBCustomField(3503, "s1", 1, "Credit/Debit Indicator", "A"), # C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3503, "s2", 16, "Amount", "N"), #Total Amount in Transaction Currency
}

# Bit 3504: Total Credit Amount, in Transaction Currency
pde3504Format = {
    "s1": JCBCustomField(3504, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3504, "s2", 16, "Amount", "N"), #Total Credit Amount in Transaction Currency
}


# Bit 3505: Total Debit Amount, in Transaction Currency
pde3505Format = {
    "s1": JCBCustomField(3505, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3505, "s2", 16, "Amount", "N"), #Total Debit Amount in Transaction Currency
}

# Bit 3506: Presentment Message Count
pde3506Format = {
    "s1": JCBCustomField(3506, "s1", 8, "Presentment Total Processed Count", "N"),
    "s2": JCBCustomField(3506, "s2", 8, "Presentment Total Erroneous Count", "N"),
    "s3": JCBCustomField(3506, "s3", 8, "Presentment Retail Processed Count", "N"),
    "s4": JCBCustomField(3506, "s4", 8, "Presentment Refund Processed Count", "N"),
    "s5": JCBCustomField(3506, "s5", 8, "Presentment Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3506, "s6", 8, "Presentment ATM Processed Count", "N"),
    "s7": JCBCustomField(3506, "s7", 8, "Presentment Reversal Processed Count", "N"),
}

# Bit 3507: Presentment Net Amount, in Transaction Currency
pde3507Format = {
    "s1": JCBCustomField(3507, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3507, "s2", 16, "Amount", "N"), #Net Presentment Amount in Transaction Currency
}

# Bit 3508: Presentment Credit Amount, in Transaction Currency
pde3508Format = {
    "s1": JCBCustomField(3508, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3508, "s2", 16, "Amount", "N"), #Presentment Credit Amount in Transaction Currency
}

# Bit 3509: Presentment Debit Amount, in Transaction Currency
pde3509Format = {
    "s1": JCBCustomField(3509, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3509, "s2", 16, "Amount", "N"), #Presentment Debit Amount in Transaction Currency
}

# Bit 3510: First Chargeback (Full) Message Count
pde3510Format = {
    "s1": JCBCustomField(3510, "s1", 8, "First Chargeback (Full) Total Processed Count", "N"),
    "s2": JCBCustomField(3510, "s2", 8, "First Chargeback (Full) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3510, "s3", 8, "First Chargeback (Full) Retail Processed Count", "N"),
    "s4": JCBCustomField(3510, "s4", 8, "First Chargeback (Full) Refund Processed Count", "N"),
    "s5": JCBCustomField(3510, "s5", 8, "First Chargeback (Full) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3510, "s6", 8, "First Chargeback (Full) ATM Processed Count", "N"),
    "s7": JCBCustomField(3510, "s7", 8, "First Chargeback (Full) Reversal Processed Count", "N"),
}

# Bit 3511: First Chargeback (Full) Net Amount, in Transaction Currency
pde3511Format = {
    "s1": JCBCustomField(3511, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3511, "s2", 16, "Amount", "N"), #First Chargeback (Full) Amount in Transaction Currency
}


# Bit 3512: First Chargeback (Full) Credit Amount, in Transaction Currency
pde3512Format = {
    "s1": JCBCustomField(3512, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3512, "s2", 16, "(Full) Credit Amount", "N"), #First Chargeback (Full) Credit Amount in Transaction Currency
}

# Bit 3513: First Chargeback (Full) Debit Amount, in Transaction Currency
pde3513Format = {
    "s1": JCBCustomField(3513, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3513, "s2", 16, "(Full) Debit Amount", "N"), #First Chargeback (Full) Debit Amount in Transaction Currency
}

# Bit 3514: First Chargeback (Partial) Message Count
pde3514Format = {
    "s1": JCBCustomField(3514, "s1", 8, "First Chargeback (Partial) Total Processed Count", "N"),
    "s2": JCBCustomField(3514, "s2", 8, "First Chargeback (Partial) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3514, "s3", 8, "First Chargeback (Partial) Retail Processed Count", "N"),
    "s4": JCBCustomField(3514, "s4", 8, "First Chargeback (Partial) Refund Processed Count", "N"),
    "s5": JCBCustomField(3514, "s5", 8, "First Chargeback (Partial) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3514, "s6", 8, "First Chargeback (Partial) ATM Processed Count", "N"),
    "s7": JCBCustomField(3514, "s7", 8, "First Chargeback (Partial) Reversal Processed Count", "N"),
}

# Bit 3515: First Chargeback (Partial) Net Amount, in Transaction Currency
pde3515Format = {
    "s1": JCBCustomField(3515, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3515, "s2", 16, "(Partial) Amount", "N"), #First Chargeback (Partial) Amount in Transaction Currency
}

# Bit 3516: First Chargeback (Partial) Credit Amount, in Transaction Currency
pde3516Format = {
    "s1": JCBCustomField(3516, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3516, "s2", 16, "(Partial) Credit Amount", "N"), #First Chargeback (Partial) Credit Amount in Transaction Currency
}

# Bit 3517: First Chargeback (Partial) Debit Amount, in Transaction Currency
pde3517Format = {
    "s1": JCBCustomField(3517, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3517, "s2", 16, "(Partial) Debit Amount", "N"), #First Chargeback (Partial) Debit Amount in Transaction Currency
}


# Bit 3518: Representment (Full) Message Count
pde3518Format = {
    "s1": JCBCustomField(3518, "s1", 8, "Representment (Full) Total Processed Count", "N"),
    "s2": JCBCustomField(3518, "s2", 8, "Representment (Full) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3518, "s3", 8, "Representment (Full) Retail Processed Count", "N"),
    "s4": JCBCustomField(3518, "s4", 8, "Representment (Full) Refund Processed Count", "N"),
    "s5": JCBCustomField(3518, "s5", 8, "Representment (Full) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3518, "s6", 8, "Representment (Full) ATM Processed Count", "N"),
    "s7": JCBCustomField(3518, "s7", 8, "Representment (Full) Reversal Processed Count", "N"),
}

# Bit 3519: Representment (Full) Net Amount, in Transaction Currency
pde3519Format = {
    "s1": JCBCustomField(3519, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3519, "s2", 16, "Representment (Full) Amount", "N"), #Representment (Full) Amount in Transaction Currency
}

# Bit 3520: Representment (Full) Credit Amount, in Transaction Currency
pde3520Format = {
    "s1": JCBCustomField(3520, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3520, "s2", 16, "Representment (Full) Credit Amount", "N"), #Representment (Full) Credit Amount in Transaction Currency
}

# Bit 3521: Representment (Full) Debit Amount, in Transaction Currency
pde3521Format = {
    "s1": JCBCustomField(3521, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3521, "s2", 16, "Representment (Full) Debit Amount", "N"), #Representment (Full) Debit Amount in Transaction Currency
}

# Bit 3522: Representment (Partial) Message Count
pde3522Format = {
    "s1": JCBCustomField(3522, "s1", 8, "Representment (Partial) Total Processed Count", "N"),
    "s2": JCBCustomField(3522, "s2", 8, "Representment (Partial) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3522, "s3", 8, "Representment (Partial) Retail Processed Count", "N"),
    "s4": JCBCustomField(3522, "s4", 8, "Representment (Partial) Refund Processed Count", "N"),
    "s5": JCBCustomField(3522, "s5", 8, "Representment (Partial) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3522, "s6", 8, "Representment (Partial) ATM Processed Count", "N"),
    "s7": JCBCustomField(3522, "s7", 8, "Representment (Partial) Reversal Processed Count", "N"),
}

# Bit 3523: Representment (Partial) Net Amount, in Transaction Currency
pde3523Format = {
    "s1": JCBCustomField(3523, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3523, "s2", 16, "Representment (Partial) Amount", "N"), #Representment (Partial) Amount in Transaction Currency
}


# Bit 3524: Representment (Partial) Credit Amount, in Transaction Currency
pde3524Format = {
    "s1": JCBCustomField(3524, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3524, "s2", 16, "Representment (Partial) Credit Amount", "N"), #Representment (Partial) Credit Amount in Transaction Currency
}

# Bit 3525: Representment (Partial) Debit Amount, in Transaction Currency
pde3525Format = {
    "s1": JCBCustomField(3525, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3525, "s2", 16, "Representment (Partial) Debit Amount", "N"), #Representment (Partial) Debit Amount in Transaction Currency
}

# Bit 3526: Second Chargeback (Full) Message Count
pde3526Format = {
    "s1": JCBCustomField(3526, "s1", 8, "Second Chargeback (Full) Total Processed Count", "N"),
    "s2": JCBCustomField(3526, "s2", 8, "Second Chargeback (Full) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3526, "s3", 8, "Second Chargeback (Full) Retail Processed Count", "N"),
    "s4": JCBCustomField(3526, "s4", 8, "Second Chargeback (Full) Refund Processed Count", "N"),
    "s5": JCBCustomField(3526, "s5", 8, "Second Chargeback (Full) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3526, "s6", 8, "Second Chargeback (Full) ATM Processed Count", "N"),
    "s7": JCBCustomField(3526, "s7", 8, "Second Chargeback (Full) Reversal Processed Count", "N"),
}


# Bit 3527: Second Chargeback (Full) Net Amount, in Transaction Currency
pde3527Format = {
    "s1": JCBCustomField(3527, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for amount more than zero, D for amount less than zero
    "s2": JCBCustomField(3527, "s2", 16, "Second Chargeback (Full) Amount", "N"), #Second Chargeback (Full) Amount in Transaction Currency
}

# Bit 3528: Second Chargeback (Full) Credit Amount, in Transaction Currency
pde3528Format = {
    "s1": JCBCustomField(3528, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; C for credit amount
    "s2": JCBCustomField(3528, "s2", 16, "Second Chargeback (Full) Credit Amount", "N"), #Second Chargeback (Full) Credit Amount in Transaction Currency
}

# Bit 3529: Second Chargeback (Full) Debit Amount, in Transaction Currency
pde3529Format = {
    "s1": JCBCustomField(3529, "s1", 1, "Credit/Debit Indicator", "A"), #Credit/Debit Indicator; D for debit amount
    "s2": JCBCustomField(3529, "s2", 16, "Second Chargeback (Full) Debit Amount", "N"), #Second Chargeback (Full) Debit Amount in Transaction Currency
}

# Bit 3530: Second Chargeback (Partial) Message Count
pde3530Format = {
    "s1": JCBCustomField(3530, "s1", 8, "Second Chargeback (Partial) Total Processed Count", "N"),
    "s2": JCBCustomField(3530, "s2", 8, "Second Chargeback (Partial) Total Erroneous Count", "N"),
    "s3": JCBCustomField(3530, "s3", 8, "Second Chargeback (Partial) Retail Processed Count", "N"),
    "s4": JCBCustomField(3530, "s4", 8, "Second Chargeback (Partial) Refund Processed Count", "N"),
    "s5": JCBCustomField(3530, "s5", 8, "Second Chargeback (Partial) Manual Cash Processed Count", "N"),
    "s6": JCBCustomField(3530, "s6", 8, "Second Chargeback (Partial) ATM Processed Count", "N"),
    "s7": JCBCustomField(3530, "s7", 8, "Second Chargeback (Partial) Reversal Processed Count", "N"),
}

# Bit 3531: Second Chargeback (Partial) Net Amount in Transaction Currency
pde3531Format = {
    "s1": JCBCustomField(3531, "s1", 1, "Credit / Debit indicator", "A"),
    "s2": JCBCustomField(3531, "s2", 16, "Second Chargeback (Partial) Amount in Transaction Currency", "N"),
}

# Bit 3532: Second Chargeback (Partial) Credit Amount in Transaction Currency
pde3532Format = {
    "s1": JCBCustomField(3532, "s1", 1, "Credit / Debit indicator", "A"),
    "s2": JCBCustomField(3532, "s2", 16, "Second Chargeback (Partial) Credit Amount in Transaction Currency", "N"),
}

# Bit 3533: Second Chargeback (Partial) Debit Amount in Transaction Currency
pde3533Format = {
    "s1": JCBCustomField(3533, "s1", 1, "Credit / Debit indicator", "A"),
    "s2": JCBCustomField(3533, "s2", 16, "Second Chargeback (Partial) Debit Amount in Transaction Currency", "N"),
}


# đến trang 140


# Bit 3717: Auto Rental Audit Adjustment Amount
pde3717Format = {
    "s1": JCBCustomField(3717, "s1", 12, "Auto Rental Audit Adjustment Amount", "N"),
}

# Bit 3901: File ID
pde3901Format = {
    "s1": JCBCustomField(3901, "s1", 3, "File Type", "N"), #File Type; 001 for Incoming Interchange File, 002 for Outgoing Interchange File, 003 for Verification Result File, 004 for Settlement Result File
    "s2": JCBCustomField(3901, "s2", 6, "File Reference Date", "N"), #File Reference Date in YYMMDD format
    "s3": JCBCustomField(3901, "s3", 11, "Processor ID / Licensee ID", "N"), #Processor ID / Licensee ID; Front 0 filling
    "s4": JCBCustomField(3901, "s4", 5, "File Sequence Number", "N"), #File Sequence Number; SEQ No. of the Interchange File
}

# Bit 3902: Total Transaction Amount
pde3902Format = {
    "s1": JCBCustomField(3902, "s1", 16, "Total Transaction Amount", "N"),
}

# Bit 3903: TNumber of Messages
pde3903Format = {
    "s1": JCBCustomField(3903, "s1", 8, "Number of Messages", "N"),
}

# Bit 3904: Original Message Number
pde3904Format = {
    "s1": JCBCustomField(3904, "s1", 8, "Original Message Number", "N"),
}

class pde:
    def __init__(self,tag:str, datatype:str, length:int, name:str,pdeType:dict[str,JCBCustomField], prefix =  None):
        self.tag = tag
        self.datatype = datatype
        self.length = length
        self.name = name
        self.pdeType = pdeType
        self.prefix = prefix


# PDE Field Definitions
pde_fields = {
    3001: pde("PDE3001","ANS",3,"JCB Int'l Product / Grade Identifier",pde3001Format),
    3002: pde("PDE3002","AN",60,"Currency Exponents",pde3002Format,"LLL" ),
    3003: pde("PDE3003","ANS",25,"Clearing Data",pde3003Format),
    3004: pde("PDE3004","AN",4,"Sub-LCID",pde3004Format),
    3005: pde("PDE3005", "ANS", 570, "Amounts, Transaction Fees", pde3005Format,"LLL"),
    3006: pde("PDE3006", "ANS", 60, "Additional Info", pde3006Format,"LLL"),
    3007: pde("PDE3007", "ANS", 7, "Reversal Indicator", pde3007Format),
    3008: pde("PDE3008", "AN", 287, "Card Acceptor Additional Information", pde3008Format,"LLL"),
    3009: pde("PDE3009", "NS", 2, "EC Security Level Indicator", pde3009Format),
    3011: pde("PDE3011", "ANS", 23, "Original Acquirer Reference Data", pde3011Format, "LLL"),
    3012: pde("PDE3012", "ANS", 15, "Original Card Acceptor Terminal ID", pde3012Format,"LLL"),
    3013: pde("PDE3013", "ANS", 16, "Original Card Acceptor ID Code", pde3013Format),
    3014: pde("PDE3014", "N", 23, "Modified Acquirer Reference Data", pde3014Format),
    3021: pde("PDE3021", "AN", 16, "ATM Access Fee Amount, Reconciliation", pde3021Format),
    3030: pde("PDE3030", "N", 2, "Transit Flag", pde3030Format),
    3201: pde("PDE3201", "ANS", 11, "Transit Flag", pde3201Format,"LLL"),
    3202: pde("PDE3202", "AN", 21, "Retrieval Request Data", pde3202Format,"LLL"),
    3203: pde("PDE3203", "AN", 1, "Retrieval Document", pde3203Format),
    3205: pde("PDE3205", "ANS", 12, "First Chargeback Reference Number", pde3205Format),
    3206: pde("PDE3206", "NS", 12, "Chargeback Support Documentation Dates", pde3206Format),
    3207: pde("PDE3207", "ANS", 26, "First Chargeback Return Data", pde3207Format),
    3208: pde("PDE3208", "ANS", 12, "Representment Reference Number", pde3208Format),
    3209: pde("PDE3209", "N", 6, "Second Chargeback Support Documentation Date", pde3209Format),
    3210: pde("PDE3210", "ANS", 26, "Representment Resubmission Data", pde3210Format,"LLL"),
    3211: pde("PDE3211", "ANS", 12, "Second Chargeback Reference Number", pde3211Format),
    3250: pde("PDE3250", "N", 1, "Documentation Indicator", pde3250Format),
    3251: pde("PDE3251", "ANS", 100, "Sender Memo", pde3251Format,"LLL"),
    3302: pde("PDE3302", "ANS", 111, "Amount, Other", pde3302Format),
    3501: pde("PDE3501", "N", 12, "Date and Time, Verification", pde3501Format),
    3502: pde("PDE3502", "N", 16, "Total Message Count", pde3502Format),
    3503: pde("PDE3503", "AN", 17, "Total Net Amount, in Transaction Currency", pde3503Format),
    3504: pde("PDE3504", "AN", 17, "Total Credit Amount, in Transaction Currency", pde3504Format),
    3505: pde("PDE3505", "AN", 17, "Total Debit Amount, in Transaction Currency", pde3505Format),
    3506: pde("PDE3506", "N", 56, "Presentment Message Count", pde3506Format),
    3507: pde("PDE3507", "N", 17, "Presentment Net Amount, in Transaction Currency", pde3507Format),
    3508: pde("PDE3508", "N", 17, "Presentment Credit Amount, in Transaction Currency", pde3508Format),
    3509: pde("PDE3509", "N", 17, "Presentment Debit Amount, in Transaction Currency", pde3509Format),
    3510: pde("PDE3510", "N", 56, "First Chargeback (Full) Message Count", pde3510Format),
    3511: pde("PDE3511", "N", 17, "First Chargeback (Full) Net Amount, in Transaction Currency", pde3511Format),
    3512: pde("PDE3512", "N", 17, "First Chargeback (Full) Credit Amount, in Transaction Currency", pde3512Format),
    3513: pde("PDE3513", "N", 17, "First Chargeback (Full) Debit Amount, in Transaction Currency", pde3513Format),
    3514: pde("PDE3514", "N", 56, "First Chargeback (Partial) Message Count", pde3514Format),
    3515: pde("PDE3515", "N", 17, "First Chargeback (Partial) Net Amount, in Transaction Currency", pde3515Format),
    3516: pde("PDE3516", "N", 17, "First Chargeback (Partial) Credit Amount, in Transaction Currency", pde3516Format),
    3517: pde("PDE3517", "N", 17, "First Chargeback (Partial) Debit Amount, in Transaction Currency", pde3517Format),
    3518: pde("PDE3518", "N", 56, "Representment (Full) Message Count", pde3518Format),
    3519: pde("PDE3519", "N", 17, "Representment (Full) Net Amount, in Transaction Currency", pde3519Format),
    3520: pde("PDE3520", "N", 17, "Representment (Full) Credit Amount, in Transaction Currency", pde3520Format),
    3521: pde("PDE3521", "N", 17, "Representment (Full) Debit Amount, in Transaction Currency", pde3521Format),
    3522: pde("PDE3522", "N", 56, "Representment (Partial) Message Count", pde3522Format),
    3523: pde("PDE3523", "N", 17, "Representment (Partial) Net Amount, in Transaction Currency", pde3523Format),
    3524: pde("PDE3524", "N", 17, "Representment (Partial) Credit Amount, in Transaction Currency", pde3524Format),
    3525: pde("PDE3525", "N", 17, "Representment (Partial) Debit Amount, in Transaction Currency", pde3525Format),
    3526: pde("PDE3526", "N", 56, "Second Chargeback (Full) Message Count", pde3526Format),
    3527: pde("PDE3527", "N", 17, "Second Chargeback (Full) Net Amount, in Transaction Currency", pde3527Format),
    3528: pde("PDE3528", "N", 17, "Second Chargeback (Full) Credit Amount, in Transaction Currency", pde3528Format),
    3529: pde("PDE3529", "N", 17, "Second Chargeback (Full) Debit Amount, in Transaction Currency", pde3529Format),
    3530: pde("PDE3530", "N", 56, "Second Chargeback (Partial) Message Count", pde3530Format),
    3531: pde("PDE3531", "N", 17, "Second Chargeback (Partial) Net Amount, in Transaction Currency", pde3531Format),
    3532: pde("PDE3532", "N", 17, "Second Chargeback (Partial) Credit Amount, in Transaction Currency", pde3532Format),
    3533: pde("PDE3533", "N", 17, "Second Chargeback (Partial) Debit Amount, in Transaction Currency", pde3533Format),

    3717: pde("PDE3717", "N", 12, "Auto Rental Audit Adjustment Amount", pde3717Format),
    3901: pde("PDE3901", "N", 25, "File ID", pde3901Format),
    3902: pde("PDE3902", "N", 16, "Total Transaction Amount", pde3902Format),
    3903: pde("PDE3903", "N", 8, "Number of Messages", pde3903Format),
    3904: pde("PDE3904", "N", 8, "Original Message Number", pde3904Format),
}

