# WisePenny

A minimalistic web application to log and analyze your expenses.

## Features

- Log expenses with date, description, amount, method, category, and type.
- View all logged expenses.
- Separate tracking of cash and checking account balances.
- Add funds to either cash or checking account balances.
- View detailed balance breakdown between cash and checking accounts.
- Remove and edit logged expenses.

## Development Setup

1. Clone the repository:

    ```sh
    git clone git@github.com:user/WisePenny.git
    cd WisePenny
    ```

2. Create virtual environment:

    ```sh
    python -m venv wpenv
    source ./wpenv/bin/activate
    ```

3. Install requirements:

    ```sh
    pip install -r requirements.txt
    ```

4. Run Flask backend application:

    ```sh
    export FLASK_APP='./backend/main.py'
    export FLASK_ENV='dev'
    flask run
    ```

5. Install npm modules and run development server:

    ```sh
    cd frontend
    npm install
    npm run start
    ```

6. Open up `http://localhost:3000` on a browser to see local changes as you develop.

## Usage

### Adding Funds

### Viewing Balance

### Adding an Expense


### Removing an Expense

TODO: fill description

### Editing an Expense

TODO: fill description

### Viewing All Expenses

TODO: fill description

### Analyzing Expenses

TODO: fill description

## Current Development To-Do List

TODO: fill description

### Future Development

1. **Web Application Development**
    - Enable users to view and analyze their expenses from any device.

2. **Feature Enhancements**
    - Enable categorization and tagging of expenses for better tracking and reporting.
    - Provide detailed reports and visualizations for financial insights.
    - Implement notifications and reminders for upcoming expenses or budget limits.
    - Integrate with bank APIs to automatically log transactions.

3. **Mobile Application Development**
    - Develop a mobile application for on-the-go expense tracking.
    - Synchronize data between the web and mobile applications.

4. **Improved Analytics**
    - Enhance the analysis features to provide more detailed insights.
