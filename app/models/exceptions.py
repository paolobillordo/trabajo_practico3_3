from flask import jsonify

class CustomException(Exception):

    def __init__(self, status_code, name = "Custom Error", description = 'Error'): 
        super().__init__()
        self.description = description
        self.name = name
        self.status_code = status_code

    def get_response(self):
        response = jsonify({
            'error': {
                'code': self.status_code,
                'name': self.name,
                'description': self.description,
            }
        })
        response.status_code = self.status_code
        return response
    
class FilmNotFound(CustomException):
    
    def __init__(self, description = "Film with id {film_id} not found", name = "FilmNotFound", status_code = 404):
        super().__init__(status_code, name, description)


class InvalidDataError(CustomException):
    
    def __init__(self, description = "The data entered is incorrect", name = "InvalidDataError", status_code = 400):
        super().__init__(status_code, name, description)
        
    