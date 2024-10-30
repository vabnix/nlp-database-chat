const API_URL = 'http://localhost:8000';

export const executeQuery = async (queryText) => {
  try {
    const response = await fetch(`${API_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text: queryText }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Query failed');
    }

    return await response.json();
  } catch (error) {
    throw new Error(error.message);
  }
}; 