from sqlite3 import IntegrityError
from __init__ import app, db

class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column(db.Integer, primary_key=True)
    _pick= db.Column(db.String(255), nullable=False)
    _user= db.Column(db.String(255), nullable=False)
    
    def __init__(self, pick, user):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of classes who are the moderators of the group. Defaults to None.
        """
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
            'user': self._user,
        }
    
    def update(self, inputs):
        if not isinstance(inputs, dict):
            return self

        pick = inputs.get("pick", "")
        user = inputs.get("user", "")

        # Update table with new data
        if pick:
            self._pick = pick
        if user:
            self._user = user

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self
    
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
        
            classes = [
                Class(pick="AP CSP", user="Admin"),
                Class(pick="AP Chemistry", user="Admin"),
                Class(pick="AP Biology", user="Admin"),
                Class(pick="AP Seminar", user="Admin"),
                Class(pick="AP Environmental Science", user="Admin"),
                Class(pick="AP World History", user="Admin"),
                Class(pick="AP Calculus AB", user="Admin"),
                Class(pick="AP Calculus BC", user="Admin"),
                Class(pick="Photography", user="Admin"),
                Class(pick="AP CSA", user="Admin"),
                Class(pick="CSSE", user="Admin"),
                Class(pick="AP Lunch Theory", user="Admin"),
                Class(pick="World History ", user="Admin"),
                Class(pick="Chemistry", user="Admin"),
                Class(pick="Offrole", user="Admin"),
                Class(pick="English", user="Admin"),
                Class(pick="AP Language", user="Admin"),
                Class(pick="AP Literature", user="Admin"),
                Class(pick="Math", user="Admin"),
                Class(pick="P.E.", user="Admin"),
                Class(pick="Spanish", user="Admin"),
                Class(pick="Chinese", user="Admin"),
                Class(pick="AP Spanish", user="Admin"),
                Class(pick="AP Chinese", user="Admin"),
                Class(pick="AP Photography", user="Admin"),
                Class(pick="ASB", user="Admin"),
                Class(pick="Human Body Systems", user="Admin"),
                Class(pick="Principles of Biomedical Science", user="Admin"),
                Class(pick="Business and Law", user="Admin")
            ]

            for message in classes:
                    try:
                        message.create()
                    except IntegrityError:
                        db.session.remove()

def update(self, inputs):
    """
    Updates the Class object with new data.
    
    Args:
        inputs (dict): A dictionary containing the new data for the Class object.
    
    Returns:
        Class: The updated Class object, or None if an error occurs.
    """
    if not isinstance(inputs, dict):
        raise ValueError("Inputs must be a dictionary.")

    # Extract fields from inputs
    pick = inputs.get("_pick")      # Match column name
    user = inputs.get("_user")      # Match column name

    # Update fields only if provided
    if pick:
        self._pick = pick
    if user:
        self._user = user

    try:
        db.session.commit()
        return self
    except IntegrityError as e:
        db.session.rollback()
        print(f"IntegrityError: {e}")
        return None
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")
        return None

