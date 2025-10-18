"use client";

import { useEffect, useState } from "react";
import { me } from "../api/auth";
import { clearTokens } from "../lib/auth";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const [user, setUser] = useState<any>(null);
  const router = useRouter();

  useEffect(() => {
    me()
      .then((res) => setUser(res.data.user))
      .catch(() => router.push("/login"));
  }, [router]);

  const handleLogout = () => {
    clearTokens();
    router.push("/login");
  };

  if (!user) return <p>Loading...</p>;

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">Welcome, {user.first_name}</h1>
      <button
        onClick={handleLogout}
        className="mt-4 bg-gray-800 text-white px-4 py-2 rounded-lg"
      >
        Logout
      </button>
    </div>
  );
}
