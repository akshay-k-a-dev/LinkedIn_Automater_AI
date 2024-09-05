import json
import os
import re
import textwrap
import requests  # Added for making HTTP requests
from datetime import datetime
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages.ai import AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompt_values import StringPromptValue
from langchain_core.prompts import ChatPromptTemplate
# from langchain_gemini import GeminiAPIClient  # Removed as we're not using it anymore
from Levenshtein import distance

import src.strings as strings

load_dotenv()


class LLMLogger:
    
    def __init__(self, llm):
        self.llm = llm

    @staticmethod
    def log_request(prompts, parsed_reply: Dict[str, Dict]):
        calls_log = os.path.join(Path("data_folder/output"), "gemini_calls.json")
        if isinstance(prompts, StringPromptValue):
            prompts = prompts.text
        elif isinstance(prompts, Dict):
            # Convert prompts to a dictionary if they are not in the expected format
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }
        else:
            prompts = {
                f"prompt_{i+1}": prompt.content
                for i, prompt in enumerate(prompts.messages)
            }

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract token usage details from the response
        token_usage = parsed_reply["usage_metadata"]
        output_tokens = token_usage["output_tokens"]
        input_tokens = token_usage["input_tokens"]
        total_tokens = token_usage["total_tokens"]

        # Extract model details from the response
        model_name = parsed_reply["response_metadata"]["model_name"]
        prompt_price_per_token = 0.00000015
        completion_price_per_token = 0.0000006

        # Calculate the total cost of the API call
        total_cost = (input_tokens * prompt_price_per_token) + (
            output_tokens * completion_price_per_token
        )

        # Create a log entry with all relevant information
        log_entry = {
            "model": model_name,
            "time": current_time,
            "prompts": prompts,
            "replies": parsed_reply["content"],  # Response content
            "total_tokens": total_tokens,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_cost": total_cost,
        }

        # Write the log entry to the log file in JSON format
        with open(calls_log, "a", encoding="utf-8") as f:
            json_string = json.dumps(log_entry, ensure_ascii=False, indent=4)
            f.write(json_string + "\n")


