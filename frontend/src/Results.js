function Results({ results }) {
  if (!results || results.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <div className="results-list">
      {results.map((r, index) => (
        <div key={index} className="card">
          {r.text ? (
            <>
              {r.score !== undefined && (
                <p><strong>Score:</strong> {r.score.toFixed(4)}</p>
              )}
              <p>{r.text}</p>
            </>
          ) : ( 
            <p>{r}</p>
          )}
        </div>
      ))}
    </div>
  );
}

export default Results;
