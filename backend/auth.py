"""
Google OAuth 2.0 Authentication Blueprint for Flask Backend
Handles authentication flow, token management, and route protection.
"""

from flask import Blueprint, request, jsonify, session, redirect, current_app
import requests
import os
from functools import wraps
from datetime import datetime
import secrets

# Create a Blueprint for auth routes
auth_bp = Blueprint('auth', __name__)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/auth/google/callback')

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def login_required(f):
    """Decorator to protect routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required', 'authenticated': False}), 401
        return f(*args, **kwargs)
    return decorated_function


@auth_bp.route('/auth/google/login', methods=['GET'])
def google_login():
    """Initiate Google OAuth flow"""
    if not GOOGLE_CLIENT_ID:
        return jsonify({'error': 'GOOGLE_CLIENT_ID environment variable not set'}), 500

    # Generate random state for CSRF protection
    state = secrets.token_urlsafe(32)
    session['oauth_state'] = state

    # Build authorization URL
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'state': state,
        'access_type': 'offline',
        'prompt': 'select_account'
    }

    query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
    auth_url = f"{GOOGLE_AUTH_URL}?{query_string}"

    return jsonify({
        'auth_url': auth_url,
        'state': state
    })


@auth_bp.route('/auth/google/callback', methods=['GET'])
def google_callback():
    """Handle Google OAuth callback"""
    # Verify state to prevent CSRF
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return jsonify({'error': 'Invalid state parameter'}), 400

    # Get authorization code
    code = request.args.get('code')
    if not code:
        error = request.args.get('error')
        return jsonify({'error': f'Authorization failed: {error}'}), 400

    try:
        # Exchange code for tokens
        token_data = {
            'code': code,
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'redirect_uri': GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        token_response.raise_for_status()
        tokens = token_response.json()

        # Get user info
        headers = {'Authorization': f"Bearer {tokens['access_token']}"}
        userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()

        # Store user info in session
        session['user'] = {
            'id': user_info.get('sub'),
            'email': user_info.get('email'),
            'name': user_info.get('name'),
            'picture': user_info.get('picture'),
            'email_verified': user_info.get('email_verified')
        }
        session['tokens'] = {
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token'),
            'expires_at': datetime.now().timestamp() + tokens.get('expires_in', 3600)
        }

        # Redirect to frontend with success
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/auth/success")

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'OAuth failed: {str(e)}'}), 500


@auth_bp.route('/auth/status', methods=['GET'])
def auth_status():
    """Check if user is authenticated"""
    if 'user' in session:
        return jsonify({
            'authenticated': True,
            'user': session['user']
        })
    return jsonify({'authenticated': False}), 401


@auth_bp.route('/auth/logout', methods=['POST'])
def logout():
    """Logout user and clear session"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})


@auth_bp.route('/auth/refresh', methods=['POST'])
def refresh_token():
    """Refresh access token using refresh token"""
    if 'tokens' not in session or 'refresh_token' not in session['tokens']:
        return jsonify({'error': 'No refresh token available'}), 401

    try:
        token_data = {
            'refresh_token': session['tokens']['refresh_token'],
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'grant_type': 'refresh_token'
        }

        response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
        response.raise_for_status()
        tokens = response.json()

        # Update tokens in session
        session['tokens']['access_token'] = tokens['access_token']
        session['tokens']['expires_at'] = datetime.now().timestamp() + tokens.get('expires_in', 3600)

        return jsonify({'message': 'Token refreshed successfully'})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Token refresh failed: {str(e)}'}), 500


# Protected route example
@auth_bp.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Get user profile (protected route)"""
    return jsonify({
        'user': session['user']
    })
