import React, { useState, useEffect } from "react"
import api from "../services/api"
import ServerStatusContext from "./ServerStatus"

export const ServerStatusProvider = ({ children }) => {
  const [isServerDown, setIsServerDown] = useState(false)

  useEffect(() => {
    // Add a response interceptor
    const interceptor = api.interceptors.response.use(
      (response) => {
        // Any status code that lie within the range of 2xx cause this function to trigger
        // If we get a successful response, we can assume server is up
        if (isServerDown) setIsServerDown(false)
        return response
      },
      (error) => {
        // Any status codes that falls outside the range of 2xx cause this function to trigger
        if (
          error.message === "Network Error" ||
          (error.response && [502, 503, 504].includes(error.response.status))
        ) {
          setIsServerDown(true)
        }
        return Promise.reject(error)
      }
    )

    // Cleanup interceptor on unmount
    return () => {
      api.interceptors.response.eject(interceptor)
    }
  }, [isServerDown])

  const checkHealth = async () => {
    try {
      await api.get("/") // Assuming root or a health endpoint exists, otherwise just any lightweight call
      setIsServerDown(false)
    } catch {
      // Keep it down or set it down
      // interceptor will handle it
    }
  }

  return (
    <ServerStatusContext.Provider value={{ isServerDown, checkHealth }}>
      {children}
    </ServerStatusContext.Provider>
  )
}
