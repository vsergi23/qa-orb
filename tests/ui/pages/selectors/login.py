class LoginPage:
    log_in_btn = "#login-button > a > span"
    login_pop_up = "div#login-dialog"
    email_field = "#LoginForm_email"
    password_field = "#LoginForm_password"
    login_submit_btn = "#login-form > div input.ajax-sbm"
    agreement_pop_up = "#security-disclaimer-dialog > div"
    agreement_accept_btn = "xpath=//*[@id='security-accept' and text()='Accept']"
    session_warning_pop_up = "div#sessions-warning"
    session_warning_btn = "button#sessions-continuewith-new"