document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('password');
  const icon = document.getElementById('togglePassword');

  if (!icon || !input) {
    console.warn("Campo de senha ou ícone não encontrado.");
    return;
  }

  icon.addEventListener('click', function() {
    const isPassword = input.type === "password";

    input.type = isPassword ? "text" : "password";

    // alterna os ícones
    icon.classList.toggle("bi-eye");
    icon.classList.toggle("bi-eye-slash");
  });
});