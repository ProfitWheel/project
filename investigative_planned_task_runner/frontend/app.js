async function loadTasks() {
  const res = await fetch('/tasks');
  const data = await res.json();
  const table = document.getElementById('tasks');
  table.innerHTML = '';
  const header = document.createElement('tr');
  header.innerHTML = '<th>ID</th><th>Title</th><th>Mode</th><th>Status</th>';
  table.appendChild(header);
  data.forEach((task) => {
    const row = document.createElement('tr');
    row.innerHTML = `<td>${task.id}</td><td>${task.title}</td><td>${task.mode}</td><td>${task.status}</td>`;
    row.addEventListener('click', () => subscribeToTask(task.id));
    table.appendChild(row);
  });
}

let eventSource;

function subscribeToTask(taskId) {
  if (eventSource) {
    eventSource.close();
  }
  document.getElementById('audit').innerHTML = '';
  eventSource = new EventSource(`/stream/tasks/${taskId}`);
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const item = document.createElement('li');
    item.textContent = `${data.created_at} – ${data.message}`;
    document.getElementById('audit').appendChild(item);
  };
}

loadTasks();
