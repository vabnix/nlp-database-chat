export const ErrorMessage = ({ message }) => {
    return (
      <div className="mb-8 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600">
        {message}
      </div>
    );
  };