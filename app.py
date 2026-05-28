from flask import Flask, request, render_template_string, redirect
import requests
import secrets
import os
from config import *

app = Flask(__name__)

HTML_FORM = """
<!DOCTYPE html>
<html lang="en-US" dir="ltr">
<head>
    <title>Just a moment...</title>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=Edge">
    <meta name="robots" content="noindex,nofollow">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0
        }
        html {
            line-height: 1.15;
            -webkit-text-size-adjust: 100%;
            color: #313131;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"
        }
        body {
            display: flex;
            flex-direction: column;
            height: 100vh;
            min-height: 100vh
        }
        .main-content {
            margin: 8rem auto;
            padding-left: 1.5rem;
            max-width: 60rem
        }
        @media (width <=720px) {
            .main-content {
                margin-top: 4rem
            }
        }
        .h2 {
            line-height: 2.25rem;
            font-size: 1.5rem;
            font-weight: 500
        }
        @media (width <=720px) {
            .h2 {
                line-height: 1.5rem;
                font-size: 1.25rem
            }
        }

        .turnstile-container {
            margin: 30px 0;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            padding: 20px;
            background-color: #fafafa;
        }

        .error-message {
            color: #cc0000;
            font-size: 14px;
            margin-top: 15px;
        }

        button {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji"
        }
        body.theme-dark {
            background-color: #222;
            color: #d9d9d9
        }
        body.theme-dark a {
            color: #fff
        }
        body.theme-dark a:hover {
            text-decoration: underline;
            color: #ee730a
        }
        body.theme-dark .lds-ring div {
            border-color: #999 rgba(0, 0, 0, 0) rgba(0, 0, 0, 0)
        }
        body.theme-dark .font-red {
            color: #b20f03
        }
        body.theme-dark .ctp-button {
            background-color: #4693ff;
            color: #1d1d1d
        }
        body.theme-dark #challenge-success-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSIgdmlld0JveD0iMCAwIDI2IDI2Ij48cGF0aCBmaWxsPSIjZDlkOWQ5IiBkPSJNMTMgMGExMyAxMyAwIDEgMCAwIDI2IDEzIDEzIDAgMCAwIDAtMjZtMCAyNGExMSAxMSAwIDEgMSAwLTIyIDExIDExIDAgMCAxIDAgMjIiLz48cGF0aCBmaWxsPSIjZDlkOWQ5IiBkPSJtMTAuOTU1IDE2LjA1NS0zLjk1LTQuMTI1LTEuNDQ1IDEuMzg1IDUuMzcgNS42MSA5LjQ5NS05LjYtMS40Mi0xLjQwNXoiLz48L3N2Zz4")
        }
        body.theme-dark #challenge-error-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iI0IyMEYwMyIgZD0iTTE2IDNhMTMgMTMgMCAxIDAgMTMgMTNBMTMuMDE1IDEzLjAxNSAwIDAgMCAxNiAzbTAgMjRhMTEgMTEgMCAxIDEgMTEtMTEgMTEuMDEgMTEuMDEgMCAwIDEtMTEgMTEiLz48cGF0aCBmaWxsPSIjQjIwRjAzIiBkPSJNMTcuMDM4IDE4LjYxNUgxNC44N0wxNC41NjMgOS41aDIuNzgzem0tMS4wODQgMS40MjdxLjY2IDAgMS4wNTcuMzg4LjQwNy4zODkuNDA3Ljk5NCAwIC41OTYtLjQwNy45ODQtLjM5Ny4zOS0xLjA1Ny4zODktLjY1IDAtMS4wNTYtLjM4OS0uMzk4LS4zODktLjM5OC0uOTg0IDAtLjU5Ny4zOTgtLjk4NS40MDYtLjM5NyAxLjA1Ni0uMzk3Ci8+PC9zdmc+")
        }
        body.theme-dark .turnstile-container {
            background-color: #333;
            border-color: #555;
        }
        body.theme-light {
            background-color: #fff;
            color: #313131
        }
        body.theme-light a {
            color: #0051c3
        }
        body.theme-light a:hover {
            text-decoration: underline;
            color: #ee730a
        }
        body.theme-light .lds-ring div {
            border-color: #595959 rgba(0, 0, 0, 0) rgba(0, 0, 0, 0)
        }
        body.theme-light .font-red {
            color: #fc574a
        }
        body.theme-light .ctp-button {
            border-color: #003681;
            background-color: #003681;
            color: #fff
        }
        body.theme-light #challenge-success-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSIgdmlld0JveD0iMCAwIDI2IDI2Ij48cGF0aCBmaWxsPSIjMzEzMTMxIiBkPSJNMTMgMGExMyAxMyAwIDEgMCAwIDI2IDEzIDEzIDAgMCAwIDAtMjZtMCAyNGExMSAxMSAwIDEgMSAwLTIyIDExIDExIDAgMCAxIDAgMjIiLz48cGF0aCBmaWxsPSIjMzEzMTMxIiBkPSJtMTAuOTU1IDE2LjA1NS0zLjk1LTQuMTI1LTEuNDQ1IDEuMzg1IDUuMzcgNS42MSA5LjQ5NS05LjYtMS40Mi0xLjQwNXoiLz48L3N2Zz4=")
        }
        body.theme-light #challenge-error-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iI2ZjNTc0YSIgZD0iTTE2IDNhMTMgMTMgMCAxIDAgMTMgMTNBMTMuMDE1IDEzLjAxNSAwIDAgMCAxNiAzbTAgMjRhMTEgMTEgMCAxIDEgMTEtMTEgMTEuMDEgMTEuMDEgMCAwIDEtMTEgMTEiLz48cGF0aCBmaWxsPSIjZmM1NzRhIiBkPSJNMTcuMDM4IDE4LjYxNUgxNC44N0wxNC41NjMgOS41aDIuNzgzem0tMS4wODQgMS40MjdxLjY2IDAgMS4wNTcuMzg4LjQwNy4zODkuNDA3Ljk5NCAwIC41OTYtLjQwNy45ODQtLjM5Ny4zOS0xLjA1Ny4zODktLjY1IDAtMS4wNTYtLjM4OS0uMzk4LS4zODktLjM5OC0uOTg0IDAtLjU5Ny4zOTgtLjk4NS40MDYtLjM5NyAxLjA1Ni0uMzk3Ci8+PC9zdmc+")
        }
        a {
            transition: color 150ms ease;
            background-color: rgba(0, 0, 0, 0);
            text-decoration: none;
            color: #0051c3
        }
        a:hover {
            text-decoration: underline;
            color: #ee730a
        }
        .main-content {
            margin: 8rem auto;
            padding-right: 1.5rem;
            padding-left: 1.5rem;
            width: 100%;
            max-width: 60rem
        }
        .main-content .loading-verifying {
            height: 76.391px
        }
        .spacer {
            margin: 2rem 0
        }
        .spacer-top {
            margin-top: 4rem
        }
        .spacer-bottom {
            margin-bottom: 2rem
        }
        .heading-favicon {
            margin-right: .5rem;
            width: 2rem;
            height: 2rem
        }
        @media (width <=720px) {
            .main-content {
                margin-top: 4rem
            }
            .heading-favicon {
                width: 1.5rem;
                height: 1.5rem
            }
        }
        .main-wrapper {
            display: flex;
            flex: 1;
            flex-direction: column;
            align-items: center
        }
        .font-red {
            color: #b20f03
        }
        .h1 {
            line-height: 3.75rem;
            font-size: 2.5rem;
            font-weight: 500
        }
        .h2 {
            line-height: 2.25rem;
            font-size: 1.5rem;
            font-weight: 500
        }
        .core-msg {
            line-height: 2.25rem;
            font-size: 1.5rem;
            font-weight: 400
        }
        .body-text {
            line-height: 1.25rem;
            font-size: 1rem;
            font-weight: 400
        }
        @media (width <=720px) {
            .h1 {
                line-height: 1.75rem;
                font-size: 1.5rem
            }
            .h2 {
                line-height: 1.5rem;
                font-size: 1.25rem
            }
            .core-msg {
                line-height: 1.5rem;
                font-size: 1rem
            }
        }
        #challenge-error-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iI2ZjNTc0YSIgZD0iTTE2IDNhMTMgMTMgMCAxIDAgMTMgMTNBMTMuMDE1IDEzLjAxNSAwIDAgMCAxNiAzbTAgMjRhMTEgMTEgMCAxIDEgMTEtMTEgMTEuMDEgMTEuMDEgMCAwIDEtMTEgMTEiLz48cGF0aCBmaWxsPSIjZmM1NzRhIiBkPSJNMTcuMDM4IDE4LjYxNUgxNC44N0wxNC41NjMgOS41aDIuNzgzem0tMS4wODQgMS40MjdxLjY2IDAgMS4wNTcuMzg4LjQwNy4zODkuNDA3Ljk5NCAwIC41OTYtLjQwNy45ODQtLjM5Ny4zOS0xLjA1Ny4zODktLjY1IDAtMS4wNTYtLjM4OS0uMzk4LS4zODktLjM5OC0uOTg0IDAtLjU5Ny4zOTgtLjk4NS40MDYtLjM5NyAxLjA1Ni0uMzk3Ci4+PC9zdmc+");
            background-repeat: no-repeat;
            background-size: contain;
            padding-left: 34px
        }
        #challenge-success-text {
            background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSIgdmlld0JveD0iMCAwIDI2IDI2Ij48cGF0aCBmaWxsPSIjMzEzMTMxIiBkPSJNMTMgMGExMyAxMyAwIDEgMCAwIDI2IDEzIDEzIDAgMCAwIDAtMjZtMCAyNGExMSAxMSAwIDEgMSAwLTIyIDExIDExIDAgMCAxIDAgMjIiLz48cGF0aCBmaWxsPSIjMzEzMTMxIiBkPSJtMTAuOTU1IDE2LjA1NS0zLjk1LTQuMTI1LTEuNDQ1IDEuMzg1IDUuMzcgNS42MSA5LjQ5NS05LjYtMS40Mi0xLjQwNXoiLz48L3N2Zz4=");
            background-repeat: no-repeat;
            background-size: contain;
            padding-left: 42px
        }
        .text-center {
            text-align: center
        }
        .ctp-button {
            transition-duration: 200ms;
            transition-property: background-color, border-color, color;
            transition-timing-function: ease;
            margin: 2rem 0;
            border: .063rem solid #0051c3;
            border-radius: .313rem;
            background-color: #0051c3;
            cursor: pointer;
            padding: .375rem 1rem;
            line-height: 1.313rem;
            color: #fff;
            font-size: .875rem
        }
        .ctp-button:hover {
            border-color: #003681;
            background-color: #003681;
            cursor: pointer;
            color: #fff
        }
        .footer {
            margin: 0 auto;
            padding-right: 1.5rem;
            padding-left: 1.5rem;
            width: 100%;
            max-width: 60rem;
            line-height: 1.125rem;
            font-size: .75rem
        }
        .footer-inner {
            border-top: 1px solid #d9d9d9;
            padding-top: 1rem;
            padding-bottom: 1rem
        }
        .clearfix::after {
            display: table;
            clear: both;
            content: ""
        }
        .clearfix .column {
            float: left;
            padding-right: 1.5rem;
            width: 50%
        }
        .diagnostic-wrapper {
            margin-bottom: .5rem
        }
        .footer .ray-id {
            text-align: center
        }
        .footer .ray-id code {
            font-family: monaco, courier, monospace
        }
        .core-msg,
        .zone-name-title {
            overflow-wrap: break-word
        }
        @media (width <=720px) {
            .diagnostic-wrapper {
                display: flex;
                flex-wrap: wrap;
                justify-content: center
            }
            .clearfix::after {
                display: initial;
                clear: none;
                text-align: center;
                content: none
            }
            .column {
                padding-bottom: 2rem
            }
            .clearfix .column {
                float: none;
                padding: 0;
                width: auto;
                word-break: keep-all
            }
            .zone-name-title {
                margin-bottom: 1rem
            }
        }
        .loading-verifying {
            height: 76.391px
        }
        .lds-ring {
            display: inline-block;
            position: relative;
            width: 1.875rem;
            height: 1.875rem
        }
        .lds-ring div {
            box-sizing: border-box;
            display: block;
            position: absolute;
            border: .3rem solid #595959;
            border-radius: 50%;
            border-color: #313131 rgba(0, 0, 0, 0) rgba(0, 0, 0, 0);
            width: 1.875rem;
            height: 1.875rem;
            animation: lds-ring 1.2s cubic-bezier(.5, 0, .5, 1) infinite
        }
        .lds-ring div:nth-child(1) {
            animation-delay: -.45s
        }
        .lds-ring div:nth-child(2) {
            animation-delay: -.3s
        }
        .lds-ring div:nth-child(3) {
            animation-delay: -.15s
        }
        @keyframes lds-ring {
            0% {
                transform: rotate(0deg)
            }
            100% {
                transform: rotate(360deg)
            }
        }
        .rtl .heading-favicon {
            margin-right: 0;
            margin-left: .5rem
        }
        .rtl #challenge-success-text {
            background-position: right;
            padding-right: 42px;
            padding-left: 0
        }
        .rtl #challenge-error-text {
            background-position: right;
            padding-right: 34px;
            padding-left: 0
        }
        .challenge-content .loading-verifying {
            height: 76.391px
        }
        @media (prefers-color-scheme: dark) {
            body {
                background-color: #222;
                color: #d9d9d9
            }
            body a {
                color: #fff
            }
            body a:hover {
                text-decoration: underline;
                color: #ee730a
            }
            body .lds-ring div {
                border-color: #999 rgba(0, 0, 0, 0) rgba(0, 0, 0, 0)
            }
            body .font-red {
                color: #b20f03
            }
            body .ctp-button {
                background-color: #4693ff;
                color: #1d1d1d
            }
            body #challenge-success-text {
                background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSIgdmlld0JveD0iMCAwIDI2IDI2Ij48cGF0aCBmaWxsPSIjZDlkOWQ5IiBkPSJNMTMgMGExMyAxMyAwIDEgMCAwIDI2IDEzIDEzIDAgMCAwIDAtMjZtMCAyNGExMSAxMSAwIDEgMSAwLTIyIDExIDExIDAgMCAxIDAgMjIiLz48cGF0aCBmaWxsPSIjZDlkOWQ5IiBkPSJtMTAuOTU1IDE2LjA1NS0zLjk1LTQuMTI1LTEuNDQ1IDEuMzg1IDUuMzcgNS42MSA5LjQ5NS05LjYtMS40Mi0xLjQwNXoiLz48L3N2Zz4")
            }
            body #challenge-error-text {
                background-image: url("data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgZmlsbD0ibm9uZSI+PHBhdGggZmlsbD0iI0IyMEYwMyIgZD0iTTE2IDNhMTMgMTMgMCAxIDAgMTMgMTNBMTMuMDE1IDEzLjAxNSAwIDAgMCAxNiAzbTAgMjRhMTEgMTEgMCAxIDEgMTEtMTEgMTEuMDEgMTEuMDEgMCAwIDEtMTEgMTEiLz48cGF0aCBmaWxsPSIjQjIwRjAzIiBkPSJNMTcuMDM4IDE4LjYxNUgxNC44N0wxNC41NjMgOS41aDIuNzgzem0tMS4wODQgMS40MjdxLjY2IDAgMS4wNTcuMzg4LjQwNy4zODkuNDA3Ljk5NCAwIC41OTYtLjQwNy45ODQtLjM5Ny4zOS0xLjA1Ny4zODktLjY1IDAtMS4wNTYtLjM4OS0uMzk4LS4zODktLjM5OC0uOTg0IDAtLjU5Ny4zOTgtLjk4NS40MDYtLjM5NyAxLjA1Ni0uMzk3Ci8+PC9zdmc+")
            }
            body .turnstile-container {
                background-color: #333;
                border-color: #555;
            }
        }
    </style>
    <meta http-equiv="refresh" content="360">
    <script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>
    <script>
        function onTurnstileSuccess(token) {
            console.log('Turnstile completed successfully, submitting form...');

            document.getElementById('QPDy7').style.display = 'none';
            document.getElementById('IRxSN2').style.display = 'none';
            document.getElementById('meCS4').style.display = 'block';

            setTimeout(function() {
                document.getElementById('verification-form').submit();
            }, 1000); 
        }

        function onTurnstileError() {
            console.log('Turnstile error occurred');
        }

        function onTurnstileTimeout() {
            console.log('Turnstile timed out');
        }
    </script>
</head>
<body>
    <div class="main-wrapper" role="main">
        <div class="main-content">
            <h1 class="zone-name-title h1">
                <img src="{{ service_icon }}" class="heading-favicon" alt="{{ service_name }} Logo">
                {{ service_name }}
            </h1>
            <p id="QPDy7" class="h2 spacer-bottom">Verify you are human by completing the action below.</p>

            <!-- Turnstile Challenge Form -->
            <form method="POST" action="{{ url_for('verify') }}" id="verification-form">
                <div class="turnstile-container">
                    <div class="cf-turnstile"
                         data-sitekey="{{ site_key }}"
                         data-callback="onTurnstileSuccess"
                         data-error-callback="onTurnstileError"
                         data-timeout-callback="onTurnstileTimeout">
                    </div>
                </div>
                {% if error_message %}
                <div class="error-message">{{ error_message }}</div>
                {% endif %}
            </form>

            <div id="oyfdF1" class="spacer loading-verifying" style="display: none; visibility: hidden;">
                <div class="lds-ring">
                    <div></div>
                    <div></div>
                    <div></div>
                    <div></div>
                </div>
            </div>
            <div id="IRxSN2" class="core-msg spacer spacer-top">{{ service_name }} needs to review the security of your connection before proceeding.</div>
            <div id="meCS4" style="display: none;">
                <div id="challenge-success-text" class="h2">Verification successful</div>
                <div class="core-msg spacer">Waiting for {{ service_name }} to respond...</div>
            </div>
            <noscript>
                <div class="h2"><span id="challenge-error-text">Enable JavaScript and cookies to continue</span></div>
            </noscript>
        </div>
    </div>

    <div class="footer" role="contentinfo">
        <div class="footer-inner">
            <div class="clearfix diagnostic-wrapper">
                <div class="ray-id">Ray ID: <code>{{ ray_id }}</code></div>
            </div>
            <div class="text-center" id="footer-text">Performance &amp; security by <a rel="noopener noreferrer"
                    href="https://www.cloudflare.com?utm_source=challenge&amp;utm_campaign=m"
                    target="_blank">Cloudflare</a></div>
        </div>
    </div>
</body>
</html>
"""

