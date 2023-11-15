#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """validate register user endpoint"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://0.0.0.0:5000/users', data=data)

    payload = {"email": email, "message": "user created"}

    assert resp.status_code == 200
    assert resp.json() == payload


def log_in_wrong_password(email: str, password: str) -> None:
    """validate user login enpoint wrong_password"""
    data = {'email': email, 'password': password}
    resp = requests.post('http://0.0.0.0:5000/sessions', data=data)

    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """validate user login endpoint"""
    data = {'email': email, 'password': password}
    payload = {"email": email, "message": "logged in"}

    resp = requests.post('http://0.0.0.0:5000/sessions', data=data)

    assert resp.status_code == 200
    assert resp.json() == payload
    return resp.cookies.get('session_id')


def profile_unlogged() -> None:
    """validates profile enpoint unlogged"""
    resp = requests.get('http://0.0.0.0:5000/profile')

    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """validates profile enpoint logged"""
    cookies = {'session_id': session_id}
    payload = {'email': 'guillaume@holberton.io'}
    resp = requests.get('http://0.0.0.0:5000/profile', cookies=cookies)

    assert resp.status_code == 200
    assert resp.json() == payload


def log_out(session_id: str) -> None:
    """validate user logout endpoint"""
    endpoint = 'http://0.0.0.0:5000/logout'
    cookies = {'session_id': session_id}
    resp = requests.delete(endpoint, cookies=cookies)

    assert resp.status_code == 200


def reset_password_token(email: str) -> str:
    """validate reset_password enpoint"""
    endpoint = 'http://0.0.0.0:5000/reset_password'
    data = {'email': email}

    resp = requests.post(endpoint, data=data)

    assert resp.status_code == 200

    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """validate update_password enpoint"""
    endpoint = 'http://0.0.0.0:5000/reset_password'
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password
            }
    payload = {"email": email, "message": "Password updated"}

    resp = requests.put(endpoint, data=data)

    assert resp.status_code == 200
    assert resp.json() == payload


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
