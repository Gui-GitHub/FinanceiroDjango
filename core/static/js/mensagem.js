// Espera 3 segundos e começa a sumir suavemente as mensagens
setTimeout(function() {
const alerts = document.querySelectorAll('.alert');
alerts.forEach(alert => {
    alert.style.transition = 'opacity 0.8s ease';
    alert.style.opacity = '0';
    setTimeout(() => alert.remove(), 800); // remove após fade-out
});
}, 2000); // tempo que a mensagem fica visível (2 segundos)