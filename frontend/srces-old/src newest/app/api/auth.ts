// frontend/app/api/auth.ts
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:5000/api";

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true, // allow cookies if needed
});

export const register = (data: {
  email: string;
  password: string;
  first_name: string;
  last_name: string;
}) => api.post("/auth/register", data);

export const login = (data: { email: string; password: string }) =>
  api.post("/auth/login", data);

export const refresh = () => api.post("/auth/refresh");

export const me = () => api.get("/auth/me");

export const googleLogin = () =>
  (window.location.href = `${API_URL}/auth/google/login`);
