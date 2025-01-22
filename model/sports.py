from sqlite3 import IntegrityError
from __init__ import app, db

class Sports(db.Model):
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)
    _name= db.Column(db.String(255), nullable=False)
    _emoji = db.Column(db.String(255), nullable=False)
    
    def __init__(self, name, emoji):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of classes who are the moderators of the group. Defaults to None.
        """
        self._name = name
        self._emoji = emoji
    
    def create(self):
        """
        The create method adds the object to the database and commits the transaction.
        
        Uses:
            The db ORM methods to add and commit the transaction.
        
        Raises:
            Exception: An error occurred when adding the object to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the group data.
        """
        return {
            'id': self.id,
            'name': self._name,
            'emoji': self._emoji
        }
    
    def update(self, inputs):
        """
        Updates the channel object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the channel.
        
        Returns:
            Channel: The updated channel object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        name = inputs.get("name", "")
        emoji = inputs.get("emoji", "")

        # Update table with new data
        if name:
            self._name = name
        if emoji:
            self._emoji = emoji
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def delete(self):
        """
        The delete method removes the object from the database and commits the transaction.
        
        Uses:
            The db ORM methods to delete and commit the transaction.
        
        Raises:
            Exception: An error occurred when deleting the object from the database.
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
        
    @staticmethod
    def restore(data):
        classes = {}
        for class_data in data:
            _ = class_data.pop('id', None)
            name = class_data.get("name", None)
            message = Sports.query.filter_by(_name=name).first()
            if message:
                message.update(class_data)
            else:
                message = Sports(**class_data)
                message.create()
        return classes

    
def initAkshajs():  
        with app.app_context():
                """Create database and tables"""
                db.create_all()
                """Tester data for table"""
                
                m1 = Sports(name="Football", emoji="")
                m2 = Sports(name="Soccer", emoji="")
                classes = [m1, m2]
                
                for message in classes:
                    try:
                        message.create()
                    except IntegrityError:
                        '''fails with bad or duplicate data'''
                        db.session.remove()