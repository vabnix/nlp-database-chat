import { Search } from 'lucide-react';

export const QueryForm = ({ query, setQuery, onSubmit, loading }) => {
  return (
    <form onSubmit={onSubmit} className="mb-8">
      <div className="flex gap-4">
        <div className="flex-1 relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., 'Show me employees with salary more than 80000'"
            className="w-full p-4 pr-12 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          />
          <Search className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
        </div>
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="px-6 py-4 bg-blue-600 text-white rounded-lg shadow-sm hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors"
        >
          {loading ? 'Querying...' : 'Search'}
        </button>
      </div>
    </form>
  );
};