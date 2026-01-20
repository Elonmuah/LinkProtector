export const API_BASE = 'http://192.168.2.101:5000';

// Example function to fetch user URLs
export async function getUserUrls() {
  const res = await fetch(`${API_BASE}/api/getUserUrls`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ /* payload */ })
  });

  if (!res.ok) {
    throw new Error('Failed to fetch user URLs');
  }
  return res.json();
}