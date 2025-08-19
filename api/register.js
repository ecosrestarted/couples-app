let users = {}; // simple in-memory storage

export default function handler(req, res) {
  if (req.method === 'POST') {
    const { username, password } = req.body;
    if (users[username]) return res.status(400).json({ error: 'User exists' });
    users[username] = { password, journal: [] };
    return res.status(200).json({ message: 'Registered!' });
  }
  res.status(405).json({ error: 'Method not allowed' });
}