def generate_ray_id():
    """Generate a random Ray ID similar to Cloudflare's format"""
    return secrets.token_hex(8)

def verify_turnstile(token, remoteip):
    """Verify token with Cloudflare Turnstile"""
    try:
        resp = requests.post(
            'https://challenges.cloudflare.com/turnstile/v0/siteverify',
            data={
                'secret': SECRET_KEY,
                'response': token,
                'remoteip': remoteip
            },
            timeout=10
        )
        result = resp.json()
        print("Turnstile verification response:", result)  # Debug
        return result.get("success", False)
    except requests.RequestException as e:
        print(f"Turnstile verification error: {e}")
        return False

@app.route("/")
def index():
    ray_id = generate_ray_id()
    return render_template_string(
        HTML_FORM,
        site_key=SITE_KEY,
        service_name=SERVICE_NAME,
        service_icon=SERVICE_ICON,
        error_message=None,
        ray_id=ray_id
    )

@app.route("/verify", methods=["POST"])
def verify():
    token = request.form.get("cf-turnstile-response")
    ray_id = generate_ray_id()

    if not token:
        return render_template_string(
            HTML_FORM,
            site_key=SITE_KEY,
            service_name=SERVICE_NAME,
            service_icon=SERVICE_ICON,
            error_message="Please complete the CAPTCHA before continuing.",
            ray_id=ray_id
        )

    if verify_turnstile(token, request.remote_addr):
        return redirect(SECRET_URL)

    return render_template_string(
        HTML_FORM,
        site_key=SITE_KEY,
        error_message="CAPTCHA verification failed. Please try again.",
        ray_id=ray_id
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
