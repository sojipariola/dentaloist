import { useState } from 'react';

export default function useAuth() {
  const [user, setUser] = useState(null);

  const login = async (email: string, password: string) => {
    // call auth API
    setUser({ email });
  };

  const logout = () => setUser(null);

  return { user, login, logout };
}
