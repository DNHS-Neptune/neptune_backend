from sqlite3 import IntegrityError
from __init__ import app, db

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    _period= db.Column(db.String(255), nullable=False)
    _pick= db.Column(db.String(255), nullable=False)
    _user= db.Column(db.String(255), nullable=False)
    
    def __init__(self, period, pick, user):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of classes who are the moderators of the group. Defaults to None.
        """
        self._period = period
        self._pick = pick
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

    
    def read(self):
        """
        The read method retrieves the object data from the object's attributes and returns it as a dictionary.
        
        Returns:
            dict: A dictionary containing the group data.
        """
        return {
            'id': self.id,
            'pick': self._pick,
            'period': self._period,
            'user': self._user,
        }
    
    @staticmethod
    def restore(data):
        classes = {}
        for class_data in data:
            _ = class_data.pop('id', None)
            pick = class_data.get("pick", None)
            message = Class.query.filter_by(_pick=pick).first()
            if message:
                message.update(class_data)
            else:
                message = Class(**class_data)
                message.create()
        return classes
    
def initClasses():  
        with app.app_context():
                """Create database and tables"""
                db.create_all()
                """Tester data for table"""
                
        m1 = Class(user="1", pick="AP World", period="5")
        m2 = Class(user="2", pick="AP Calculus", period="1")
        m3 = Class(user="3", pick="Biology", period="3")
        m4 = Class(user="4", pick="Physics", period="4")

        classes = [m1, m2, m3, m4]
                
        for message in classes:
                    try:
                        message.create()
                    except IntegrityError:
                        '''fails with bad or duplicate data'''
                        db.session.remove()