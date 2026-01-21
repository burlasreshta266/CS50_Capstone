function markTaskComplete(button){
    id = button.dataset.id;

    const csrftoken = document.querySelector('#csrf-container input').value;

    fetch(`/mark_task_complete/${id}`, {
        method : 'POST',
        headers : {'X-CSRFToken': csrftoken}
    }).then(response => response.json())
    .then(result => {
        const status_p = document.querySelector(`#status-${id}`);
        if(result.curr_status=='completed'){
            status_p.innerHTML = `🟢 completed`;
            document.querySelector(`#div-${id}`).classList.add("d-none");
        }
    })
    .catch(error => console.error('Error:', error));
}


function toggleEdit(identifier) {
    let taskId;
    if (typeof identifier === 'object' && identifier.dataset) {
        taskId = identifier.dataset.id;
    } else {
        taskId = identifier;
    }

    const contentDiv = document.getElementById(`task-content-${taskId}`);
    const editDiv = document.getElementById(`edit-task-${taskId}`);
    const btnDiv = document.getElementById(`div-${taskId}`);

    if (editDiv.classList.contains('d-none')) {
        contentDiv.classList.add('d-none');
        if (btnDiv) btnDiv.classList.add('d-none');
        editDiv.classList.remove('d-none');
    } else {
        contentDiv.classList.remove('d-none');
        if (btnDiv) btnDiv.classList.remove('d-none');
        editDiv.classList.add('d-none');
    }
}


function saveTask(event, form) {
    event.preventDefault();
    const taskId = form.dataset.id;
    const formData = new FormData(form);
    
    const csrftoken = document.querySelector('#csrf-container input').value;

    fetch(`/edit_task/${taskId}`, { 
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById(`task-title-${taskId}`).innerText = data.title;
            document.getElementById(`task-deadline-${taskId}`).innerText = `by ${data.deadline}`;
            
            document.getElementById(`task-content-${taskId}`).classList.remove('d-none');
            document.getElementById(`edit-task-${taskId}`).classList.add('d-none');
            document.getElementById(`div-${taskId}`).classList.remove('d-none');
        } else {
            alert("Error updating task: " + JSON.stringify(data.errors));
        }
    })
    .catch(error => console.error('Error:', error));
}


function markProjectComplete(button) {
    if (!confirm("Are you sure you want to mark this project as complete?")) return;

    const projectId = button.dataset.id;
    const csrftoken = document.querySelector('#csrf-container input').value;

    fetch(`/mark_project_complete/${projectId}`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const statusText = document.getElementById("project-status-text");
            if (statusText) {
                statusText.innerText = "🟢 Completed";
            }

            const btn = document.getElementById("mark-project-btn");
            if (btn) {
                btn.remove();
            }
        } else {
            alert("Error: " + (data.error || "Could not update project"));
        }
    })
    .catch(error => console.error('Error:', error));
}