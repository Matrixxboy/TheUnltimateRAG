import React from "react"
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import Header from "./components/Header"
import Footer from "./components/Footer"
import Home from "./pages/Home"
import RAGDemo from "./pages/RAGDemo"
import About from "./pages/About"
import Contact from "./pages/Contact"
import Docs from "./pages/Docs"
import { ServerStatusProvider } from "./context/ServerStatusProvider"
import MaintenanceScreen from "./components/MaintenanceScreen"

import SmoothScroll from "./components/SmoothScroll"

function App() {
  return (
    <ServerStatusProvider>
      <Router>
        <SmoothScroll>
          <div className="flex flex-col min-h-screen bg-white">
            <Header />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/demo" element={<RAGDemo />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/docs" element={<Docs />} />
            </Routes>
            <Footer />
          </div>
        </SmoothScroll>
      </Router>
    </ServerStatusProvider>
  )
}

export default App
