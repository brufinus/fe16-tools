document.addEventListener('DOMContentLoaded', () => {
  const currentTheme = localStorage.getItem('theme') || 'light';
  if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
  }
});

function toggleTheme() {
  document.body.classList.toggle('dark-mode');
  const theme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
  localStorage.setItem('theme', theme);
}
