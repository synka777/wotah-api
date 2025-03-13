# WOTAH-API

[![](https://img.shields.io/static/v1?label=Python&message=v3.12&color=teal)](#) [![](https://img.shields.io/static/v1?label=Django&message=v5.1.7&color=purple)](#)
[![](https://img.shields.io/static/v1?label=Django%20Rest%20Framework&message=v3.15.2)](#)
### Overview

This API allows users to manage their houseplants and associated watering schedules, helping them track the last time each plant was watered or fertilized.

Please note that this project is a work in progress (WIP) meant to be used as a training ground.
This API is designed to work alongside a mobile app, which is still in development. You can find the app  [here](https://github.com/synka777/wotah-app "here").

### Authentication Workflow

The API uses token-based authentication with JSON Web Tokens (JWT). Here’s the general authentication workflow:

1. User registers an account.
2. User logs in, receiving a JWT token.
3. The JWT token is included in the Authorization header for all authenticated requests.
4. If the token expires, the user can refresh it.
5. If the user forgets their password, they can request a password reset.

### Endpoints Overview

##### 1. User Registration

Endpoint: POST /api/register/
Registers a new user with a username, email, and password.

Request Example:

```bash
curl -X POST http://localhost:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "email": "test@example.com", "password": "SecureP@ssw0rd"}'
```

##### 2. User Login

Endpoint: POST /api/login/
Authenticates a user and returns a JWT token.

Request Example:

```bash
curl -X POST http://localhost:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "password": "SecureP@ssw0rd"}'
```
Response Example:

{
  "access": "your_jwt_access_token",
  "refresh": "your_jwt_refresh_token"
}

##### 3. Refresh JWT Token

Endpoint: POST /api/token/refresh/
Refreshes an expired access token using a refresh token.

Request Example:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "your_jwt_refresh_token"}'
```
##### 4. Password Reset Request

Endpoint: POST /api/password-reset-request/
Sends a password reset email to the user.

Request Example:
```bash
curl -X POST http://localhost:8000/api/password-reset-request/ \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com"}'
```
##### 5. Password Reset Confirmation

Endpoint: POST /api/password-reset-confirm/
Resets the user’s password using a token received via email.

Request Example:
```bash
curl -X POST http://localhost:8000/api/password-reset-confirm/ \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "token": "reset_token", "new_password": "NewSecureP@ssw0rd"}'
```
##### 6. Change Password (Authenticated Users)
Endpoint: POST /api/password-reset/

Allows logged-in users to change their password.

Request Example:
```bash
curl -X POST http://localhost:8000/api/password-reset/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_jwt_access_token" \
     -d '{"old_password": "SecureP@ssw0rd", "new_password": "NewSecureP@ssw0rd"}'
```

##### 7. List and Create Plants

Endpoint: GET /api/plants/ (List all plants)
Endpoint: POST /api/plants/ (Create a new plant)

Retrieves all plants belonging to the authenticated user or allows them to create a new plant.

Request Example (List Plants):
```bash
curl -X GET http://localhost:8000/api/plants/ \
     -H "Authorization: Bearer your_jwt_access_token"
```
Request Example (Create Plant):
```bash
curl -X POST http://localhost:8000/api/plants/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_jwt_access_token" \
     -d '{"name": "Fern", "last_watered": "2025-03-10", "watering_frequency": 7, "notes": "Needs indirect light."}'
```
##### 8. Retrieve, Update, or Delete a Plant

- Endpoint: GET /api/plants/<id>/ (Retrieve plant details)
- Endpoint: PUT /api/plants/<id>/ (Update plant details)
- Endpoint: DELETE /api/plants/<id>/ (Delete a plant)

Allows authenticated users to retrieve, update, or delete a specific plant.

Request Example (Retrieve Plant):
```bash
curl -X GET http://localhost:8000/api/plants/1/ \
     -H "Authorization: Bearer your_jwt_access_token"
```
Request Example (Update Plant):
```bash
curl -X PUT http://localhost:8000/api/plants/1/ \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_jwt_access_token" \
     -d '{"name": "Updated Fern", "last_watered": "2025-03-12", "watering_frequency": 5, "notes": "Updated notes."}'
```
Request Example (Delete Plant):
```bash
curl -X DELETE http://localhost:8000/api/plants/1/ \
     -H "Authorization: Bearer your_jwt_access_token"
```
### Notes

Authentication: Except for registration, login, and password reset request, all other endpoints require the Authorization: Bearer <token> header.

**Rate Limits: ** Password reset requests and login attempts are throttled for security.

**Error Handling:** If authentication fails or the token is invalid, the API returns a 401 Unauthorized response.

