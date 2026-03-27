setTimeout(() => {
  const toasts = document.querySelectorAll('.toast');
  toasts.forEach(t => {
    t.style.display = 'none';
  });
}, 5000); // 5 seconds
