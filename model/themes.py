from sqlite3 import IntegrityError
from __init__ import app, db

class Theme(db.Model):
    __tablename__ = 'themes'

    id = db.Column(db.Integer, primary_key=True)
    _theme = db.Column(db.String(255), unique=True, nullable=False)
    _css = db.Column(db.String(255), unique=True, nullable=False)
    
    def __init__(self, theme, css):
        """
        Constructor, 1st step in object creation.
        
        Args:
            theme (str): The name of the theme.
            css (str): The CSS associated with the theme.
        """
        self._theme = theme
        self._css = css
        
    @property
    def theme(self):
        return self._theme

    def delete(self):
        """
        Removes the theme object from the database and commits the transaction.
        
        Returns:
            None
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            raise e

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
            dict: A dictionary containing the theme data.
        """
        return {
            'id': self.id,
            'theme': self._theme,
            'css': self._css,
        }

    def update(self, inputs):
        """
        Updates the theme object with new data.
        
        Args:
            inputs (dict): A dictionary containing the new data for the theme.
        
        Returns:
            Theme: The updated theme object, or None on error.
        """
        if not isinstance(inputs, dict):
            return self

        theme = inputs.get("theme", "")
        css = inputs.get("css", "")

        # Update table with new data
        if theme:
            self._theme = theme
        if css:
            self._css = css
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return None
        return self

    @staticmethod
    def restore(data):
        themes = {}
        for theme_data in data:
            _ = theme_data.pop('id', None)  # Remove 'id' from theme_data
            css = theme_data.get("css", None)
            theme = Theme.query.filter_by(_css=css).first()
            if theme:
                theme = theme.update(theme_data)  # Call update on the instance
            else:
                theme = Theme(**theme_data)
                theme.create()
            themes[theme._theme] = theme  # Keep track of themes if needed
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
                db.session.rollback()
