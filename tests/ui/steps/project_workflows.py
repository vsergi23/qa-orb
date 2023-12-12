import json
import logging
import re

from pytest_bdd import parsers, when, then

from utils.helper import Application

LOGGER = logging.getLogger(__name__)


@when(parsers.parse("I create a project without tasks"))
def create_one_project(app: Application):
    input_data = {
        "client": "Automation company / Automation person",
        "owner": "Automation person / Automation company",
        "distributor": "Automation person / Automation company",
        "product": "Automation Products",
        "delivery_facilities": ["Automation company / Automation person"],
        "management_team": ["Automation Team"],
        "project_manager": ["Automation Tests"],
        "client_coordinator": "Automation Tests",
        "tiers": ["Standard"],
        "atlas_content_owner": "Amazon",
        "title_name": "100 WOMEN",
        "version_name": "Theatrical",
        "delivery_format": "Texted"
    }
    app.project_input_data = input_data
    app.create_project.direct_open_create_project_page()
    app.create_project.set_client(input_data["client"])
    app.create_project.set_owner(input_data["owner"])
    app.create_project.set_distributor(input_data["distributor"])
    app.create_project.set_product(input_data["product"])
    app.create_project.set_project_delivery_facilities(input_data["delivery_facilities"])
    app.create_project.set_test_practice(checkbox=True)
    app.create_project.set_management_team(input_data["management_team"])
    app.create_project.set_project_manager(input_data["project_manager"])
    app.create_project.set_project_client_coordinator(input_data["client_coordinator"])
    app.create_project.set_tiers(input_data["tiers"])
    app.create_project.set_project_atlas_content_owner(input_data["atlas_content_owner"])
    app.create_project.set_title_name(input_data["title_name"])
    app.create_project.set_version_name(input_data["version_name"])
    app.create_project.set_video_location(app.env)
    app.create_project.set_delivery_format(input_data["delivery_format"])
    app.create_project.create_project()
    app.create_project.decline_similar_project_creation()
    app.tasks_creation.wait_page()
    project_id = app.tasks_creation.read_project_number()

    assert project_id, "Project was not created successfully"
    app.session.last_request = {"project_id": project_id}
    LOGGER.info(f"Project created with id {project_id}")
    app.session.clean_up.append({"type": "project", "id": project_id, "tasks": None})
    app.update_csrf()  # just to refresh csrf for future api requests


@then(parsers.parse("I verify that project was successfully created"))
def create_one_language_project_from_template(app: Application):
    project_id = app.session.last_request["project_id"]
    check_data = app.project_input_data
    client_pattern = re.compile(r"Client: (.*)[/\n]")
    product_pattern = re.compile(r"Product: (.*)[/\n]")
    response = app.requester.get_project_breakdown_reports(app, project_id)
    creation_info = [obj for obj in response if obj.get("action") == "Project created"]
    assert creation_info, "Information about project was not found in Project Breakdown Report"

    client = re.search(client_pattern, creation_info[0].get("description")).group(1)
    product = re.search(product_pattern, creation_info[0].get("description")).group(1)
    assert client == check_data["client"], \
        f"Error: Expected client ({check_data['client']}) doesn't match actual {client}"
    assert product == check_data["product"], \
        f"Error: Expected client ({check_data['product']}) doesn't match actual {product}"

