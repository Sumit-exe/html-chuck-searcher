import React, { useState } from "react";
import axios from "axios";
import SearchForm from "./SearchForm";
import Results from "./Results";
import './App.css';


function App() {
  const [results, setResults] = useState([]);

  const handleSearch = async (url, query) => {
    const res = await axios.post("http://localhost:8000/search", { url, query });
    setResults(res.data.results);
  };

  return (
    <div className="container">
      <h1>HTML Semantic Search</h1>
      <SearchForm onSearch={handleSearch} />
      <Results results={results} />
    </div>
  );
}

export default App;
