@dev1 @project @smoke
Feature: Verifies that general project workflows still work

  Scenario: verifies project workflow without language tasks
    Given signed-in user as "SupperAdmin"
    When I create a project without tasks
    Then I verify that project was successfully created
