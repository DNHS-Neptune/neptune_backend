from sqlite3 import IntegrityError
from __init__ import app, db

class Sports(db.Model):
    __tablename__ = 'sports'

    id = db.Column(db.Integer, primary_key=True)
    _sport= db.Column(db.String(255), nullable=False)
    _emoji = db.Column(db.String(255), nullable=False)
    
    def __init__(self, sport, emoji):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of classes who are the moderators of the group. Defaults to None.
        """
        self._sport = sport
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
            'sport': self._sport,
            'emoji': self._emoji,
        }
    
    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self
        
        sport = inputs.get("sport", "")
        emoji = inputs.get("emoji", "")


        # Update table with new data
        if sport:
            self._sport = sport
        if emoji:
            self._emoji = emoji

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
    def restore(data):
        sports = {}
        for sport_data in data:
            _ = sport_data.pop('id', None)
            emoji = sport_data.get("emoji", None)
            message = Sports.query.filter_by(_emoji=emoji).first()
            if message:
                message.update(sport_data)
            else:
                message = Sports(**sport_data)
                message.create()
        return sports
    
def initSports():  
        with app.app_context():
            """Create database and tables"""
            db.create_all()
            """Tester data for table"""
                
            m1 = Sports(sport="Basketball", emoji="⚽️")   # Populates the table with data when the table is intialized
            m2 = Sports(sport="Tennis", emoji="🎾")
            m3 = Sports(sport="Soccer", emoji="⚽️")
            m4 = Sports(sport="Football", emoji="🏈")

            sports = [m1, m2, m3, m4]
                
            for message in sports:
                    try:
                        message.create()
                    except IntegrityError:
                        db.session.remove()
                        
