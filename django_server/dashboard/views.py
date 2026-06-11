import json
import os
import secrets
from functools import wraps
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import urlopen

from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods


ALLOWED_SHEETS = {
    "Verbas - Resumo",
    "CCA",
    "CPD",
    "CCF",
    "CIIC",
    "SAÚDE",
    "LEGAL OPS",
    "COMP",
    "MBA LID",
    "CONGRESSO",
}


def dashboard_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get("dashboard_authenticated"):
            return view_func(request, *args, **kwargs)
        return redirect("login")

    return wrapper


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.session.get("dashboard_authenticated"):
        return redirect("dashboard")

    error = ""
    if request.method == "POST":
        expected_user = os.environ.get("DASHBOARD_USERNAME", "")
        expected_password = os.environ.get("DASHBOARD_PASSWORD", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        valid_user = secrets.compare_digest(username, expected_user)
        valid_password = secrets.compare_digest(password, expected_password)
        if expected_user and expected_password and valid_user and valid_password:
            request.session["dashboard_authenticated"] = True
            return redirect("dashboard")
        error = "Usuário ou senha inválidos."

    return render(request, "dashboard/login.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("login")


@dashboard_login_required
def dashboard(request):
    return render(request, "dashboard/index.html")


@dashboard_login_required
def sheet_values(request, sheet_name):
    if sheet_name not in ALLOWED_SHEETS:
        return JsonResponse({"error": "Aba não permitida."}, status=404)

    api_key = os.environ.get("GOOGLE_SHEETS_API_KEY")
    sheet_id = os.environ.get("LEC_CURRENT_SHEET_ID")
    if not api_key or not sheet_id:
        return JsonResponse({"error": "Credenciais do Google Sheets não configuradas no servidor."}, status=500)

    url = (
        "https://sheets.googleapis.com/v4/spreadsheets/"
        f"{quote(sheet_id)}/values/{quote(sheet_name, safe='')}?key={quote(api_key)}"
    )

    try:
        with urlopen(url, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        return JsonResponse({"error": f"Google Sheets retornou HTTP {exc.code}."}, status=exc.code)
    except URLError:
        return JsonResponse({"error": "Falha de conexão com Google Sheets."}, status=502)
    except TimeoutError:
        return JsonResponse({"error": "Tempo esgotado ao consultar Google Sheets."}, status=504)

    return JsonResponse({"values": payload.get("values", [])})
