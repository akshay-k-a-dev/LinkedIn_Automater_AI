from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    title: str
    company: str
    location: str
    link: str
    apply_method: str
    description: str = ""
    summarize_job_description: str = ""
    pdf_path: str = ""
    recruiter_link: str = ""

    def set_summarize_job_description(self, summarize_job_description: str):
        self.summarize_job_description = summarize_job_description

    def set_job_description(self, description: str):
        self.description = description

    def set_recruiter_link(self, recruiter_link: str):
        self.recruiter_link = recruiter_link

    def formatted_job_information(self) -> str:
        """
        Formats the job information as a markdown string.
        """
        job_information = f"""
        # Job Description
        ## Job Information 
        - Position: {self.title}
        - At: {self.company}
        - Location: {self.location}
        - Apply Link: {self.link}
        - Application Method: {self.apply_method}
        - Recruiter Profile: {self.recruiter_link or 'Not available'}
        
        ## Description
        {self.description or 'No description provided.'}
        """
        return job_information.strip()

    def to_dict(self) -> dict:
        """
        Converts the Job object to a dictionary.
        """
        return {
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "link": self.link,
            "apply_method": self.apply_method,
            "description": self.description,
            "summarize_job_description": self.summarize_job_description,
            "pdf_path": self.pdf_path,
            "recruiter_link": self.recruiter_link,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Job':
        """
        Creates a Job object from a dictionary.
        """
        return cls(
            title=data.get("title", ""),
            company=data.get("company", ""),
            location=data.get("location", ""),
            link=data.get("link", ""),
            apply_method=data.get("apply_method", ""),
            description=data.get("description", ""),
            summarize_job_description=data.get("summarize_job_description", ""),
            pdf_path=data.get("pdf_path", ""),
            recruiter_link=data.get("recruiter_link", "")
        )
