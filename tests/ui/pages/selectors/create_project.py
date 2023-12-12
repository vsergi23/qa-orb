class CreateProject:
    # General Project Information
    page_title = "css=h1 >> text='General Project Information'"
    client_input = "#Project_client_id"
    owner_input = "#Project_owner_id"
    distributor_input = "#Project_distributor_id"
    product_input = "#Project_product_id"
    project_delivery_facilities_multichoice = "#Project_delivery_facilities"
    test_practice_checkbox = "input#Project_is_test_practice"
    management_team_multichoice = "#TeamProject_team_id"
    project_manager_multichoice = "#ProjectManager_manager_id"
    project_client_coordinator_select = "#Project_client_coordinator_id"
    project_projectTiers_multichoice = "#Project_projectTiers"
    # Title and Version Info
    project_atlas_content_owner_input = "#Project_atlas_content_owner_id"
    title_name_input_area = "#s2id_Project_title_name"
    title_name_search_field = "#s2id_autogen2_search"
    version_name_input_area = "#s2id_Project_version_name"
    version_name_search_field = "#s2id_autogen5_search"
    # Video Asset Information
    view_assets_btn = "a >> text='View assets'"
    root_folder = "a >> text='1._SFERA_QA_FTP'"
    dev1_date_folder = "xpath=//a[@rel='1._SFERA_QA_FTP/Sep_2022/'] >> text='Sep_2022'"
    dev1_asset_folder = "a >> text='World_of_Warcraft_Shadowlands_Cinematic_Trailer_25'"
    dev1_asset_file = "a >> text='World_of_Warcraft_Shadowlands_Cinematic_Trailer.json [3.99 KB]'"
    stgqa_date_folder = "xpath=//a[@rel='1._SFERA_QA_FTP/Jun_2022/'] >> text='Jun_2022'"
    stgqa_asset_folder = "a >> text='MG_Test_Guzun_Recording_1512.mp4_45'"
    stgqa_asset_file = "a >> text='MG_Test_Guzun_Recording_1512.json [2.34 KB]'"
    close_dialog_window_btn = "button.ui-dialog-titlebar-close"
    delivery_format_input = "#ProjectVideo_delivery_format_id"

    next_btn = "label >> text='Next'"
    similar_project_warning_accept_btn = "div.ui-dialog > div > div > button >> text='YES'"
    similar_project_warning_decline_btn = "div.ui-dialog > div > div > button >> text='NO'"

    manage_billing_data_window_title = "div.ui-dialog > div > span >> text='Manage Billing Data'"


class TasksCreation:
    page_title = "h1 >> text='Tasks'"
    save_jobs_btn = "div.form-actions > button#saveJobs >> text='Save'"

