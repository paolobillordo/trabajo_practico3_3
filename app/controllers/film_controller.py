from ..models.film_model import Film
from flask import request
from decimal import Decimal
from ..models.exceptions import FilmNotFound, InvalidDataError

class FilmController:
    """Film controller class"""

    @classmethod
    def get(cls, film_id):
        """Get a film by id"""
        film = Film(film_id=film_id)
        result = Film.get(film)
        if result is None:
            raise FilmNotFound(f"Film with id {film_id} not found")
        else:
            return result.serialize(), 200
        
    @classmethod
    def get_all(cls):
        """Get all films"""
        film_objects = Film.get_all()
        films = []
        for film in film_objects:
            films.append(film.serialize())
        return films, 200
    
    @classmethod
    def create(cls):
        """Create a new film"""
        data = request.json
        # TODO: Validate data
        if len(data.get('title')) < 3:
            raise InvalidDataError("title must have 3 or more characters")
        if not isinstance(data.get('language_id'), int):
            raise InvalidDataError("language_id must be an integer")
        if not isinstance(data.get('rental_duration'), int):
            raise InvalidDataError("rental_duration must be an integer")
        if not isinstance(data.get('rental_rate'), int):
            raise InvalidDataError("rental_rate must be an integer")
        if not isinstance(data.get('replacement_cost'), int):
            raise InvalidDataError("replacement_cost must be an integer")
        if isinstance(data.get('special_features'), list):
            for i in data.get('special_features'):
                if i not in ["Trailers", "Commentaries", "Deleted Scenes", "Behind the Scenes"]:
                    raise InvalidDataError("Invalid spacial_features")
        else:
            raise InvalidDataError("spacial_features must be a list")
        
        if data.get('rental_rate') is not None:
            if isinstance(data.get('rental_rate'), int):
                data['rental_rate'] = Decimal(data.get('rental_rate'))/100
        
        if data.get('replacement_cost') is not None:
            if isinstance(data.get('replacement_cost'), int):
                data['replacement_cost'] = Decimal(data.get('replacement_cost'))/100
        

        film = Film(**data)
        Film.create(film)
        return {'message': 'Film created successfully'}, 201

    @classmethod
    def update(cls, film_id):
        """Update a film"""
        
        data = request.json
        # TODO: Validate data
        if data.get('title'):
            if len(data.get('title')) < 3:
                raise InvalidDataError("title must have 3 or more characters")
        if data.get('language_id'):
            if not isinstance(data.get('language_id'), int):
                raise InvalidDataError("language_id must be an integer")
        if data.get('rental_duration'):
            if not isinstance(data.get('rental_duration'), int):
                raise InvalidDataError("rental_duration must be an integer")
        if data.get('rental_rate'):
            if not isinstance(data.get('rental_rate'), int):
                raise InvalidDataError("rental_rate must be an integer")
        if data.get('replacement_cost'):
            if not isinstance(data.get('replacement_cost'), int):
                raise InvalidDataError("replacement_cost must be an integer")
        if data.get('special_features'):
            if isinstance(data.get('special_features'), list):
                for i in data.get('special_features'):
                    if i not in ["Trailers", "Commentaries", "Deleted Scenes", "Behind the Scenes"]:
                        raise InvalidDataError("Invalid spacial_features")
            else:
                raise InvalidDataError("spacial_features must be a list")


        if data.get('rental_rate') is not None:
            if isinstance(data.get('rental_rate'), int):
                data['rental_rate'] = Decimal(data.get('rental_rate'))/100
        
        if data.get('replacement_cost') is not None:
            if isinstance(data.get('replacement_cost'), int):
                data['replacement_cost'] = Decimal(data.get('replacement_cost'))/100
        
        data['film_id'] = film_id

        film = Film(**data)

        # TODO: Validate film exists
        if not Film.exists(film_id):
            raise FilmNotFound(f"Film with id {film_id} not found")
        
        Film.update(film)
        return {'message': 'Film updated successfully'}, 200
    
    @classmethod
    def delete(cls, film_id):
        """Delete a film"""
        film = Film(film_id=film_id)

        # TODO: Validate film exists
        if not Film.exists(film_id):
            raise FilmNotFound(f"Film with id {film_id} not found")
        
        Film.delete(film)
        return {'message': 'Film deleted successfully'}, 204