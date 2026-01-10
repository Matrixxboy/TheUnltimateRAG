import React, { useState, useEffect } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { Layout, Github, Menu, X, ArrowUpRight } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

const Header = () => {
  const [open, setOpen] = useState(false)
  const location = useLocation()

  // Close menu on route change
  useEffect(() => {
    setOpen(false)
  }, [location])

  // Lock body scroll when menu is open
  useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden"
    } else {
      document.body.style.overflow = "unset"
    }
    return () => {
      document.body.style.overflow = "unset"
    }
  }, [open])

  const items = [
    { name: "Home", path: "/" },
    { name: "Docs", path: "/docs" },
    { name: "About", path: "/about" },
    { name: "Contact", path: "/contact" },
  ]

  return (
    <header className="fixed top-0 left-0 right-0 z-50 bg-white/70 backdrop-blur-xl border-b border-slate-200 shadow-sm transition-all duration-300">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between relative z-50">
        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-3 group">
          {/* <div className="bg-slate-900 p-2 rounded-lg shadow-md group-hover:scale-105 transition-transform duration-200">
            <Layout className="w-6 h-6 text-white" />
          </div> */}
          <span className="text-2xl font-bold text-slate-900 tracking-tight">
            TUG
            <span className="text-purple-600">.</span>
          </span>
        </NavLink>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          {items.map((item) => (
            <NavLink
              key={item.name}
              to={item.path}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors hover:text-purple-600 ${
                  isActive ? "text-slate-900" : "text-slate-500"
                }`
              }
            >
              {item.name}
            </NavLink>
          ))}
        </nav>

        {/* Actions */}
        <div className="flex items-center gap-4 ">
          <a
            href="https://github.com/Matrixxboy/TheUnltimateRAG"
            target="_blank"
            rel="noopener noreferrer"
            className="hidden md:flex p-2 text-slate-500 hover:text-slate-900 hover:bg-slate-100 rounded-lg transition-all"
          >
            <Github className="w-5 h-5" />
          </a>
          <NavLink
            to="/demo"
            className="hidden md:flex bg-slate-900 hover:bg-slate-800 text-white px-5 py-2.5 rounded-xl text-sm font-medium shadow-md hover:shadow-lg transition-all active:scale-95"
          >
            Try Demo
          </NavLink>

          {/* Mobile Toggle Button - Unique Design */}
          <button
            onClick={() => setOpen(!open)}
            className="md:hidden relative z-70 flex items-center gap-2 px-4 py-2 rounded-full 
            bg-purple-200/30
            backdrop-blur-sm
            border border-purple-300/40
            shadow-lg shadow-purple-500/20 font-medium text-sm transition-colors"
          >
            <AnimatePresence mode="wait" initial={false}>
              {open ? (
                <motion.div
                  key="close"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                  className="flex items-center gap-2 "
                >
                  <span>Close</span>
                  <X size={16} />
                </motion.div>
              ) : (
                <motion.div
                  key="menu"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}
                  className="flex items-center gap-2"
                >
                  <span>Menu</span>
                  <Menu size={16} />
                </motion.div>
              )}
            </AnimatePresence>
          </button>
        </div>
      </div>

      {/* Mobile Navigation Overlay - Unique "Curtain" Effect */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: "-100%" }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: "-100%" }}
            transition={{ type: "spring", damping: 25, stiffness: 200 }}
            className="fixed inset-0 z-40 bg-white min-h-screen md:hidden pt-24 px-6 pb-6 flex flex-col justify-between"
          >
            <div className="flex flex-col gap-2">
              {items.map((item, idx) => (
                <motion.div
                  key={item.name}
                  initial={{ opacity: 0, x: -50 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.1 + idx * 0.1 }}
                  className=""
                >
                  <NavLink
                    to={item.path}
                    className={({ isActive }) =>
                      `flex items-center justify-between p-4 text-2xl font-bold border-b  border-slate-100 ${
                        isActive ? "text-slate-900" : "text-slate-400"
                      }`
                    }
                  >
                    {item.name}
                    <ArrowUpRight
                      className={`w-5 h-5 transition-transform ${
                        location.pathname === item.path
                          ? "rotate-45 text-purple-600"
                          : ""
                      }`}
                    />
                  </NavLink>
                </motion.div>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="space-y-4"
            >
              <div className="p-6 bg-slate-50 rounded-2xl border border-slate-100">
                <h4 className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-4">
                  Quick Links
                </h4>
                <div className="flex gap-4">
                  <a
                    href="https://github.com/Matrixxboy/TheUnltimateRAG"
                    target="_blank"
                    rel="noreferrer"
                    className="flex-1 flex items-center justify-center p-3 bg-white border border-slate-200 rounded-xl text-slate-700 shadow-sm hover:border-slate-300"
                  >
                    <Github size={20} />
                  </a>
                  <NavLink
                    to="/demo"
                    className="flex-[3] flex items-center justify-center p-3 bg-slate-900 text-white rounded-xl font-medium shadow-lg active:scale-95 transition-transform"
                  >
                    Try Demo
                  </NavLink>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  )
}

export default Header
