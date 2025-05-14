# Delivery Order Price Calculator (DOPC) 🚚💰

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68.0-green?style=for-the-badge&logo=fastapi)
![pytest](https://img.shields.io/badge/pytest-6.2.5-yellow?style=for-the-badge&logo=pytest)

## 📄 Table of Contents
- [Delivery Order Price Calculator (DOPC) 🚚💰](#delivery-order-price-calculator-dopc-)
  - [📄 Table of Contents](#-table-of-contents)
  - [🎯 Overview](#-overview)
  - [✨ Key Features and Highlights](#-key-features-and-highlights)
  - [🔧 Technologies Used](#-technologies-used)
  - [🏛 Architecture Overview](#-architecture-overview)
  - [🚀 Running the Application](#-running-the-application)
    - [Prerequisites](#prerequisites)
    - [Steps](#steps)
  - [📖 API Documentation](#-api-documentation)
    - [Calculate Delivery Order Price](#calculate-delivery-order-price)
      - [Query Parameters](#query-parameters)
      - [Example Request](#example-request)
      - [Successful Response](#successful-response)
      - [Error Responses](#error-responses)
  - [🧪 Testing API](#-testing-api)
    - [Running Tests](#running-tests)
    - [Test Coverage](#test-coverage)
  - [📝 Project Structure](#-project-structure)
  - [👷🏻‍♂ Design Patterns and SOLID Principles](#-design-patterns-and-solid-principles)
    - [Design Patterns](#design-patterns)
    - [SOLID Principles](#solid-principles)
  - [📈 Performance and Scalability](#-performance-and-scalability)
  - [📚 Documentation](#-documentation)
  - [📬 Contact Information](#-contact-information)

## 🎯 Overview

The **Delivery Order Price Calculator (DOPC)** is a backend service designed to compute the total price of a delivery order, providing a detailed breakdown that includes cart value, delivery fee, and any applicable surcharges. This project was developed as a preliminary assignment for the Wolt 2025 Backend Engineering Internship, showcasing advanced backend development skills and adherence to best practices.

## ✨ Key Features and Highlights

- **Modular Architecture 🗂️:** Clean MVC structure promoting maintainability.
- **SOLID Principles 🎯:** Strong adherence, especially in Dependency Injection.
- **Design Patterns 🧩:** Strategic use of Strategy, Singleton, and Observer patterns.
- **Asynchronous Programming ⚡:** Enhances performance and scalability.
- **Background Tasks 🕒:** Non-blocking logging operations.
- **Robust Exception Handling 🚫:** Custom exceptions and global handlers.
- **Comprehensive Testing 🧪:** High test coverage with unit and integration tests.
- **Flexible Logging System 📜🖥️:** Observer pattern for configurable log destinations.
- **Robust API Client 🔄⏱️:** Retries, timeouts, and thread-safe singleton implementation.
- **Dynamic Configuration Management 🛠️:** Environment variables and `pydantic-settings`.
- **Clean Input Validation ✅:** Effective and robust validation.
- **Comprehensive Documentation 📚:** High-quality inline and external documentation.

## 🔧 Technologies Used

- **Programming Language:** Python 3.9+
- **Frameworks & Libraries:** FastAPI, Pydantic, httpx, pytest
- **Tools:** Github
- **Design Patterns:** Strategy, Singleton, Observer

## 🏛 Architecture Overview

The DOPC service follows a modular MVC architecture, separating concerns across different layers:
- **Routers:** Define API endpoints and handle request routing.
- **Models:** Define Pydantic models for request validation and response schemas.
- **Services:** Contain business logic for price calculation and interactions with external APIs.
- **Integrations:** Handle communication with external services like the Home Assignment API.
- **Middlewares:** Manage cross-cutting concerns like logging and error handling.
- **Utils:** Provide utility classes and strategies for distance calculation and pricing.
- **Exceptions:** Define custom exceptions and their handlers for consistent error responses.

## 🚀 Running the Application

### Prerequisites
- **Python 3.9+**: Ensure Python is installed. You can download it from the [official website](https://www.python.org/downloads/).
- **Git**: To clone the repository.

### Steps

1. **Clone the Repository**
    ```bash
    git clone https://github.com/3laaHisham/Wolt_Assignment.git # or unzip the file you downloaded
    cd wolt_assignment
    ```

2. **Create a Virtual Environment**
    ```bash
    pip install pipenv
    pipenv install
    pipenv shell
    ```

3. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Start the Server**
    ```bash
    cd src
    uvicorn main:app --env-file ../.env.local
    ```

## 📖 API Documentation

### Calculate Delivery Order Price

`GET /api/v1/delivery-order-price`

#### Query Parameters
- `venue_slug` (string, required): Unique identifier for the venue.
- `cart_value` (integer, required): Total value of the items in the shopping cart (in cents).
- `user_lat` (float, required): Latitude of the user's location.
- `user_lon` (float, required): Longitude of the user's location.

#### Example Request
```bash
curl "http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087"
```
#### Successful Response
```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```
#### Error Responses
```plaintext
- **400 Bad Request:** Delivery not possible due to distance constraints.
- **404 Not Found:** Venue not found.
- **503 Service Unavailable:** Issues with external API or service.
- **504 Gateway Timeout:** External API timeout.
- **422 Unprocessable Entity:** Validation errors for request parameters.
```
    
## 🧪 Testing API

### Running Tests

```bash
cd src # if not already in src
pytest --disable-warnings --verbose --color=yes
```

### Test Coverage

<details>
<summary>Coverage Report</summary>

![image](https://github.com/3laaHisham/Wolt_Assignment/blob/main/coverage.png)
    
</details>

## 📝 Project Structure

```plaintext
src/
├── config.py
├── dependencies.py
├── main.py
├── exceptions/
│   ├── __init__.py
│   ├── handlers.py
│   ├── invalid_distance.py
│   └── venue_not_found.py
├── integrations/
│   └── home_api_client.py
├── middlewares/
│   ├── exception_handler.py
│   └── logging_middleware.py
├── models/
│   ├── delivery_request_v1.py
│   ├── delivery_response_v1.py
│   └── home_api_response.py
├── routers/
│   └── delivery_router_v1.py
├── services/
│   ├── delivery_service.py
│   └── delivery_strategy.py
├── tests/
│   ├── conftest.py
│   ├── integration/
│   │   └── test_delivery_service_integration.py
│   └── unit/
│       ├── test_api_client.py
│       ├── test_delivery_endpoint.py
│       ├── test_delivery_service.py
│       ├── test_distance_strategy.py
│       ├── test_logging.py
│       ├── test_models.py
│       └── test_pricing_strategy.py
├── utils/
│   ├── distance/
│   │   ├── __init__.py
│   │   ├── base_distance_strategy.py
│   │   ├── euclidean_calculator.py
│   │   └── haversine_calculator.py
│   ├── loggers/
│   │   ├── console_destination.py
│   │   ├── file_destination.py
│   │   ├── logger.py
│   │   └── log_destination.py
│   └── pricing/
│       ├── base_pricing_strategy.py
│       └── distance_pricing.py
└── README.md
```

## 👷🏻‍♂ Design Patterns and SOLID Principles

### Design Patterns

- **Strategy Pattern:** Used for distance calculations (`DistanceStrategy`) and pricing strategies (`PricingStrategy`). This allows for easy swapping of algorithms, such as upgrading to public map distance calculations or including royalties in pricing.
- **Singleton Pattern:** Applied to the `ApiClient` and `Logger` to ensure a single instance throughout the application, optimizing resource usage and maintaining consistent state.
- **Observer Pattern:** Implemented in the `Logger` to flexibly add or remove log destinations based on environment variables, enhancing the logging system's configurability.

### SOLID Principles

- **Single Responsibility Principle:** Each class or module handles one responsibility, simplifying maintenance.
- **Open/Closed Principle:** The system allows extensions without modifying existing code, as seen in <em>Strategy</em> and <em>Observer</em> patterns.
- **Liskov Substitution Principle:** Subtypes replace base types without affecting program correctness.
- **Interface Segregation Principle:** Interfaces are specific to client needs, avoiding unnecessary methods.
- **Dependency Inversion Principle:** High-level and low-level modules rely on abstractions, supported by <em>FastAPI's dependency injection</em> for loose coupling and testability.


## 📈 Performance and Scalability
- **Asynchronous Operations ⚡:**
  - Leverages asynchronous programming paradigms throughout the application to handle multiple requests efficiently.
  - Enhances throughput and reduces latency, making the service scalable under high load.
  
- **Thread-Safe Implementations 🧵:**
  - Ensures thread safety in singleton implementations using locks, preventing race conditions and ensuring consistent behavior.
  
- **Efficient Resource Management 🔄:**
  - Uses context managers and graceful shutdown procedures to manage resources effectively, preventing memory leaks and dangling connections.

## 📚 Documentation

- **Inline Code Documentation 📖:**
  - Docstrings and comments throughout the codebase provide clear explanations of classes and methods.
  - Facilitates easier onboarding for new contributors and streamlines maintenance processes.

- **API Documentation 📝:**
  - Automatically generated interactive API docs available at `/redoc`
  - Includes detailed schemas, parameter descriptions, and example requests/responses.


## 📬 Contact Information

- **Alaa Hisham**
- **Email:** [alaaismail286@gmail.com](mailto:alaaismail286@gmail.com)
- **LinkedIn:** [linkedin.com/in/alaahisham/](https://www.linkedin.com/in/alaahisham/)
- **GitHub:** [github.com/3laaHisham](https://github.com/3laaHisham)
