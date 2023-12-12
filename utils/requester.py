from utils.endpoints import Endpoints
# from utils.helper import Application
# circle import, but you can uncomment it for development and use as link for app: Application


def logout(app):
    link = app.base_url + Endpoints.logout
    response = app.page.request.get(link)
    if response.status == 200:
        return response.body()
    else:
        raise Exception(f"Status code of response: {response.status}\nError message: {response.status_text}")


def get_project_option(app, project_id):
    link = app.base_url + Endpoints.api.project.action + f"?projects[0][projectId]={project_id}"
    response = app.page.request.get(link)
    app.session.last_request = response
    if response.status == 200:
        return response.json()
    else:
        raise Exception(f"Status code of response: {response.status}\nError message: {response.status_text}")


def post_remove_project(app, project_id):
    link = app.base_url + Endpoints.api.project.cancel_project
    headers = {"CSRFTOKEN": app.session.is_signed_in['csrf']}
    payload = {
        "projectIds": [project_id],
        "setDeleted": 1,
        "jobOnly": 0,
        "submitRemove": 1,
        "removeJobReviewer": 1,
        "caps_payment": None,
        "skipOptionJobs": []
    }
    response = app.page.request.post(link, headers=headers, data=payload)
    app.session.last_request = response
    if response.status == 200:
        return response.json()
    else:
        raise Exception(f"Status code of response: {response.status}\nError message: {response.status_text}")


def get_project_breakdown_reports(app, project_id):
    link = app.base_url + Endpoints.api.project.breakdown_reports
    parameters = f"?projectId={project_id}&filters[pageSizeFilter]=10&page=1&pageSize=10&sort="
    response = app.page.request.get(link + parameters)
    app.session.last_request = response
    if response.status == 200:
        return response.json()
    else:
        raise Exception(f"Status code of response: {response.status}\nError message: {response.status_text}")
