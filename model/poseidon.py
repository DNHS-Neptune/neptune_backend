from sqlite3 import IntegrityError
from __init__ import app, db

class PoseidonChatLog(db.Model):
    __tablename__ = 'poseidon_chat_logs'

    id = db.Column(db.Integer, primary_key=True)
    _question = db.Column(db.String(500), nullable=False)
    _response = db.Column(db.String(2000), nullable=False)

    def __init__(self, question, response):
        """
        Constructor to initialize PoseidonChatLog object.
        
        Args:
            question (str): The user's question.
            response (str): The AI's response.
        """
        self._question = question
        self._response = response

    @property
    def question(self):
        return self._question

    @property
    def response(self):
        return self._response

    def create(self):
        """
        Add the object to the database and commit the transaction.
        
        Raises:
            Exception: If an error occurs during the commit.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def read(self):
        """
        Retrieve the object's data as a dictionary.
        
        Returns:
            dict: A dictionary containing the question and response.
        """
        return {
            'id': self.id,
            'question': self._question,
            'response': self._response,
        }

    @staticmethod
    def restore(data):
        """
        Restore data from a list of dictionaries into the database.
        
        Args:
            data (list): List of dictionaries containing chat logs.
        
        Returns:
            dict: A dictionary of restored chat logs.
        """
        chat_logs = {}
        for log_data in data:
            _ = log_data.pop('id', None)
            question = log_data.get("question", None)
            log = PoseidonChatLog.query.filter_by(_question=question).first()
            if log:
                log.update(log_data)
            else:
                log = PoseidonChatLog(**log_data)
                log.create()
        return chat_logs


def initPoseidonChatLogs():
    """
    Initialize the database with example chat logs for testing.
    """
    with app.app_context():
        db.create_all()

        # Example chat logs
        log1 = PoseidonChatLog(question="What is Newton's third law?", response="Newton's third law states that for every action, there is an equal and opposite reaction.")
        log2 = PoseidonChatLog(question="What is the capital of France?", response="The capital of France is Paris.")
        
        chat_logs = [log1, log2]

        for log in chat_logs:
            try:
                log.create()
            except IntegrityError:
                db.session.rollback()

# Ensuring the table is created
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Table creation complete.")
