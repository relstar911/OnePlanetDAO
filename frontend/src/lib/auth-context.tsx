"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import { api } from "./api";

interface AuthContextType {
  isLoggedIn: boolean;
  userId: string | null;
  login: (userId: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  isLoggedIn: false,
  userId: null,
  login: async () => {},
  logout: () => {},
});

function getStoredAuth() {
  if (typeof window === "undefined") return { token: null, user: null };
  return {
    token: localStorage.getItem("op_token"),
    user: localStorage.getItem("op_user"),
  };
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const stored = getStoredAuth();
  const [isLoggedIn, setIsLoggedIn] = useState(!!stored.token && !!stored.user);
  const [userId, setUserId] = useState<string | null>(stored.user);

  const login = async (uid: string, password: string) => {
    await api.login({ user_id: uid, password });
    localStorage.setItem("op_user", uid);
    setUserId(uid);
    setIsLoggedIn(true);
  };

  const logout = () => {
    api.logout();
    localStorage.removeItem("op_user");
    setUserId(null);
    setIsLoggedIn(false);
  };

  return (
    <AuthContext.Provider value={{ isLoggedIn, userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
