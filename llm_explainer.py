# Set your OpenAI key as an environment variable
import os
import evadb
from gpt4all import GPT4All


class LLMExplainer():

    def __init__(self):
        self.model = GPT4All("orca-mini-3b.ggmlv3.q4_0.bin")
        self.open_ai_key = os.environ.get('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')
        self.cursor = evadb.connect().cursor()


    def explain_sql_chatgpt(self, query_string):
        prompt = "SELECT ChatGPT('Please explain this query', {}".format(query_string)
        response = self.cursor.query(prompt).df()
        return response

    def explain_sql_local(self, query_string: str, response_length: int) -> str:
        tokens = list(self.model.generate("Explain what the SQL query: '{}' does".format(query_string), max_tokens=response_length, streaming=True))
        text = "".join(tokens)
        return text
    

# Examples
explainer = LLMExplainer()

# ChatGPT

query = """SELECT ChatGPT('Please explain this query', "SELECT * FROM students");"""
print(explainer.explain_sql_chatgpt("SELECT * FROM students", 50))
print(explainer.explain_sql_chatgpt("INSERT INTO students (id, name) VALUES ('1', 'Krish')", 50))
print(explainer.explain_sql_chatgpt("""SELECT * FROM students WHERE id = 1, name = Krish GROUP BY class ORDER BY id""", 100))

# Local

print(explainer.explain_sql_local("SELECT * FROM students", 50))
print(explainer.explain_sql_local("INSERT INTO students (id, name) VALUES ('1', 'Krish')", 50))
print(explainer.explain_sql_local("""SELECT * FROM students WHERE id = 1, name = Krish GROUP BY class ORDER BY id""", 100))
