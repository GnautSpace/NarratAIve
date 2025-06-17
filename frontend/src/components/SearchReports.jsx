import { useState } from "react";
import "../App.css";

const SearchReports = ({ onSelect }) => {
    const [q, setQ] = useState("");
    const [res, setRes] = useState([]);

    const search = async () => {
        if (!q.trim()) return;
        const response = await fetch("https://super-duper-winner-7vvjj4p6q756crqwr-8000.app.github.dev/vector_search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: q }),
        });

        const data = await response.json();
        console.log(data);
        setRes(data);
    }

    return (
        <div>
            <input type="text" value={q} onChange={(e) => setQ(e.target.value)} placeholder="Search reports..." />
            <button onClick={search}>Search</button>

            {res.length > 0 && (
                <ul className="search-results">
                    {res.map((r, index) => (
                        <li
                            key={index}
                            
                            onClick={() => onSelect(r)}
                        >
                           <strong>{r.filename}</strong><br/>
        <small>
          {r.narrative?.slice(0, 60)}...
        </small>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    )
}
export default SearchReports;