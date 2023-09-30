import { Route, Routes } from "react-router-dom";
import Header from "./components/Header";
import Hero from "./components/Hero";
import HeroPowerForm from "./components/HeroPowerForm";
import Power from "./components/Power";
import PowerEditForm from "./components/PowerEditForm";
import Home from "./components/Home";

function App() {
  return (
    <div>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/heroes/:id" element={<Hero />} />
          <Route path="/hero_powers/new" element={<HeroPowerForm />} />
          <Route path="/powers/:id" element={<Power />} />
          <Route path="/powers/:id/edit" element={<PowerEditForm />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
