
# BuyOrder Django API

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running with Docker](#running-with-docker)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Overview
This project is a simple Django-based API for managing buy orders of a specific currency. The API allows users to place orders, and the system will handle various scenarios like insufficient balance, invalid currency, and aggregating orders below a certain threshold before buying from an external exchange.

## Features
- User account management with balance deduction.
- Currency and order management.
- Automatic handling of orders with total prices below $10.
- Handling of external exchange purchases for orders over $10.
- API endpoint for placing buy orders.
- Dockerized environment for easy deployment.
- Comprehensive testing for all edge cases.

## Requirements
- Python 3.10
- Django 3.x or later
- Django REST Framework
- Docker (Optional, for containerized deployment)

## Installation

### Clone the repository:
```bash
git clone https://github.com/your-username/buyorder-django-api.git
cd buyorder-django-api
```

### Create and activate a virtual environment:
```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install the required dependencies:
```bash
pip install -r requirements.txt
```

### Apply migrations to set up the database:
```bash
python manage.py migrate
```

### Create a superuser to access the Django admin:
```bash
python manage.py createsuperuser
```

### Run the development server:
```bash
python manage.py runserver
```

The API should now be accessible at `http://127.0.0.1:8000/`.

## Running the Project

1. **Start the server**:
    ```bash
    python manage.py runserver
    ```

2. **Access the Django admin**:
    Go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials.

3. **Place orders via the API**:
    You can use tools like [Postman](https://www.postman.com/) or [cURL](https://curl.se/) to interact with the API.

## Running with Docker

To run this project in a Docker container:

1. **Build the Docker image**:
    ```bash
    docker build -t buyorder-django-api .
    ```

2. **Run the Docker container**:
    ```bash
    docker run -d -p 8000:8000 buyorder-django-api
    ```

The API will be available at `http://127.0.0.1:8000/`.

## API Endpoints

### Place a Buy Order
- **Endpoint**: `/api/orders/`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
        "currency": "ABAN",
        "amount": 2,
        "user_account": 1
    }
    ```
- **Response**:
    - **201 Created**: Returns the created order.
    - **400 Bad Request**: Returns an error message if the request is invalid.

### Example of Request Using `cURL`:
```bash
curl -X POST http://127.0.0.1:8000/api/orders/ \
    -H "Content-Type: application/json" \
    -d '{"currency": "ABAN", "amount": 2, "user_account": 1}'
```

## Testing

To run tests for this project:

1. **Activate your virtual environment**:
    ```bash
    source venv/bin/activate
    ```

2. **Run the tests**:
    ```bash
    python manage.py test
    ```

The test suite covers various scenarios, including successful order placements, insufficient balances, invalid inputs, and more.

## Project Structure

```
buyorder-django-api/
│
├── app/                        # Main application directory
│   ├── migrations/             # Database migrations
│   ├── models.py               # Database models
│   ├── serializers.py          # API serializers
│   ├── views.py                # API views
│   ├── tests.py                # Unit tests for the app
│   └── urls.py                 # URL routing for the app
│
├── buyorder/                   # Project configuration directory
│   ├── settings.py             # Project settings
│   ├── urls.py                 # Project URLs
│   └── wsgi.py                 # WSGI application
│
├── Dockerfile                  # Dockerfile for containerizing the app
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # Project documentation (this file)
```

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code adheres to the existing style and that all tests pass before submitting your PR.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
