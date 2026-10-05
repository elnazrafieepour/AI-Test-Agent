from app.llm.client import LLMClient
from app.models.requirement_analysis import RequirementAnalysis
from app.validation.requirement_validator import (
    RequirementAnalysisValidator,
)


class TestEngineerAgent:

    def __init__(
        self,
        llm: LLMClient,
        validator: RequirementAnalysisValidator,
    ):
        self.llm = llm
        self.validator = validator

    def analyze_requirement(
        self,
        requirement: str,
    ) -> RequirementAnalysis:

        prompt = f"""
        You are a Senior Software Test Engineer.

        Your task is to analyze a software requirement from a
        testing and quality perspective.

        First, understand the requirement.

        Then identify:

        1. Functional test scenarios
        2. Negative scenarios
        3. Boundary conditions
        4. Validation rules
        5. Potential risks
        6. Missing or ambiguous requirements

        For the requirement summary:
        - Explain your understanding of the requirement.
        - Do not invent requirements that are not explicitly stated.

        For every test scenario:
        - Provide a clear title.
        - Explain what should be tested.
        - Classify the scenario.
        - Assign a priority.

        For every risk:
        - Explain the risk.
        - Assign a severity.

        For every ambiguity:
        - Explain what is unclear.
        - Provide a question that should be asked to clarify it.

        Important:
        - Do not assume unspecified business rules.
        - If information is missing, report it as an ambiguity.
        - Think like a senior QA engineer.
        - Focus on testability, correctness, boundary conditions,
          failure conditions, and business risks.

        Requirement:
        {requirement}
        """

        analysis = self.llm.ask_structured(
            prompt,
            RequirementAnalysis,
        )

        validation_errors = self.validator.validate(
            analysis
        )

        if validation_errors:
            raise ValueError(
                "Requirement analysis validation failed: "
                + "; ".join(validation_errors)
            )

        return analysis