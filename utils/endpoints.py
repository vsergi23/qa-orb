from dataclasses import dataclass


@dataclass
class _Casting:
    actors = "casting/vendorActor"
    casting_orders = "casting/order"
    classifications = "casting/classification"
    order_processing_tasks = "casting/processingTask"


@dataclass
class _ProjectAPI:
    cancel_project = "remove/webservice/jobs/cancelJob"
    action = "overview/webservice/localizationDashboard/projectActions/"
    breakdown_reports = "projectReport/webservice/v1/index/getProjectBreakdownReports"


@dataclass
class _API:
    project = _ProjectAPI


@dataclass
class Endpoints:
    vendor_po = "fabrik/vendorPO/worksheet"
    work_orders = "app/workOrder/orders"
    casting = _Casting
    release_notes = "app/releaseNotes/dashboard/viewNotes"
    logout = "site/logout"
    api = _API
