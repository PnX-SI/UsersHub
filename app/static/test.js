$( document ).ready(function() {  
   
    $("#transfert").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow.find('td:eq(1)').html());
        
        });
        console.log(tab)
    });    
    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    
    
});


var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cette élement ? ");
        if (c == true)
           window.location.href = path;  
    }