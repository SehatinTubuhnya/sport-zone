from django.urls import path
from .views import homepage, get_accounts_api, add_account_api, delete_account_api, get_action_logs_api, accounts_page, action_logs_page, get_summary, delete_action_log_api, edit_account_api

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
    path("api/action-logs", get_action_logs_api, name="get_action_logs"),
    path("api/action-logs/delete", delete_action_log_api, name="delete_action_logs")
]
