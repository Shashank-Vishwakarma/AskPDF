import {create} from "zustand"

export interface UserProps {
    name: string
    email: string
    token: string
}

interface AuthStore {
    user: UserProps | null
    setUser: (user: UserProps) => void
    removeUser: () => void
}

export const useAuthStore = create<AuthStore>((set) => ({
    user: localStorage.getItem("user") ? JSON.parse(localStorage.getItem("user")!) : null,
    setUser: (user: UserProps) => set({user}),
    removeUser: () => set({user: null})
}))
