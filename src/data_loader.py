import pandas as pd

class AnimeDataLoader:
    def __init__(self,original_csv:str, processed_csv:str):
        self.original_csv = original_csv
        self.processed_csv = processed_csv

    def load_and_process(self):
        # on_bad_lines = 'skip' : bỏ qua những dòng thoại không hay mà không cần nhắc nhở hay cảnh báo khi gặp phải.
        df = pd.read_csv(self.original_csv, encoding='utf-8', on_bad_lines='skip').dropna()
        required_cols = {'Name', 'Genres', 'sypnopsis'}
        # set(df.columns) = ['Name', 'Genres', 'sypnopsis', 'mail_id']
        # kiểu như nếu tất cả các phần tử trong required_cols có trong set(df.columns) thì missing =[] - rỗng 
        # nếu thiếu 1 phần tử nào đó thì missing sẽ chứa phần tử thiếu
        missing = required_cols - set(df.columns)  # phép toán Relative Complement (phần bù) - Lấy tất cả các phần tử có trong required_cols nhưng không có trong set(df.columns)
    
        if missing:
            raise ValueError('Missing column in CSV file')
        
        df['combine_info'] = (
            'Title: ' + df['Name'] + ' .. Overview: ' + df['sypnopsis'] + ' Genres: ' + df['Genres']
        )

        df[['combine_info']].to_csv(self.processed_csv, index=False, encoding='utf-8') 
        # [['combine...']] dấu [] mở đầu là tạo 1 khung dữ liệu mới với ['combine..'] là dữ liệu dùng để cho vào khung đó và lưu vào file mới sau khi xử lý
        # index = False để nó không tạo ra thêm cột nào khác

        return self.processed_csv