import pandas as pd
from utilities import Utils

class VpbTransformData:
    def __init__(self):
        """
        """

    def __enter__(self):
        return self
    
    def __del__(self):
        """"""

    def __exit__(self, exc_type, exc_val, exc_tb):

        """"""

    

    
        
    def __parseContent(self, text):
        parts = text.split()
        data = {}
        for i in range(len(parts)):
            part = parts[i]
            if part == "TT":
                if parts[i + 2] == "DEB":
                    data["CARD_TYPE"] = parts[i + 1] + " " + parts[i + 2]
                else:
                    data["CARD_TYPE"] = parts[i + 1]
            elif part == "TID":
                data["TERMINAL_ID"] = parts[i + 1]
            elif part == "GD" and parts[i - 1] == "NGAY":
                data["TRANS_DATE"] = Utils.parseDate(parts[i + 1] + " " + parts[i + 2])
            elif part == "THE" and parts[i - 1] == "SO":
                data["CARD_NUMBER"] = parts[i+1]
            elif part == "CODE":
                data["AUTH_CODE"] = parts[i+1]
            elif part == "TIEN" and parts[i - 1] == "SO":
                data["TRANS_AMOUNT"] = Utils.convertStrToNumber(parts[i+1].replace("VND",""))
            elif part == "PHI":
                data["FEE_AMOUNT"] = Utils.convertStrToNumber(parts[i+1].replace("VND",""))
            elif part == "VAT":
                data["VAT_AMOUNT"] = Utils.convertStrToNumber(parts[i+1].replace("VND",""))
            elif part == "RRN":
                data["RRN"] = parts[i+1]
            

        return data
    # end parseContent

    def transform(self, dfImp: pd.DataFrame) -> pd.DataFrame:
        try:
            # add column with parse func
            for col_name in self.__parseContent(dfImp.IMPORT_CONTENT[0]).keys(): 
                dfImp[col_name] = ""
            # Parse content and add value
            for index, row in dfImp.iterrows():
                parsed_data = self.__parseContent(row["IMPORT_CONTENT"])
                for col_name, value in parsed_data.items():
                    dfImp.loc[index, col_name] = value
            return dfImp
        except Exception as e:
            raise Exception (f'transform data is Error: {e}')
    # end transform
