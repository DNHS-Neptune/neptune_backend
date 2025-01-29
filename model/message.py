from sqlite3 import IntegrityError
from __init__ import app, db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    _content= db.Column(db.String(255), unique=True, nullable=False)
    _user= db.Column(db.String(255), unique=True, nullable=False)
    
    def __init__(self, content, user):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of messages who are the moderators of the group. Defaults to None.
        """
        self._content = content
        self._user = user
        
    @property
    def content(self):
        return self._content
    
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
        
    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self

        content = inputs.get("content", "")
        user = inputs.get("user", "")

        # Update table with new data
        if content:
            self._content = content

        if user:
            self._user = user

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def delete(self):
        try:
            db.session.delete(self)
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
            'content': self._content,
            'user': self._user,
        }
    
    @staticmethod
    def restore(data):
        messages = {}
        for message_data in data:
            _ = message_data.pop('id', None)
            content = message_data.get("content", None)
            message = Message.query.filter_by(_content=content).first()
            if message:
                message.update(message_data)
            else:
                message = Message(**message_data)
                message.create()
        return messages
    
def initMessages():  
        with app.app_context():
                """Create database and tables"""
                db.create_all()
                """Tester data for table"""
                
                m1 = Message(user="nolan", content="yash patil is stupid")
                m2 = Message(user="arya", content="i'm a dumb potato")
                messages = [m1, m2]
                
                for message in messages:
                    try:
                        message.create()
                    except IntegrityError:
                        '''fails with bad or duplicate data'''
                        db.session.remove()