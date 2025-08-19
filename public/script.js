const API_BASE = '/api';

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

// Example login/register functions
async function registerUser(username, password){
  const data = await apiPost('/register', { username, password });
  alert(data.message || data.error);
}

async function loginUser(username, password){
  const data = await apiPost('/login', { username, password });
  alert(data.message || data.error);
}

async function addJournal(username, entry){
  const data = await apiPost('/journal', { username, entry });
  console.log(data);
}

async function getJournal(username){
  const data = await apiGet(`/journal?username=${username}`);
  console.log(data);
}
