$( document ).ready(function() {  
   
    $("#add").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow[0]);
            $("#user").find("input[type=checkbox]").attr('checked', false);
            
        });
        var table = $('#adding_table')
        addTab(tab,table)
 
    });
    
    $("#delete").click(function(){
        var tab = []
        $('#adding_table input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            $("#adding_table").find("input[type=checkbox]").attr('checked', false);
            tab.push(getRow[0]);
            
            
        });
        var table = $('#user')
        addTab(tab,table)
 
    });

    function addTab(tab,table){
        // table.find("input[type=checkbox]").attr('checked', false);
        for(var i = 0; i<tab.length;i++){
            
            table.append(tab[i]);
        }    
        
    }



    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    
    
});





var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
        if (c == true)
           window.location.href = path;  
    }


//  var user ={
    // id : getRow.find('td:eq(1)').html()}