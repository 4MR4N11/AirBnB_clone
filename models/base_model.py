#!/usr/bin/python3
"""class BaseModel that defines all common
attributes/methods for other classes"""
import uuid
import datetime
import os


class BaseModel():

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                if key == 'id':
                    setattr(self, key, str(value))
                elif key == 'created_at' or key == 'updated_at':
                    setattr(self, key, datetime.datetime.fromisoformat(value))
                elif key == '__class__':
                    pass
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self._created_at()
            self.updated_at = datetime.datetime.now()
            models.storage.new(self)

    def _created_at(self):
        """
        Helper method to retrieve or create the timestamp for object creation.
        """
        created_file = "created_at.txt"

        if os.path.exists(created_file):
            with open(created_file, 'r') as file:
                created_at = file.read()
            if created_at:
                return datetime.datetime.fromisoformat(created_at)
        else:
            created_at = datetime.datetime.now()
            with open(created_file, 'w') as file:
                file.write(created_at.isoformat())
            return created_at

    def __str__(self):
        """
        String representation of the object.
        """
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """
        Updates the `updated_at` timestamp to the current time.
        """
        self.updated_at = datetime.datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Converts the object into a dictionary representation.

        Returns:
            dict: Dictionary containing the object's attributes and values.
        """
        self.__dict__['__class__'] = self.__class__.__name__
        self.__dict__['created_at'] = self.created_at.isoformat()
        self.__dict__['updated_at'] = self.updated_at.isoformat()
        return self.__dict__
