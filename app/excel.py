import os
import re
import shutil
import pandas
from datetime import datetime, timezone

from app.db import Database

class ExcelExtractor:    

    @staticmethod
    def extract(dir, spreadsheet) -> list:
        files = os.listdir(dir)                
        
        for file in files:

            if os.path.isfile(os.path.join(dir, file)):      
                
                file_path = os.path.join(dir, file)                
                date_time = ExcelExtractor.extract_date(os.path.getmtime(file_path))
                file_name, file_extension = os.path.splitext(file)                                                            

                if file_extension == '.xlsx':

                    file_pending_path = os.path.join(dir, f'pending_{file_name}{date_time}{file_extension}')
                    file_error_path = os.path.join(dir, 'error', f'error_{file_name}{date_time}{file_extension}')                                           
                    file_success_path = os.path.join(dir, 'success', f'success_{file_name}{date_time}{file_extension}') 

                    try:                                                                             
                        
                        os.rename(file_path, file_pending_path)                        

                        db = Database(f'table_{date_time}', [                            
                            'NUMPAL TEXT', 
                            'INTERFACE TEXT', 
                            'MENSAGEM TEXT', 
                            'QUANTIDADE TEXT', 
                            'ORIGEM TEXT',
                            'DESTINO TEXT',
                            'DATA TEXT',
                            'VARMSG TEXT',
                            'NUMEXC TEXT'                            
                        ])     

                        all_data = []

                        df = pandas.read_excel(file_pending_path, sheet_name=spreadsheet, header=1)      
                        for index, row in df.iterrows():
                            all_data.append({
                                'NUMPAL' : row['NUMPAL'],
                                'INTERFACE' : row['INTERFACE'],
                                'MENSAGEM' : row['MENSAGEM'],
                                'QUANTIDADE' : row['QUANTIDADE'],
                                'ORIGEM' : row['ORIGEM'],
                                'DESTINO' : row['DESTINO'],
                                'DATA' : row['DATA'],
                                'VARMSG' : row['VARMSG'],
                                'NUMEXC' : row['NUMEXC']})   
                                                                                                                                                                  
                        db.insert_data(all_data)  
                        all = db.all()
                        shutil.move(file_pending_path, file_success_path)                          

                        return all   
                        
                    except Exception as e:                        
                        os.rename(file_pending_path, file_error_path)
                        raise e                    

    @staticmethod            
    def extract_date(date):
        date_formated =  datetime.fromtimestamp(date, timezone.utc)
        return re.sub(r'\D', '', str(date_formated))        