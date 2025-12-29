import sys

class CustomException(Exception):
    def __init__(self, message:str, error_detail: Exception=None):
        self.error_message = self.get_error_message(message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def get_error_message(message: str, error_detail: Exception) -> str:
        _, _, exc_tb = sys.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename 
        line_number = exc_tb.tb_lineno
        return (
            f'{message} |'
            f'Error Detail: {str(error_detail)} |'
            f'File name: {file_name} |'
            f'Line: {line_number}'
        )

    def __str__(self):
        return self.error_message
