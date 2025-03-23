document.addEventListener('DOMContentLoaded', function() {
    // Elementos do formulário
    const form = document.getElementById('formulario_producao');
    const fileInput = document.getElementById('fileInput');
    const fileList = document.getElementById('fileList');
    const papelAdesivo = document.getElementById('papelAdesivo');
    const tipoAdesivoGroup = document.getElementById('tipoAdesivoGroup');
    const dataEntrega = document.getElementById('dataEntrega');
    
    // Exibir nomes dos arquivos selecionados
    fileInput.addEventListener('change', function() {
        fileList.innerHTML = '';
        
        if (this.files.length > 0) {
            for (let i = 0; i < this.files.length; i++) {
                const li = document.createElement('li');
                li.textContent = this.files[i].name;
                fileList.appendChild(li);
            }
        }
    });
    
    // Mostrar/esconder opções de adesivo
    papelAdesivo.addEventListener('change', function() {
        if (this.value === 'sim') {
            tipoAdesivoGroup.style.display = 'block';
        } else {
            tipoAdesivoGroup.style.display = 'none';
        }
    });
    
    // Validação da data (não permitir datas passadas)
    dataEntrega.addEventListener('input', function() {
        const hoje = new Date();
        hoje.setHours(0, 0, 0, 0);
        
        const dataSelecionada = new Date(this.value);
        
        if (dataSelecionada < hoje) {
            this.setCustomValidity('A data de entrega não pode ser no passado');
        } else {
            this.setCustomValidity('');
        }
    });
    
    // Definir data mínima como hoje
    const dataHoje = new Date().toISOString().split('T')[0];
    dataEntrega.setAttribute('min', dataHoje);
    
    // Manipular envio do formulário
    form.addEventListener('submit', function(e) {
        e.preventDefault(); // Prevenir o envio padrão do formulário
        
        // Verificar se o formulário é válido
        if (form.checkValidity()) {
            // Mostrar modal de processamento
            showProcessingStatus();
            
            // Simular envio do formulário
            setTimeout(function() {
                const isSuccess = Math.random() > 0.2;
                
                if (isSuccess) {
                    showSuccessStatus();
                } else {
                    showErrorStatus();
                }
            }, 2000);
        } else {
            form.reportValidity();
        }
    });

    
});


