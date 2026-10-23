import { BrowserRouter, Routes, Route, Link } from "react-router";
import Index from "./pages/Index";

function App() {
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Index />} />
    </Routes>
  </BrowserRouter>
}

export default App