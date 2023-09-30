import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

function Home() {
  const [heroes, setHeroes] = useState([]);

  useEffect(() => {
    fetch("/heroes")
      .then((r) => {
        if (!r.ok) {
          throw new Error("Network response was not ok");
        }
        return r.json();
      })
      .then((data) => {
        setHeroes(data);
      })
      .catch((error) => {
        console.error("Fetch error:", error);
      });
  }, []);

  return (
    <section>
      <h2>All Heroes</h2>
      <ul>
        {heroes.map((hero) => (
          <li key={hero.id}>
            <Link to={`/heroes/${hero.id}`}>{hero.super_name}</Link>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default Home;
