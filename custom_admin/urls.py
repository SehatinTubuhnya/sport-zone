from django.urls import path

from .views import (
    accounts_page,
    action_logs_page,
    add_account_api,
    delete_account_api,
    delete_action_log_api,
    edit_account_api,
    get_accounts_api,
    get_action_logs_api,
    get_all_accounts_api,
    get_all_action_logs_api,
    get_summary,
    homepage,
)

app_name = "custom_admin"

urlpatterns = [
    path("", homepage, name="homepage"),
    path("accounts", accounts_page, name="manage_accounts"),
    path("action-logs", action_logs_page, name="manage_action_logs"),
    path("api/summary", get_summary, name="summary"),
    path("api/accounts", get_accounts_api, name="get_accounts"),
    path("api/accounts/add", add_account_api, name="add_account"),
    path("api/accounts/edit", edit_account_api, name="edit_account"),
    path("api/accounts/delete", delete_account_api, name="delete_account"),
    path("api/accounts/all", get_all_accounts_api, name="get_all_accounts"),
    path("api/action-logs", get_action_logs_api, name="get_action_logs"),
    path("api/action-logs/all", get_all_action_logs_api, name="get_all_action_logs"),
    path("api/action-logs/delete", delete_action_log_api, name="delete_action_logs"),
]
