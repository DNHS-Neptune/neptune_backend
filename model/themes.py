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
        
        t1 = Theme(
    theme='Red',
    css="""<style>
    /* Flex container for overall layout */
    .profile-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 20px;
        max-width: 900px;
        margin: auto;
        gap: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #ffcccc; /* Light red background */
    }
  
    /* Profile Picture Section */
    .image-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 40%;
    }

    #profileImageBox {
        margin-top: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #ff0000; /* Red border */
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    #profileImageBox img {
        width: 120%;
        height: 120%;
        object-fit: cover;
        object-position: center center;
    }

    .file-icon {
        cursor: pointer;
        font-size: 0.9rem;
        margin-bottom: 10px;
        color: #ff0000; /* Red icon */
    }

    .file-icon i {
        margin-left: 5px;
    }

    /* Form Section */
    .form-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    label {
        display: block;
        font-weight: bold;
        margin-bottom: 5px;
        color: #ff0000; /* Red text for labels */
    }

    input {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ff6666; /* Light red border */
        font-size: 1rem;
        color: #ff0000; /* Red text */
        background-color: #fff; /* White background for inputs */
    }

    input::placeholder {
        opacity: 0.7;
        color: #ff6666; /* Light red placeholder text */
    }

    /* Theme Selection Section */
    .theme-switch {
        margin-top: 15px;
    }

    #theme {
        padding: 8px;
        font-size: 1rem;
        border-radius: 5px;
        border: 1px solid #ff6666; /* Light red border for dropdown */
        background-color: #fff;
        color: #ff0000; /* Red text for theme dropdown */
    }

    #applytheme {
        background-color: #ff0000; /* Bright red button */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    #applytheme:hover {
        background-color: #e60000; /* Darker red on hover */
    }

    /* Button Styling */
    .side-btn {
        background-color: #ff3333; /* Darker red button */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }

    .side-btn:hover {
        background-color: #e60000; /* Darker red on hover */
    }

    /* Optional message styling */
    #profile-message {
        margin-top: 10px;
        font-size: 0.9rem;
        color: #ff6666; /* Light red text for messages */
    }
</style>
"""
)

        t2 = Theme(theme='Green', css="""<style>
    /* Flex container for overall layout */
    .profile-container {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        padding: 20px;
        max-width: 900px;
        margin: auto;
        gap: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #c8e6c9; /* Light green background */
    }
  
    /* Profile Picture Section */
    .image-section {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 40%;
    }

    #profileImageBox {
        margin-top: 10px;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 200px;
        height: 200px;
        border-radius: 50%;
        overflow: hidden;
        border: 4px solid #388e3c; /* Dark green border */
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }

    #profileImageBox img {
        width: 120%;
        height: 120%;
        object-fit: cover;
        object-position: center center;
    }

    .file-icon {
        cursor: pointer;
        font-size: 0.9rem;
        margin-bottom: 10px;
        color: #388e3c; /* Dark green icon */
    }

    .file-icon i {
        margin-left: 5px;
    }

    /* Form Section */
    .form-section {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }

    label {
        display: block;
        font-weight: bold;
        margin-bottom: 5px;
        color: #388e3c; /* Dark green text for labels */
    }

    input {
        width: 100%;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #81c784; /* Light green border */
        font-size: 1rem;
        color: #388e3c; /* Dark green text */
        background-color: #fff; /* White background for inputs */
    }

    input::placeholder {
        opacity: 0.7;
        color: #81c784; /* Light green placeholder text */
    }

    /* Theme Selection Section */
    .theme-switch {
        margin-top: 15px;
    }

    #theme {
        padding: 8px;
        font-size: 1rem;
        border-radius: 5px;
        border: 1px solid #81c784; /* Light green border for dropdown */
        background-color: #fff;
        color: #388e3c; /* Dark green text for theme dropdown */
    }

    #applytheme {
        background-color: #388e3c; /* Dark green button */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
        transition: background-color 0.3s;
    }

    #applytheme:hover {
        background-color: #2c6b2f; /* Even darker green on hover */
    }

    /* Button Styling */
    .side-btn {
        background-color: #66bb6a; /* Medium green button */
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        font-weight: bold;
    }

    .side-btn:hover {
        background-color: #388e3c; /* Dark green on hover */
    }

    /* Optional message styling */
    #profile-message {
        margin-top: 10px;
        font-size: 0.9rem;
        color: #81c784; /* Light green text for messages */
    }
</style>
""")
        themes = [t1, t2]
        
        for theme in themes:
            try:
                theme.create()
            except IntegrityError:
                '''fails with bad or duplicate data'''
                db.session.rollback()