class LoggerChatModel:
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key
        self.model_name = model_name
        self.endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent"

    def __call__(self, messages: List[Dict[str, str]]) -> str:
        # Prepare the payload for the API request
        payload = {
            "prompt": {
                "text": "\n".join([msg["content"] for msg in messages])
            },
            "temperature": 0.4,
            # Add other parameters as needed
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Make the API request
        response = requests.post(self.endpoint, headers=headers, json=payload)

        if response.status_code != 200:
            raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

        response_json = response.json()

        # Parse the response to match the expected format
        reply_content = response_json.get("candidates", [{}])[0].get("output", "")
        usage = response_json.get("usage", {})
        response_metadata = {
            "model_name": self.model_name,
            "system_fingerprint": "",  # Update if available
            "finish_reason": "",       # Update if available
            "logprobs": None           # Update if available
        }

        parsed_reply = {
            "content": reply_content,
            "response_metadata": response_metadata,
            "id": response_json.get("id", ""),
            "usage_metadata": {
                "input_tokens": usage.get("promptTokens", 0),
                "output_tokens": usage.get("completionTokens", 0),
                "total_tokens": usage.get("totalTokens", 0),
            },
        }

        # Log the request and response
        LLMLogger.log_request(prompts=messages, parsed_reply=parsed_reply)

        return reply_content


class GPTAnswerer:
    def __init__(self, gemini_api_key):
        self.llm_cheap = LoggerChatModel(
            api_key=gemini_api_key,
            model_name="gemini-1.5-flash"  # Updated model name if necessary
        )

    @property
    def job_description(self):
        return self.job.description

    @staticmethod
    def find_best_match(text: str, options: list[str]) -> str:
        distances = [
            (option, distance(text.lower(), option.lower())) for option in options
        ]
        best_option = min(distances, key=lambda x: x[1])[0]
        return best_option

    @staticmethod
    def _remove_placeholders(text: str) -> str:
        text = text.replace("PLACEHOLDER", "")
        return text.strip()

    @staticmethod
    def _preprocess_template_string(template: str) -> str:
        # Preprocess a template string to remove unnecessary indentation.
        return textwrap.dedent(template)

    def set_resume(self, resume):
        self.resume = resume

    def set_job(self, job):
        self.job = job
        self.job.set_summarize_job_description(self.summarize_job_description(self.job.description))

    def set_job_application_profile(self, job_application_profile):
        self.job_application_profile = job_application_profile
        
    def summarize_job_description(self, text: str) -> str:
        strings.summarize_prompt_template = self._preprocess_template_string(
            strings.summarize_prompt_template
        )
        prompt = ChatPromptTemplate.from_template(strings.summarize_prompt_template)
        chain = prompt | self.llm_cheap | StrOutputParser()
        output = chain.invoke({"text": text})
        return output
            
    def _create_chain(self, template: str):
        prompt = ChatPromptTemplate.from_template(template)
        return prompt | self.llm_cheap | StrOutputParser()
    
    def answer_question_textual_wide_range(self, question: str) -> str:
        # Define chains for each section of the resume
        chains = {
            "personal_information": self._create_chain(strings.personal_information_template),
            "self_identification": self._create_chain(strings.self_identification_template),
            "legal_authorization": self._create_chain(strings.legal_authorization_template),
            "work_preferences": self._create_chain(strings.work_preferences_template),
            "education_details": self._create_chain(strings.education_details_template),
            "experience_details": self._create_chain(strings.experience_details_template),
            "projects": self._create_chain(strings.projects_template),
            "availability": self._create_chain(strings.availability_template),
            "salary_expectations": self._create_chain(strings.salary_expectations_template),
            "certifications": self._create_chain(strings.certifications_template),
            "languages": self._create_chain(strings.languages_template),
            "interests": self._create_chain(strings.interests_template),
            "cover_letter": self._create_chain(strings.coverletter_template),
        }
        section_prompt = """
        You are assisting a bot designed to automatically apply for jobs on LinkedIn. The bot receives various questions about job applications and needs to determine the most relevant section of the resume to provide an accurate response.

        For the following question: '{question}', determine which section of the resume is most relevant. 
        Respond with exactly one of the following options:
        - Personal information
        - Self Identification
        - Legal Authorization
        - Work Preferences
        - Education Details
        - Experience Details
        - Projects
        - Availability
        - Salary Expectations
        - Certifications
        - Languages
        - Interests
        - Cover letter

        Here are detailed guidelines to help you choose the correct section:

        1. **Personal Information**:
        - **Purpose**: Contains your basic contact details and online profiles.
        - **Use When**: The question is about how to contact you or requests links to your professional online presence.
        - **Examples**: Email address, phone number, LinkedIn profile, GitHub repository, personal website.

        2. **Self Identification**:
        - **Purpose**: Covers personal identifiers and demographic information.
        - **Use When**: The question pertains to your gender, pronouns, veteran status, disability status, or ethnicity.
        - **Examples**: Gender, pronouns, veteran status, disability status, ethnicity.

        3. **Legal Authorization**:
        - **Purpose**: Details your work authorization status and visa requirements.
        - **Use When**: The question asks about your ability to work in specific countries or if you need sponsorship or visas.
        - **Examples**: Work authorization in EU and US, visa requirements, legally allowed to work.

        4. **Work Preferences**:
        - **Purpose**: Specifies your preferences regarding work conditions and job roles.
        - **Use When**: The question is about your preferences for remote work, in-person work, relocation, and willingness to undergo assessments or background checks.
        - **Examples**: Remote work, in-person work, open to relocation, willingness to complete assessments.

        5. **Education Details**:
        - **Purpose**: Contains information about your academic qualifications.
        - **Use When**: The question concerns your degrees, universities attended, GPA, and relevant coursework.
        - **Examples**: Degree, university, GPA, field of study, exams.

        6. **Experience Details**:
        - **Purpose**: Lists your professional work experience and roles.
        - **Use When**: The question inquires about your previous job roles, responsibilities, and accomplishments.
        - **Examples**: Previous job titles, key responsibilities, achievements.

        7. **Projects**:
        - **Purpose**: Details any relevant personal or professional projects you’ve completed.
        - **Use When**: The question asks about projects you've worked on, including their scope, technologies used, and your role.
        - **Examples**: Project descriptions, technologies used, your role in the project.

        8. **Availability**:
        - **Purpose**: Specifies your availability for work and any notice period.
        - **Use When**: The question is about when you can start a new job or your current employment status.
        - **Examples**: Notice period, availability to start work.

        9. **Salary Expectations**:
        - **Purpose**: Provides your expected salary range or compensation details.
        - **Use When**: The question concerns your salary expectations, including expected salary range.
        - **Examples**: Expected salary range, compensation expectations.

        10. **Certifications**:
        - **Purpose**: Lists any professional certifications you have obtained.
        - **Use When**: The question inquires about your professional certifications and their relevance to the job.
        - **Examples**: Certifications, issuing organizations, validity period.

        11. **Languages**:
        - **Purpose**: Indicates the languages you speak and your proficiency level.
        - **Use When**: The question is about the languages you speak or your language skills.
        - **Examples**: Languages spoken, proficiency level.

        12. **Interests**:
        - **Purpose**: Describes your hobbies, interests, and personal passions.
        - **Use When**: The question relates to your personal interests and extracurricular activities.
        - **Examples**: Hobbies, personal interests, volunteer activities.

        13. **Cover Letter**:
        - **Purpose**: Contains a personalized cover letter for the job application.
        - **Use When**: The question is about your cover letter or how to address the hiring manager.
        - **Examples**: Cover letter text, personalized introduction.

        Respond with the section that best matches the question.
        """

        # Determine the most relevant section for the question
        chain = self._create_chain(section_prompt)
        section = chain.invoke({"question": question})

        # Get the response from the appropriate section
        if section.strip() not in chains:
            return "Section not found."

        chain = chains[section.strip()]
        output = chain.invoke({"text": self.resume})

        return self._remove_placeholders(output)
