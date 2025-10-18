import { fetchHello, fetchUsers } from './api.js';

document.getElementById('hello-btn').addEventListener('click', async () => {
    const data = await fetchHello();
    document.getElementById('result').textContent = data.message;
});