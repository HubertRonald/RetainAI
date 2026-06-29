Feature: Dashboard foundation

  Scenario: Dashboard architecture documents are available
    Given the dashboard planning documents exist
    Then the dashboard architecture should define four analytical pages

  Scenario: Dashboard service boundaries are defined
    Given the dashboard service contract exists
    Then the API domains should include overview, predict, explainability and survival

  Scenario: Dashboard mockup is validated before implementation
    Given the dashboard mockup specification exists
    Then it should include the fancy dark layout contract
