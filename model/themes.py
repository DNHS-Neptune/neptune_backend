from sqlite3 import IntegrityError
from __init__ import app, db

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    _theme= db.Column(db.String(255), unique=True, nullable=False)
    _css= db.Column(db.String(255), unique=True, nullable=False)
    
    def __init__(self, theme, css):
        """
        Constructor, 1st step in object creation.
        
        Args:
            name (str): The name of the group.
            section_id (int): The section to which the group belongs.
            moderators (list, optional): A list of themes who are the moderators of the group. Defaults to None.
        """
        self._theme=theme
        self._css = css
        
    @property
    def theme(self):
        return self._theme
    
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
            'theme': self._theme,
            'css': self._css,
        }
    
    @staticmethod
    def restore(data):
        themes = {}
        for theme_data in data:
            _ = theme_data.pop('id', None)  # Remove 'id' from theme_data and store it in theme_id
            css = theme_data.get("css", None)
            theme = Theme.query.filter_by(_css=css).first()
            if theme:
                theme.update(theme_data)
            else:
                theme = Theme(**theme_data)
                theme.create()
        return themes
    
def initThemes():  
        with app.app_context():
                """Create database and tables"""
                db.create_all()
                """Tester data for table"""
                
                t1 = Theme(theme='Red', css="testpath1")
                t2 = Theme(theme='Green', css="testpath2")
                themes = [t1, t2]
                
                for theme in themes:
                    try:
                        theme.create()
                    except IntegrityError:
                        '''fails with bad or duplicate data'''
                        db.session.remove()