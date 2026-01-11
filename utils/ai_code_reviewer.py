import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def review_code_file(filename, code, tech_stack):
    prompt = f"""
You are a senior software engineer.

Review the following source code file and provide:
1. Code quality feedback
2. Bugs or logical issues
3. Performance improvements
4. Security concerns
5. Best practice suggestions

Technology Stack: {", ".join(tech_stack)}

File Name: {filename}

Code:

Respond in a clear bullet-point format.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()
