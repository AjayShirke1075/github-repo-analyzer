from openai import OpenAI, OpenAIError
import os

# Create OpenAI client using environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_suggestions(repo_info, tech_stack):
    """
    Generates AI-based improvement suggestions for a GitHub repository.
    If OpenAI quota/billing is unavailable, returns a safe fallback message.
    """

    prompt = f"""
Analyze the following GitHub repository and suggest improvements.

Repository Name: {repo_info.get('name')}
Description: {repo_info.get('description')}
Tech Stack: {', '.join(tech_stack)}

Provide suggestions for:
- Code quality
- Project structure
- Testing
- Security
- Documentation
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior software engineer reviewing a GitHub project."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content

    except OpenAIError:
        return (
            "⚠️ AI suggestions are currently unavailable.\n\n"
            "Reason: OpenAI API quota exceeded or billing not enabled.\n\n"
            "This feature automatically works when a valid API plan is active."
        )

    except Exception as e:
        return (
            "⚠️ An unexpected error occurred while generating AI suggestions.\n\n"
            f"Details: {str(e)}"
        )
