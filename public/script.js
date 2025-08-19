const API_BASE = '/api';
let currentUser = null;

async function apiPost(path, data){
  const res = await fetch(API_BASE + path, {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify(data)
  });
  return res.json();
}

async function apiGet(path){
  const res = await fetch(API_BASE + path);
  return res.json();
}

async function registerUser(username, password){
  const data = await apiPost('/register', { username, password });
  alert(data.message || data.error);
}

async function loginUser(username, password){
  const data = await apiPost('/login', { username, password });
  if(data.message){
    alert(data.message);
    currentUser = username;
    window.location.href = 'dashboard.html';
  } else alert(data.error);
}

async function addJournal(username, entry){
  if(!username) return alert('Not logged in');
  const data = await apiPost('/journal', { username, entry });
  console.log(data);
  displayJournal(data.journal);
}

async function getJournal(username){
  const data = await apiGet(`/journal?username=${username}`);
  displayJournal(data.journal);
}

function displayJournal(entries){
  const list = document.getElementById('journalList');
  if(!list) return;
  list.innerHTML = '';
  entries.forEach(e => {
    const li = document.createElement('li');
    li.textContent = e;
    list.appendChild(li);
  });
}
