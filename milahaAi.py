# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
from flask import Flask, render_template, request, jsonify


wikipedia_article_on_curling = """| **Category**                 | **Violation**                                                                                                      | **Severity Rating** |
|------------------------------|--------------------------------------------------------------------------------------------------------------------|---------------------|
| **Unauthorized Absence**     | Reporting late to work without permission or justified reason.                                                     | 3                   |
|                              | Leaving work early without permission or justified reason.                                                         | 3                   |
|                              | Absence for one or up to six days without permission or a justified reason during the year.                        | 4                   |
|                              | Absent for 7 consecutive days or 15 non-consecutive days throughout the year without permission or a justified reason. | 5                   |
|                              | Violating instructions related to the attendance punching system.                                                  | 3                   |
| **Discriminatory Behavior**  | Acting or failing to act on a matter which improperly considers an individual's race, color, age, etc.             | 5                   |
|                              | Use of critical,harrasment ,demeaning, or degrading remarks based on another's race, color, age, sexual orientation, etc.     | 5                   |
| **Disruptive Behavior**      | Use of abusive, slanderous, malicious, derogatory language, gestures, or conduct to or about co-workers.           | 4                   |
|                              | Use of discourteous, unprofessional language, gestures, or conduct toward members of the public, visitors, and clients. | 4                   |
| **Neglect of Duty**          | Failure to follow proper supervisory instructions.                                                                 | 4                   |
|                              | Willful and intentional refusal to follow a proper order, regulation, policy, rule, or procedure.                   | 5                   |
|                              | Refusing to work overtime hours in an emergency without a justified reason.                                        | 4                   |
|                              | Refusing to undertake new or added tasks if they are not fundamentally different from the original job description. | 3                   |
|                              | Non-performance of required work on deadline without a justified reason.                                           | 4                   |                                        |

"""


app = Flask(__name__)

# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-4"
openai.api_key = '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'  # Make sure to keep your API key private


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def api_query():
    print("test")
    print(request.get_json())
    data = request.get_json()  # Get JSON data from the request
    user_query = data['query']
    
    query = f"""Use the below violation policy to strictly only answer the subsequent question. If the answer cannot be found, write "It is not a violation." only and nothing else.

Article:
\"\"\"
{wikipedia_article_on_curling}
\"\"\"

{user_query}"""

    response = openai.ChatCompletion.create(
        messages=[
            {'role': 'system', 'content': 'You answer questions about the violation policies. and (display as html table with purple borders for the severity of the violation and return in HTML table with purple borders for the results) secondly put below it to show course of action as a penalty: first time first written warning second time second written warning third time final written warning and fourth time termination as an html table with purple borders with margin on top and bottom if exists'},
            {'role': 'user', 'content': query},
        ],
        model=GPT_MODEL,
        temperature=0,
    )
    print("RESPONSE: ",response['choices'][0]['message']['content'])
    return jsonify(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    app.run(debug=True)