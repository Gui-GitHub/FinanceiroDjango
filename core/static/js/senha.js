function setupTogglePassword(inputId, iconId) {
  const input = document.getElementById(inputId);
  const icon = document.getElementById(iconId);

  if (!icon || !input) return;

  icon.addEventListener('click', function() {
    const isPassword = input.type === "password";
    input.type = isPassword ? "text" : "password";

    icon.classList.toggle("bi-eye");
    icon.classList.toggle("bi-eye-slash");
  });
}

document.addEventListener('DOMContentLoaded', function() {
  setupTogglePassword("current_password", "toggleCurrentPassword");
  setupTogglePassword("new_password", "toggleNewPassword");
  setupTogglePassword("confirm_password", "toggleConfirmPassword");
});