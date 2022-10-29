window.onload = () => {
    document.getElementById("imc_valor").onfocus = function() {
        const peso = document.getElementById("peso").value;
        const altura = document.getElementById("altura").value;
        let res = "";

        let imc = (peso / (altura ** 2)).toFixed(2);

        if (imc < 18.5){
            res = "Magreza";
        } else if ((imc >= 18.5) && (imc <= 24.9)) {
            res = "Normal";
        } else if ((imc >= 25.0) && (imc <= 29.9)) {
            res = "Sobrepeso";
        } else if ((imc >= 30.0) && (imc <= 34.9)) {
            res = "Obesidade";
        } else {
            res = "Obesidade Mórbida";
        }    
        document.getElementById("imc_classificacao").value = res;    
        document.getElementById("imc_valor").value = imc;
        
    }  
}