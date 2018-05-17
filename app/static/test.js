$( document ).ready(function() {  
   
    $("#transfert").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
           
            tab.push(getRow[0]);
            
            
        });
        addTab(tab)
 
    });    




    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    function addTab(tab){
    var table = $('#test')
    console.log(table)
    console.log(tab)
    for(var i = 0; i<tab.length;i++){
        console.log(tab[i])
        
        
        table.append(tab[i]);
    }    
    
    }
    
});





var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
        if (c == true)
           window.location.href = path;  
    }


//  var user ={
    // id : getRow.find('td:eq(1)').html()}