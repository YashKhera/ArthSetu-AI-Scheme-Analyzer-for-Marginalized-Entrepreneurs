"""Google OAuth 2.0 (Authorization Code) router."""
import logging
import urllib.parse
import urllib.request
import urllib.error

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.services.auth_service import AuthService
from app.utils.security import create_oauth_state_token, verify_oauth_state_token

router = APIRouter()
logger = logging.getLogger("arthsetu.oauth")


def _login_redirect(error: str = None) -> RedirectResponse:
    target = f"{settings.FRONTEND_URL}/login.html"
    if error:
        target += f"?error={urllib.parse.quote(error)}"
    return RedirectResponse(target)


@router.get("/auth/google")
def google_login():
    """Start the Google sign-in flow.

    Redirects the browser to Google's consent screen. If OAuth is not
    configured, bounces back to the login page with an error hint.
    """
    if not settings.google_oauth_enabled:
        return _login_redirect("google_not_configured")

    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": create_oauth_state_token(),
        "prompt": "select_account",
    }
    url = settings.GOOGLE_AUTH_URL + "?" + urllib.parse.urlencode(params)
    return RedirectResponse(url, status_code=302)


@router.get("/auth/google/callback")
def google_callback(
    code: str = None,
    state: str = None,
    error: str = None,
    db: Session = Depends(get_db),
):
    """Handle Google's redirect back to the app.

    Exchanges the authorization code for an access token, loads the user's
    Google profile, links/creates the ArthSetu account, then hands the browser
    a JWT access token via the frontend's oauth callback page.
    """
    if error or not code or not state:
        return _login_redirect(error or "oauth_cancelled")

    if not verify_oauth_state_token(state):
        return _login_redirect("oauth_invalid_state")

    if not settings.google_oauth_enabled:
        return _login_redirect("google_not_configured")

    # 1) Exchange the code for tokens
    token_data = urllib.parse.urlencode({
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.google_redirect_uri,
        "grant_type": "authorization_code",
    }).encode()

    try:
        req = urllib.request.Request(
            settings.GOOGLE_TOKEN_URL,
            data=token_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            token_json = resp.read(100_000)
        import json as _json
        token_payload = _json.loads(token_json)
    except (urllib.error.URLError, ValueError) as exc:
        logger.error("Google token exchange failed: %s", exc)
        return _login_redirect("oauth_failed")

    access_token = token_payload.get("access_token")
    if not access_token:
        logger.error("No access_token in Google response: %s", token_payload)
        return _login_redirect("oauth_failed")

    # 2) Load the verified Google profile
    try:
        info_url = settings.GOOGLE_USERINFO_URL + "?access_token=" + urllib.parse.quote(access_token)
        with urllib.request.urlopen(info_url, timeout=10) as resp:
            userinfo = json_parse(resp.read(200_000))
    except (urllib.error.URLError, ValueError) as exc:
        logger.error("Google userinfo failed: %s", exc)
        return _login_redirect("oauth_failed")

    email = (userinfo.get("email") or "").strip().lower()
    if not email or not userinfo.get("email_verified"):
        return _login_redirect("oauth_email_unverified")

    # 3) Link/create the account and issue an access token
    user = AuthService.get_or_create_oauth_user(db, email, userinfo.get("name") or "Google User")
    access_tok = AuthService.create_access_token(user.id)

    target = (
        f"{settings.FRONTEND_URL}/oauth/callback.html"
        f"?token={urllib.parse.quote(access_tok)}"
        f"&email={urllib.parse.quote(email)}"
        f"&name={urllib.parse.quote(userinfo.get('name') or '')}"
    )
    return RedirectResponse(target)


def json_parse(data: bytes):
    import json
    return json.loads(data.decode("utf-8"))