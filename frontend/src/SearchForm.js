import React, { useState } from "react";

function SearchForm({ onSearch }) {
  const [url, setUrl] = useState("");
  const [query, setQuery] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(url, query);
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Website URL</label>
      <input value={url} onChange={(e) => setUrl(e.target.value)} />

      <label>Search Query</label>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />

      <button type="submit">Search</button>
    </form>
  );
}

export default SearchForm;
