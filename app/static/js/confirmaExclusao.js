$(document).ready(function() {

    $('*[data-confirm="true"]').on('click',function(){
        return confirm('Tem certeza que deseja excluir?');
    }); 

});