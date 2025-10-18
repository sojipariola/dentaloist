// js/components/Card.js
export function renderCard({ title, body, footer }) {
  const template = document.getElementById('card-template').content;
  const clone = document.importNode(template, true);
  clone.querySelector('.card-header').textContent = title;
  clone.querySelector('.card-body').innerHTML = body;
  clone.querySelector('.card-footer').textContent = footer;
  return clone;
}