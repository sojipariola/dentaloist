export async function fetchHello() {
    const res = await fetch('http://localhost:5000/api/hello');
    return await res.json();
}

export async function fetchUsers() {
    const res = await fetch('http://localhost:5000/api/users');
    return await res.json();
}