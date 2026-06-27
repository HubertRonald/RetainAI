Feature: RetainAI analytical foundation

  Scenario: Validate a minimal HR dataset contract
    Given a synthetic HR dataset
    When the dataset schema is validated
    Then the validation report should be valid

  Scenario: Detect attrition distribution
    Given a synthetic HR dataset
    When the attrition distribution is computed
    Then both attrition classes should be present

  Scenario: Build classification features
    Given a synthetic HR dataset
    When classification features are built
    Then the target should be binary encoded
