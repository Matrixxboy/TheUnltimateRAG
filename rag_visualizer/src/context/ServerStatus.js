import { createContext, useContext } from "react"

const ServerStatusContext = createContext()

export const useServerStatus = () => useContext(ServerStatusContext)

export default ServerStatusContext
