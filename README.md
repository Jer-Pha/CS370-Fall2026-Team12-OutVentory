# Out-Ventory

## Getting Started

### 0. Recommended Software

- IDE/text editor: [Visual Studio Code](https://code.visualstudio.com/download)
- GitHub GUI: [GitHub Desktop](https://desktop.github.com/download/)

### 1. Install `uv` (project/dependency manager)

- **macOS / Linux:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- **Windows:**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

_Note: After installing, **close and reopen your terminal** to refresh your path._

### 2. Prepare the Project

_Note: You may need to install [git](https://git-scm.com/install/) before this step. Type `git` in your terminal to check._

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jer-Pha/out-ventory.git
    cd out-ventory
    ```
2.  **Sync the environment:**
    This will download the correct version of Python and all required libraries automatically:
    ```bash
    uv sync
    ```

### 3. Configure your Environment

You need a local environment file to be read by the project.

1.  Create a copy of the example file:
    - **macOS:** `cp .env.example .env`
    - **Windows:** `copy .env.example .env`
2.  (Optional) Open the new `.env` file and update the settings if needed (the defaults should be fine).

### 4. Initialize the Database

Set up the SQLite database tables (run this the first time you set up, and whenever you pull the repo):

```bash
uv run manage.py migrate
```

### 5. Run the App

One-time action, create a local admin user before running the app for the first time:

```bash
uv run manage.py createsuperuser
```

Whenever you want to start the project, run:

```bash
uv run manage.py runserver
```

You can now open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

### 6. Code Formatting

To keep our code formatted, this project uses `ruff`. You can manually run these commands at any time from the project directory:

```bash
uv run ruff check .
uv run ruff format .
```

_Note: This check is run on all pull requests and pushes to main to ensure the codebase stays formatted._
