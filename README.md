# BudgetExpense

Welcome to BudgetExpense Project! This project is designed to help users manage expenses, categorize transactions, 
define budgets for specific expense categories, and leverage advanced analytics features..

## Table of Contents
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Authentication](#authentication)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)


## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- Python
- Django
- Other dependencies...

### Installation

1. Clone the repository:

    bash
    git clone https://github.com/beloved10/ExpenseBudget.git
    

2. Navigate to the project directory:

    bash
    cd BudgetExpense/expTracker
    

3. Install dependencies:

    bash
    pip install -r requirements.txt
    

4. Run migrations:

    bash
    python manage.py migrate
    

5. Start the development server:

    bash
    python manage.py runserver
    

Now your application should be running locally.

## Authentication

This project uses [Django REST Framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/) for JSON Web Token (JWT) authentication. 
To authenticate, follow the instructions in the API documentation.

## API Documentation

Visit the [Swagger UI](http://localhost:8000/api/schema/swagger-ui/) endpoint to understand how to use the API.

## Contributing

Interested in contributing? Follow these steps:

1. Fork the project.
2. Create your feature branch (git checkout -b feature/YourFeature).
3. Commit your changes (git commit -m 'Add some feature').
4. Push to the branch (git push origin feature/YourFeature).
5. Open a pull request.
