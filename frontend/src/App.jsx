import { useEffect, useState } from 'react';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);
  const apiBaseUrl = import.meta.env.VITE_API_URL;

  useEffect(() => {
    fetch(`${apiBaseUrl}/items`)
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch");
        return res.json();
      })
      .then((data) => setItems(data))
      .catch((err) => console.error(err));
  }, []);

  return (
    <>

      <div>
        <h2>🔥 Items from FastAPI:</h2>
        <ul>
          {items.length === 0 ? (
            <li>No items found</li>
          ) : (
            items.map((item) => (
              <li key={item.id}>
                {item.text} - {item.is_done ? "✅" : "❌"}
              </li>
            ))
          )}
        </ul>
      </div>
    </>
  );
}

export default App;
