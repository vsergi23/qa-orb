@smoke @dev1 @login
Feature: Verify that common functionality works

  Scenario: Trying to login to the Orb localization
    When I login with role <SupperAdmin> with UI
    Then response code is <200>
    Then I log out using UI
