import { useState } from "react";

function Results({ results }) {
  if (!results || results.length === 0) {
    return <p>No results found.</p>;
  }

  return (
    <div className="results-list">
      {results.map((r, index) => (
        <ResultCard key={index} result={r} />
      ))}
    </div>
  );
}


function ResultCard({ result }) {
  const [showHtml, setShowHtml] = useState(false);

  // Strip HTML tags but keep basic rich formatting like <p>, <strong>, <em>, <a>
  const createRichText = (html) => {
    const temp = document.createElement("div");
    temp.innerHTML = html;
    return temp;
  };

  return (
    <div className="card">
      <h2 className="card-heading">{result.summary || "Result"}</h2>

      <button
        className="toggle-btn"
        onClick={() => setShowHtml(!showHtml)}
      >
        {showHtml ? "Hide Content" : "View Content"}
      </button>

      <div
        className={`html-content ${showHtml ? "open" : ""}`}
      >
        <div className="rich-text">
          {createRichText(result.html).childNodes.length > 0 &&
            Array.from(createRichText(result.html).childNodes).map((node, i) => (
              <span key={i}>
                {node.nodeType === 3
                  ? node.textContent
                  : node.outerHTML}
              </span>
            ))}
        </div>
      </div>
    </div>
  );
}

export default Results;
