# 🚀 Github-Integration-App

## Project Description

**Github-Integration-App** is a web application that integrates GitHub with a Django and Vue frontend via the GitHub and Google REST API. It allows users to log in using Google Auth, link their GitHub account, and view and select their repositories.

## Technologies Used

- Django
- Django Rest Framework (DRF)
- Vue.js
- Tailwind CSS
- PostgreSQL

## Setup Instructions

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/github-integration-app.git
   cd github-integration-app

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt

 3. Set up environment variables for the Django app (e.g., .env file) including database credentials and API keys.

4. Apply database migrations:
    ```bash
    python manage.py migrate

5. Start the Django server:
  ```bash
python manage.py runserver
```

### Frontend Setup

1. Navigate to the frontend directory:
  ```bash
cd frontend
```
2. Install NPM dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```


## Usage Instructions

1. After setting up the project, navigate to the home page.
2. Sign in using Google Auth.
3. Once logged in, you'll be redirected to a page with a "Link Github Account" button.
4. Authorize the app to access your GitHub account.
5. You will then see a list of available repositories. Select a repository to store the GitHub token, username, and selected repository in the PostgreSQL database.

## Deployment Instructions
N/A
### Contributing
**Contributions are welcome! The current Webhook implementation is not complete, so suggestions or contributions are appreciated. Feel free to open an issue or submit a pull request.**

