from ..iso8503_utils import ISO8583Field
from .jcb_custom_field import JCBCustomField
from .jcb_bitmap import JCBfields
from .jcb_extension_format import bit55Format, bit54Format, bit43Format, bit97Format
from ..iso8503_utils import ISO8583Utils
from .jcb_pde_format import pde_fields
from ..iso8503_utils import ISO8583Parser
from typing import Dict
class JCBParser(ISO8583Parser):

    def __init__(self, fields: dict[str, ISO8583Field] = JCBfields):
        super().__init__(fields)
        

    
    def custom_field_switcher(self,fieldNumber, data):
        """
        Override default parse func
        """
        if fieldNumber == 43:
            # return self.parse_field_43(data)
            return self.custom_field_decoder(data,bit43Format)
        elif fieldNumber == 54:
            # return self.parse_field_54(data,bit54Format)
            return self.custom_field_decoder(data,bit54Format)
        elif fieldNumber == 97:
            return self.custom_field_decoder(data,bit97Format)
        

        return data
    # parse_custom_field

    def custom_field_decoder(self,msg,msgType:dict[str,JCBCustomField])->list:
        content = []
        if msg is None:
            return content
        length = len(msg)
        if length == 0:
            return content
        
        index = 0
        while index < length:
            for key,item in msgType.items():
                data = msg[index:item.length]
                index += item.length
                if data is not None and len(data) > 0:
                    content.append(
                        {
                            "Field": key,
                            "Length": item.length,
                            "Data": data,
                            "Description": item.description
                        }
                    )

            # end for
        # end while
        return content
    # end customFieldDecode
            

    def parse_additional_field(self, fieldNumber, msg:bytes) -> list:
        pde_data = []
        index = 0
        length = len(msg)
        while index < length:
            pde_tag = msg[index:index+4]
            index += 4
            tag = int(pde_tag.decode('ascii'))
            pdeItem = pde_fields.get(tag)
            if pdeItem is not None:
                if pdeItem.prefix is not None and pdeItem.prefix == "LLL":
                    if index + 3 <= len(msg):
                        len_of_pde = int(msg[index:index + 3].decode('ascii'))
                        index += 3
                    else:
                        raise ValueError(f"Invalid length for field {fieldNumber}")
                else:
                    index += 3
                    len_of_pde = pdeItem.length
                # end if check prefix

                if index + len_of_pde <= len(msg):
                    content = self.custom_field_decoder(msg[index:index + length],pdeItem.pdeType)
                    index += len_of_pde
                    if content is not None and len(content) > 0 :
                        pde_data.append(
                            {
                                "Tag": pdeItem.tag,
                                "Length": len_of_pde,
                                "Value": content,
                                "Description": pdeItem.name
                            }
                        )

                else:
                    raise ValueError(f"Invalid length for field {fieldNumber}")

           
            # end while

        return pde_data

    def parse_field_43(self, data) -> list:
        bit43_data = []
        index = 0
        length = len(data)
        while index < length:
            for tag, custom_field in bit43Format.items():
                value = data[index:index + custom_field.length]
                index += custom_field.length
                bit43_data.append(
                                    {
                                        "Tag": tag,
                                        "Length": custom_field.length,
                                        "Value": custom_field.parse_value(value),
                                        "Description": custom_field.description
                                    }
                                )
        return bit43_data

    def parse_field_54(self,data) -> list:
        """
        Amounts, Additional (For DCC transaction and ATM Access Fee transaction)
            s1; Account Type; n 2
                00: Fixed value
            s2; Amount Type; n 2
                42: ATM Access Fee
                58: DCC
            s3; Currency Code; n 3
                - ATM Access Fee: Transaction Currency Code (same as Bit49)
                - DCC: Local Currency Code
            s4; Sign; a 1
                * Outgoing / Incoming Interchange Message
                    ‘D’: Retail, Manual Cash, ATM, Refund Reversal
                    ‘C’: Refund, Retail Reversal, Manual Cash Reversal, ATM Reversal
                * Reconciliation Data
                    ‘D’: Debit to Licensee
                    ‘C’: Credit to Licensee
            s5; Amount; n 12
                - ATM Access Fee: ATM Access Fee amount in Transaction Currency
                - DCC: Transaction Amount in Local Currency
                
            Decimal place must be consistent with Currency Definition in JRP Code List.
            NOTE: Even 6 sets of Bit54 can be set per transaction, currently Bit54 is used for DCC
            and ATM Access Fee transaction only
            NOTE: In the case of DCC, set the same value as the Presentment in Chargeback /
            Representment.
            NOTE: In the case of ATM Access Fee
            * Need prior approval from JCBI to set.
            * Can be set only in ATM Cash Advance Transactions whose Processing Code (Bit3) is
            ‘010000’
            .
            * ATM Access Fee amount must be less than the Transaction Amount (Bit4).
            * Only one ATM Access Fee information can be set in a single ATM Cash Advance
            Transaction.
            * In a Full Chargeback / Representment, ATM Access Fee must be same as it of the
            original Presentment transaction.
            * In a Partial Chargeback / Representment, ATM Access Fee must not be set.
        """
        length = len(data)
        
        # Initialize index to start parsing
        index = 0
        bit54_data = []
        
        while index < length:
            # Extract Account Type (2 bytes)
            # parse s1
            account_type = data[index:index+bit54Format["s1"].length]
            index += bit54Format["s1"].length

            bit54_data.append(
                {
                    "Tag": bit54Format["s1"].tag,
                    "Length": bit54Format["s1"].length,
                    "Value": bit54Format["s1"].parse_value(account_type),
                    "Description": bit54Format["s1"].description
                }
            )
            
            # Extract Amount Type (2 bytes)
            # parse s2
            amount_type = data[index:index+bit54Format["s2"].length]
            index += bit54Format["s2"].length

            amount_type_decode = bit54Format["s2"].parse_value(amount_type)
            
            # Check value of s2, define description for s2 and s3
            if amount_type_decode == '42':
                amount_type_desc = 'ATM Access Fee'
                currency_code_desc = f'{amount_type_desc}: Transaction Currency Code (same as Bit49)'
                amount_desc = f'{amount_type_desc}: ATM Access Fee amount in Transaction Currency'
            elif amount_type_decode == '58':
                amount_type_desc = 'DCC'
                currency_code_desc = f'{amount_type_desc}: Local Currency Code'
                currency_code_desc = f'{amount_type_desc}: Transaction Amount in Local Currency'
            else:
                amount_type_desc = None
                currency_code_desc = None
                amount_desc = None
            # f'{bit54Format["s2"].description}{' (' if amount_type_desc is not None else ''} {amount_type_desc} {')' if amount_type_desc is not None else ''}'
            bit54_data.append(
                {
                    "Tag": bit54Format["s2"].tag,
                    "Length": bit54Format["s2"].length,
                    "Value": bit54Format["s2"].parse_value(amount_type),
                    "Description": bit54Format["s2"].description
                }
            )
            
            # Extract Currency Code (3 bytes)
            # parse s3
            currency_code = data[index:index+bit54Format["s3"].length]
            index += bit54Format["s3"].length
            # f'{bit54Format["s3"].description}{' (' if currency_code_desc is not None else ''} {currency_code_desc} {')' if currency_code_desc is not None else ''}'
            bit54_data.append(
                {
                    "Tag": bit54Format["s3"].tag,
                    "Length": bit54Format["s3"].length,
                    "Value": bit54Format["s3"].parse_value(currency_code),
                    "Description": bit54Format["s3"].description
                }
            )


            # Extract Sign (1 byte)
            # parse s4
            sign = data[index:index+bit54Format["s4"].length]
            index += bit54Format["s4"].length

            sign_decode = bit54Format["s4"].parse_value(sign)
            
            # Check value of s2, define description for s2 and s3
            if sign_decode == 'D':
                sign_desc = bit54Format["s4"].description + '(Reconciliation Data:Debit to License| Outgoing / Incoming Interchange Message: Retail, Manual Cash, ATM, Refund Reversal)'
            elif sign_decode == 'C':
                sign_desc = bit54Format["s4"].description + '(Reconciliation Data:Credit to License|Outgoing / Incoming Interchange Message: Refund, Retail Reversal, Manual Cash Reversal, ATM Reversal)'
            else:
                sign_desc = bit54Format["s4"].description

            bit54_data.append(
                {
                    "Tag": bit54Format["s4"].tag,
                    "Length": bit54Format["s4"].length,
                    "Value": bit54Format["s4"].parse_value(sign),
                    "Description": sign_desc
                }
            )
            
            # Extract Amount (12 bytes)
            # parse s5
            amount = data[index:index+bit54Format["s5"].length]
            index += bit54Format["s5"].length

            # f'{bit54Format["s5"].description}{' (' if amount_desc is not None else ''} {amount_desc} {')' if amount_desc is not None else ''}'
            bit54_data.append(
                {
                    "Tag": bit54Format["s5"].tag,
                    "Length": bit54Format["s5"].length,
                    "Value": bit54Format["s5"].parse_value(amount),
                    "Description": bit54Format["s5"].description
                }
            )
            
         
        
        return bit54_data
    # parse_field_54

    def parse_field_55(self, tag, length, value, description: None) -> dict:
        """
        This field must be filled with IC card information by setting up s1-s3 for each necessary
        Tag.
            s1; Tag Number
                Contains the tag value indicating the EMV data element as specified in the
                EMV ’96 specification.
            s2; Length
                Contains the length in bytes of the following “s3; Value”.
            s3;Value
                Contains the data as defined in each tag data specification.
                (i.e.) Transaction Currency Code
            s1: Tag: 5F2A
            s2: Length: 2
            s3: Value: 392
            5F2A020392 (in hexadecimal)
        NOTE: In Charge
        """
        element =  {
            "Tag": tag,
            "Length": length,
            "Value": value,
            "Description": description
        }
        if tag not in bit55Format:
            return element
        
        fieldValue = bit55Format[tag]

        element["Description"] = fieldValue.description
        element["Value"] = fieldValue.parse_value(value)

        return element
    
    # parse_field_55

    def parse_field_97(self, data) -> list:
        # Khởi tạo chỉ mục để bắt đầu phân tích
        index = 0

        # s1: Credit/Debit Indicator (1 byte)
        credit_debit_indicator = data[index:index+1].decode('ascii')
        index += 1
        
        # s2: Net Amount in Reconciliation Currency (16 bytes)
        net_amount = data[index:index+16].decode('ascii')
        
        # Lưu trữ dữ liệu phân tích
        bit97_data = {
            'Credit/Debit Indicator': credit_debit_indicator,
            'Net Amount in Reconciliation Currency': net_amount
        }
        
        return bit97_data
    
    # parse_field_97

    
    def parseTLVContent(self,bit, tag, length, value, description: None) -> dict:
        """(Tag-Length-Value)
        Override parsor class
        return dict 
        {
            "Tag": tag,
            "Length": length,
            "Value": value,
            "Description": description,
        }
        Tag, Length, Value >>> TLV
        """
        dictElementData = {
                "Tag": tag,
                "Length": length,
                "Value": value,
                "Description": description
                }
        if bit == 55:
            return self.parse_field_55(tag, length, value, description)
        # end check field 55  
       
        return dictElementData

    def iso_decode(self, message) ->  Dict[int,dict[str,ISO8583Field]]:
        
        data: Dict[int,dict[str,ISO8583Field]] = {}
        if message is None:
            return data
        lenOfMsg = len(message)
        if lenOfMsg == 0:
            return data
        
        msgNum = 0
        start = 0
        while lenOfMsg > 0:
            print(f'len of Msg: {lenOfMsg}')
            # Ví dụ sử dụng
            
            parsed_message,start = self.parseISOMessage(message)
            message=message[start:lenOfMsg]
            lenOfMsg = len(message)
            if ISO8583Utils.dict_has_data(parsed_message):
                msgNum += 1
                # parsed_message["remain_len"] = lenOfMsg
                data[msgNum] = parsed_message
        # end while
        return data

    # iso_decode
    
    def parse_msg_to_iso_str(self, message) -> Dict[int,str]:
        
        data: Dict[int,str] = {}
        if message is None:
            return data
        lenOfMsg = len(message)
        if lenOfMsg == 0:
            return data
        
        msgNum = 0
        start = 0
        while lenOfMsg > 0:
            print(f'len of Msg: {lenOfMsg}')
            parsed_message,start = self.parse_full_iso_message(message)
            message=message[start:lenOfMsg]
            lenOfMsg = len(message)
            if parsed_message:
                msgNum += 1
                # parsed_message["remain_len"] = lenOfMsg
                data[msgNum] = parsed_message
        # end while
        return data

    # parse_msg_to_iso_str
    
    
