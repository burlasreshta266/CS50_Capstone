# Project Manager - CS50w Capstone

This is a Project Management web application designed to help users organize software projects, track development technologies, and manage tasks with deadlines. It allows users to create projects, assign specific technology stacks (e.g., Python, JavaScript), and manage a dynamic list of tasks within those projects without constant page reloads.

## Distinctiveness and Complexity

This project satisfies the distinctiveness and complexity requirements for the following reasons:

### Distinctiveness
This project is neither a social network, e-commerce site, nor an encyclopedia. Instead, it is a productivity and organizational tool designed for developers. Unlike the standard course projects (like "Network" or "Commerce"), this application focuses on:
* **Hierarchical Data Management:** Managing the relationship between Users, Projects, Technologies, and Tasks.
* **Workflow Tracking:** Tracking the status of both high-level Projects and individual Tasks (Ongoing vs. Completed).
* **Deadline Management:** Handling date-time inputs specifically for task deadlines.

### Complexity
The application exceeds the complexity of standard problem sets through:
1.  **Single Page Application (SPA) Features:**
    * Task editing and status updates utilize **AJAX (Fetch API)** to communicate with the server.
    * Users can edit a task's title and deadline inline. The form appears dynamically, saves data to the backend via a JSON API, and updates the DOM immediately without a page reload.
    * Projects can be marked as "Completed" directly from the dashboard using asynchronous requests.
2.  **Complex Database Relationships:**
    * It utilizes a **Many-to-Many** relationship between `Project` and `Technology`, allowing a scalable way to tag projects with their tech stack.
    * It uses `ForeignKey` relationships to link Tasks to Projects and Projects to Users.
3.  **Dynamic UI/UX:**
    * Technologies can be added dynamically via a **Bootstrap Modal** inside the "Create Project" form. This uses JavaScript to POST data to the server and immediately append the new technology to the selection dropdown without refreshing the form.
    * Responsive design using Bootstrap 5 grid system to handle mobile (stacked) vs. desktop (sidebar) layouts.

## File Contents

### `projectManager/`
* **`models.py`**: Defines the database schema:
    * `User`: Standard Django AbstractUser.
    * `Technology`: A simple model to store tech stack names (e.g., "Django", "React").
    * `Project`: Stores project metadata, links to the Creator, and has a Many-to-Many relationship with `Technology`.
    * `Task`: Individual items linked to a Project, containing deadlines and status.
* **`views.py`**: Contains the application logic. It includes:
    * Standard views: `index`, `login`, `register`, `home`, `create_project`.
    * **API views**: `edit_task`, `mark_task_complete`, `add_technology`, `mark_project_complete`, `add_task`. These return `JsonResponse` objects for the JavaScript frontend to consume.
* **`urls.py`**: Defines the URL patterns, including distinct paths for the API endpoints used by the frontend scripts.
* **`forms.py`**: Contains `ModelForm` definitions (`ProjectForm`, `TaskForm`, `TechnologyForm`, `RegistrationForm`) with custom widgets to apply Bootstrap styling and DatePickers.

### `projectManager/static/projectManager/`
* **`scripts.js`**: The core JavaScript file containing the logic for:
    * `markTaskComplete()`: Sends async POST requests to update task status.
    * `toggleEdit()`: Toggles the visibility of the edit form vs. the display text.
    * `saveTask()`: Handles the submission of the edit form via AJAX, updates the DOM with new data, and closes the form.
    * `markProjectComplete()`: Handles project status updates.
* **`styles.css`**: Custom CSS overrides for the application, including specific styling for the "technology tags" and custom scrollbars for the task list.

### `projectManager/templates/projectManager/`
* **`layout.html`**: The base template containing the HTML structure, Bootstrap CDN links, and the navigation block.
* **`index.html`**: The landing page for unauthenticated users.
* **`home.html`**: The user's dashboard displaying a grid of their active and completed projects.
* **`project.html`**: The main detail view. It features a responsive layout with project details on the left (or top) and a scrollable task list on the right (or bottom). It includes hidden forms for editing tasks that are toggled via JS and a modal for adding new tasks.
* **`create_project.html` / `edit_project.html`**: Forms for project management. These include a dynamic Modal for adding new technologies on the fly.
* **`login.html` / `register.html`**: Authentication templates.

## How to Run

1.  **Install Dependencies:**
    If you have a virtual environment, activate it. Then install Django:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Apply Migrations:**
    Set up the database schema:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Run the Server:**
    Start the development server:
    ```bash
    python manage.py runserver
    ```

4.  **Access the App:**
    Open your browser and navigate to `http://127.0.0.1:8000`. Register a new account to get started.