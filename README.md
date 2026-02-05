# Project Manager - CS50w Capstone

Welcome to **Project Manager**! This is my final capstone project for CS50’s Web Programming with Python and JavaScript.

The idea behind this app is pretty simple: as developers, we always have a bunch of side projects going on, and it’s hard to keep track of which tech stack we used for what, or which tasks are still pending. I wanted to build a centralized dashboard where I could organize my software projects, tag them with the specific technologies I used (like Python, React, or AWS), and manage a dynamic list of tasks with real deadlines.

## Distinctiveness and Complexity

I believe this project satisfies the distinctiveness and complexity requirements because focuses on productivity logic and hierarchical data management.

### Why it’s Distinct
Instead of just posting text or comments, this application is about managing state and time.
* **It’s Hierarchical:** I had to design a database structure where Users own Projects, Projects own Tasks, and Projects also share a Many-to-Many relationship with Technologies.
* **It’s Time-Sensitive:** Unlike a blog post that just has a timestamp, the tasks here have functional deadlines. The app has to handle datetime inputs from the user and visually flag when things are overdue.
* **It’s a Workflow Tool:** The UI is designed to actually get work done—moving tasks from "Active" to "Completed" and dynamically updating the dashboard.

### Why it’s Complex
I put a lot of effort into making the user experience smooth, which meant writing a lot of custom JavaScript and handling complex database queries.

1.  **Single Page Application (SPA) Feel:**
    I didn't want the user to have to reload the page every time they fixed a typo in a task. I used **AJAX and the Fetch API** heavily here.
    * **Inline Editing:** When you click a task, it transforms into an editable form right on the page. I wrote JavaScript to handle the UI swap, send the data to the backend, and update the DOM without a refresh.
    * **Dynamic Modals:** In the "Create Project" form, I added a feature to create new Technology tags on the fly. This uses a Bootstrap modal and a background Fetch request so you can add a new tag and select it immediately without losing your progress on the main form.

2.  **Database Relationships:**
    * I used a **Many-to-Many relationship** between `Project` and `Technology`. This was tricky because I wanted the technologies to be reusable tags across different projects.
    * I also had to manage `ForeignKeys` carefully so that deleting a project cascades correctly and deletes its tasks, but doesn't mess up the User or the Technology list.

3.  **Dynamic UI:**
    * I implemented responsive design manually using Bootstrap 5. The layout shifts from a sidebar view on desktop to a stacked view on mobile.
    * I also had to do some work on the backend to parse HTML5 datetime inputs into a format that Python's Django could save to the database.

## File Contents

Here is a breakdown of the files I created and the code inside them:

### `projectManager/` (The Django App)
* **`models.py`**: This is where I defined the database schema.
    * `User`: Inherits from `AbstractUser`.
    * `Technology`: A simple model to store tech names (like "Django") so they can be reused.
    * `Project`: The main model. It links to the User and has the Many-to-Many link to Technologies.
    * `Task`: Stores the specific to-do items, deadlines, and completion status (`boolean`).
* **`views.py`**: I split my views into two types:
    * **Standard Views:** `index`, `home`, `create_project`, etc. These render the HTML templates.
    * **API Views:** `edit_task`, `mark_task_complete`, `add_technology`, `add_task`. These are special functions I wrote specifically to return `JsonResponse` objects. My JavaScript files talk to these views to update data without reloading the page.
* **`urls.py`**: I defined all my paths here. I made sure to separate the API paths (like `edit_task/`) from the regular page paths.
* **`forms.py`**: I used Django’s `ModelForm` for the Projects and Tasks. I added custom widgets here to make them look good with Bootstrap, specifically adding the `type="datetime-local"` widget for the deadline input.

### `projectManager/static/projectManager/`
* **`scripts.js`**: This contains all the frontend logic I wrote.
    * `markTaskComplete(id)`: Sends a POST request to toggle the task status and strikes through the text instantly.
    * `toggleEdit(id)`: Hides the text and shows the form for inline editing.
    * `saveTask(id)`: This is the big one—it gathers the data from the inputs, sends it to the API, waits for the response, and then updates the HTML to show the new task info.
    * `markProjectComplete()`: Handles the project status updates from the dashboard.
* **`styles.css`**: I added my custom styling here, like the specific colors for the technology "pills," the scrollbar styling for the task list, and the hover effects for the buttons.

### `projectManager/templates/projectManager/`
* **`layout.html`**: My base template. It has the navbar (which changes if you are logged in or out) and the footer.
* **`index.html`**: The landing page for people who haven't logged in yet.
* **`home.html`**: The main dashboard. It loops through the user's projects and displays them in a grid.
* **`project.html`**: This is the detail view. It shows the project info on one side and the task list on the other. This is where the complex template logic is, including the hidden forms for editing tasks.
* **`create_project.html`**: The form to start a new project. It includes the modal I mentioned earlier for adding new technologies.
* **`login.html` / `register.html`**: The standard auth forms, styled with Bootstrap.

## How to Run

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Make Migrations:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Run the Server:**
    ```bash
    python manage.py runserver
    ```

4.  **Visit the App:**
    Go to `http://127.0.0.1:8000` in your browser.