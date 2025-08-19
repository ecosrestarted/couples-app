const API_BASE = '/api';
let currentUser = localStorage.getItem('user') || null;

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

async function registerUser(){
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const data = await apiPost('/register', { username, password });
  alert(data.message || data.error);
}

async function loginUser(){
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const data = await apiPost('/login', { username, password });
  if(data.message){
    alert(data.message);
    currentUser = username;
    localStorage.setItem('user', username);
    window.location.href = '/dashboard';
  } else alert(data.error);
}

async function addJournal(){
  const entry = document.getElementById('entry').value;
  if(!currentUser) return alert('Login first!');
  const data = await apiPost('/journal', { username: currentUser, entry });
  displayJournal(data.journal);
  document.getElementById('entry').value = '';
}

async function getJournal(){
  if(!currentUser) return;
  const data = await apiGet(`/journal?username=${currentUser}`);
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

// Load journal on dashboard
window.onload = () => {
  if(window.location.pathname.includes('dashboard')) getJournal();
}
