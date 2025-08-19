export default function handler(req, res) {
  if (req.method === 'POST') {
    const { username, entry } = req.body;
    if (!users[username]) return res.status(400).json({ error: 'User not found' });
    users[username].journal.push(entry);
    return res.status(200).json({ journal: users[username].journal });
  } else if (req.method === 'GET') {
    const username = req.query.username;
    if (!users[username]) return res.status(400).json({ error: 'User not found' });
    return res.status(200).json({ journal: users[username].journal });
  }
  res.status(405).json({ error: 'Method not allowed' });
}
