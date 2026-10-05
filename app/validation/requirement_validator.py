from app.models.requirement_analysis import RequirementAnalysis


class RequirementAnalysisValidator:

    def validate(
        self,
        analysis: RequirementAnalysis,
    ) -> list[str]:

        errors: list[str] = []

        if not analysis.requirement_summary.strip():
            errors.append(
                "Requirement summary must not be empty."
            )

        if not analysis.test_scenarios:
            errors.append(
                "At least one test scenario is required."
            )

        for scenario in analysis.test_scenarios:

            if not scenario.title.strip():
                errors.append(
                    "Test scenario title must not be empty."
                )

            if not scenario.description.strip():
                errors.append(
                    f"Test scenario '{scenario.title}' "
                    "must have a description."
                )

        return errors