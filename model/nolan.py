from sqlite3 import IntegrityError
from __init__ import app, db

class Nolans(db.Model):
    __tablename__ = 'flashcards'

    id = db.Column(db.Integer, primary_key=True)
    _front= db.Column(db.String(255), nullable=False)
    _back = db.Column(db.String(255), nullable=False)

    def __init__(self, front, back):
        self._front = front
        self._back = back
    
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
            'front': self._front,
            'back': self._back
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

        front = inputs.get("front", "")
        back = inputs.get("back", "")

        # Update table with new data
        if front:
            self._front = front
        if back:
            self._back = back

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
            front = class_data.get("front", None)
            message = Nolans.query.filter_by(_front=front).first()
            if message:
                message.update(class_data)
            else:
                message = Nolans(**class_data)
                message.create()
        return classes
    
def initNolans():  
        with app.app_context():
                """Create database and tables"""
                db.create_all()
                """Tester data for table"""
                
                classes = [
                    Nolans("What is the capital of California?", "Sacramento"),
                    Nolans("What is the capital of Texas?", "Austin"),
                    Nolans("What is the capital of New York?", "Albany"),
                    Nolans("What is the capital of Florida?", "Tallahassee"),
                    Nolans("What is the capital of Georgia?", "Atlanta"),
                ]
                
                for message in classes:
                    try:
                        message.create()
                    except IntegrityError:
                        '''fails with bad or duplicate data'''
                        db.session.remove()