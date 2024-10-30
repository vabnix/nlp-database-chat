import { useState } from 'react';
import { QueryForm } from './components/QueryForm';
import { SqlDisplay } from './components/SqlDisplay';
import { ResultsDisplay } from './components/ResultsDisplay';
import { ErrorMessage } from './components/ErrorMessage';
import { executeQuery } from './services/api';

function App() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const data = await executeQuery(query);
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold mb-2">Natural Language Database Query</h1>
          <p className="text-gray-600">
            Ask questions about employees and departments in plain English
          </p>
        </div>

        <QueryForm
          query={query}
          setQuery={setQuery}
          onSubmit={handleSubmit}
          loading={loading}
        />

        {error && <ErrorMessage message={error} />}

        {results && (
          <div className="space-y-6">
            <SqlDisplay
              sql={results.sql_query}
              executionTime={results.execution_time}
            />
            <ResultsDisplay results={results.results} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;