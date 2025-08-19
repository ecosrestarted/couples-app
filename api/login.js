export default function handler(req, res) {
  if (req.method === 'POST') {
    const { username, password } = req.body;
    if (!users[username] || users[username].password !== password)
      return res.status(400).json({ error: 'Invalid login' });
    return res.status(200).json({ message: 'Logged in!' });
  }
  res.status(405).json({ error: 'Method not allowed' });
}
