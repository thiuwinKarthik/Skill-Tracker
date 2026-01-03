import './Error.css'

const Error = ({ message = 'Something went wrong', onRetry }) => {
  return (
    <div className="error-container">
      <div className="error-icon">⚠️</div>
      <h3 className="error-title">Error</h3>
      <p className="error-message">{message}</p>
      {onRetry && (
        <button className="error-retry" onClick={onRetry}>
          Try Again
        </button>
      )}
    </div>
  )
}

export default Error



