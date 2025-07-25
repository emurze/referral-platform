# API Documentation

This document describes the API endpoints available for authentication and user profile management.

---

## Authentication

### 1. Login (Send Verification Code)

- **URL:** `/auth/login/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "phone_number": "+1234567890"
  }
  ```

- **Response:**

  - **200 OK**

    ```json
    {
      "message": "Verification code sent",
      "verification_code": "123456"
    }
    ```

  - **400 Bad Request**

    ```json
    {
      "phone_number": ["Enter a valid phone number."]
    }
    ```

- **Description:**
  Accepts a phone number and sends a verification code.  
  **Note:** For demo/testing, the verification code is returned in the JSON response. In production, the code would be sent via SMS or email.

---

### 2. Verify Code

- **URL:** `/auth/verify-code/`
- **Method:** `POST`
- **Request Body:**

  ```json
  {
    "phone_number": "+1234567890",
    "verification_code": "123456"
  }
  ```

- **Response:**

  - **200 OK**

    ```json
    {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    }
    ```

  - **400 Bad Request**

    ```json
    {
      "detail": "Verification code is invalid or expired"
    }
    ```

  - **404 Not Found**

    ```json
    {
      "detail": "User not found"
    }
    ```

- **Description:**
  Verifies the received code and returns a authentication token if valid.

---

## User Profile

### 3. Get Profile

- **URL:** `/profile/`
- **Method:** `GET`
- **Headers:**

  ```
  Authorization: Token <token>
  ```

- **Response:**

  - **200 OK**

    ```json
    {
      "id": 1,
      "phone_number": "+1234567890",
      "my_referral_code": "ABC123",
      "used_referral_code": null,
      "referrals": ["+1234567891"]
    }
    ```

  - **401 Unauthorized**

    ```json
    {
      "detail": "Authentication credentials were not provided."
    }
    ```

- **Description:**
  Retrieves the authenticated user's profile information.

---

### 4. Set Referrer Code

- **URL:** `/profile/set-referrer/`
- **Method:** `PUT`
- **Headers:**

  ```
  Authorization: Token <token>
  ```

- **Request Body:**

  ```json
  {
    "referral_code": "REF123"
  }
  ```

- **Response:**

  - **200 OK**

    ```json
    {
      "status": "Referral code successfully set"
    }
    ```

  - **400 Bad Request**

    ```json
    {
      "referral_code": ["This referral code is invalid or expired."]
    }
    ```

  - **401 Unauthorized**

    ```json
    {
      "detail": "Authentication credentials were not provided."
    }
    ```

- **Description:**
  Sets a referral code for the authenticated user. 
The code must be valid and not previously used.

---

# Notes

- All endpoints that require authentication expect a Authentication token 
passed in the `Authorization` header as `Token <token>`.
- Validation errors return a 400 status with details in the response body.
- The verification code handling in the `login` 
endpoint is simplified for demonstration purposes.

---