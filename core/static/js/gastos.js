document.addEventListener('DOMContentLoaded', function() {
    // Máscara para campo de dinheiro
    var valorInput = document.getElementById('valor');
    if (valorInput) {
        valorInput.addEventListener('input', function(e) {
            var value = e.target.value.replace(/\D/g, ''); // Remove tudo que não é número
            value = (value / 100).toFixed(2) + ''; // Adiciona duas casas decimais
            value = value.replace('.', ','); // Troca ponto por vírgula

            // Adiciona separador de milhar
            var partes = value.split(',');
            partes[0] = partes[0].replace(/\B(?=(\d{3})+(?!\d))/g, '.');
            e.target.value = partes.join(',');
        });
    }
});