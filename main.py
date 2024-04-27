from app.excel import ExcelExtractor
from app.sheets import SheetData

def main():
    try:

      sheets = SheetData();
      sheets.insert('excel_extract', 'Página1', ExcelExtractor.extract('temp', 'Sheet1'))
      print("FINANALIZADO.");
       
    except Exception as e:
       print(e)        

if __name__ == "__main__":
 main()