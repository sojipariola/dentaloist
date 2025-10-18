export function formatDate(dateString, format = 'MM/DD/YYYY HH:mm') {
    if (!dateString) return '';
    const date = new Date(dateString);
    
    const pad = (num) => String(num).padStart(2, '0');
    
    const month = pad(date.getMonth() + 1);
    const day = pad(date.getDate());
    const year = date.getFullYear();
    const hours = pad(date.getHours());
    const minutes = pad(date.getMinutes());
    const seconds = pad(date.getSeconds());
    
    let formatted = format
        .replace('MM', month)
        .replace('DD', day)
        .replace('YYYY', year)
        .replace('HH', hours)
        .replace('mm', minutes)
        .replace('ss', seconds);
    
    return formatted;
}

export function formatTime(dateString, format = '12h') {
    if (!dateString) return '';
    const date = new Date(dateString);
    
    let hours = date.getHours();
    let minutes = String(date.getMinutes()).padStart(2, '0');
    let ampm = '';
    
    if (format === '12h') {
        ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12; // 0 should be 12
    }
    
    return `${hours}:${minutes}${ampm ? ' ' + ampm : ''}`;
}

export function isToday(dateString) {
    const today = new Date();
    const date = new Date(dateString);
    return date.toDateString() === today.toDateString();
}

export function isPast(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    return date < now;
}

export function isFuture(dateString) {
    const now = new Date();
    const date = new Date(dateString);
    return date > now;
}

export function addDays(dateString, days) {
    const date = new Date(dateString);
    date.setDate(date.getDate() + days);
    return date.toISOString();
}

export function getDayName(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { weekday: 'long' });
}