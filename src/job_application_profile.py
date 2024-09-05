from dataclasses import dataclass
from typing import Dict
import yaml

@dataclass
class SelfIdentification:
    gender: str
    pronouns: str
    veteran: str
    disability: str
    ethnicity: str

@dataclass
class LegalAuthorization:
    eu_work_authorization: str
    us_work_authorization: str
    requires_us_visa: str
    legally_allowed_to_work_in_us: str
    requires_us_sponsorship: str
    requires_eu_visa: str
    legally_allowed_to_work_in_eu: str
    requires_eu_sponsorship: str

@dataclass
class WorkPreferences:
    remote_work: str
    in_person_work: str
    open_to_relocation: str
    willing_to_complete_assessments: str
    willing_to_undergo_drug_tests: str
    willing_to_undergo_background_checks: str

@dataclass
class Availability:
    notice_period: str

@dataclass
class SalaryExpectations:
    salary_range_usd: str

@dataclass
class JobApplicationProfile:
    self_identification: SelfIdentification
    legal_authorization: LegalAuthorization
    work_preferences: WorkPreferences
    availability: Availability
    salary_expectations: SalaryExpectations

    def __init__(self, yaml_str: str):
        try:
            data = yaml.safe_load(yaml_str)
        except yaml.YAMLError as e:
            raise ValueError("Error parsing YAML file.") from e
        except Exception as e:
            raise RuntimeError("An unexpected error occurred while parsing the YAML file.") from e

        if not isinstance(data, dict):
            raise TypeError("YAML data must be a dictionary.")

        # Helper function to create dataclass instances from dict
        def create_dataclass_instance(cls, data_key):
            try:
                return cls(**data[data_key])
            except KeyError as e:
                raise KeyError(f"Required field {e} is missing in {data_key} data.") from e
            except TypeError as e:
                raise TypeError(f"Error in {data_key} data: {e}") from e
            except Exception as e:
                raise RuntimeError(f"An unexpected error occurred while processing {data_key}.") from e

        # Process data and initialize dataclass fields
        self.self_identification = create_dataclass_instance(SelfIdentification, 'self_identification')
        self.legal_authorization = create_dataclass_instance(LegalAuthorization, 'legal_authorization')
        self.work_preferences = create_dataclass_instance(WorkPreferences, 'work_preferences')
        self.availability = create_dataclass_instance(Availability, 'availability')
        self.salary_expectations = create_dataclass_instance(SalaryExpectations, 'salary_expectations')

    def __str__(self):
        def format_dataclass(obj):
            return "\n".join(f"{field.name}: {getattr(obj, field.name)}" for field in obj.__dataclass_fields__.values())

        return (f"Self Identification:\n{format_dataclass(self.self_identification)}\n\n"
                f"Legal Authorization:\n{format_dataclass(self.legal_authorization)}\n\n"
                f"Work Preferences:\n{format_dataclass(self.work_preferences)}\n\n"
                f"Availability: {self.availability.notice_period}\n\n"
                f"Salary Expectations: {self.salary_expectations.salary_range_usd}\n\n")
