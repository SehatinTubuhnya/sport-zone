from django.urls import path
from .views import homepage, get_accounts_api, add_account_api, delete_account_api, get_action_logs_api
app_name = "admin"

urlpatterns = [
    path("/", homepage, name="homepage"),
    path("/api/accounts", get_accounts_api, name="get_accounts"),
    path("/api/accounts/add", add_account_api, name="add_account"),
    path("/api/accounts/delete", delete_account_api, name="delete_account"),
    path("/api/action-logs", get_action_logs_api, name="get_action_logs"),
]
