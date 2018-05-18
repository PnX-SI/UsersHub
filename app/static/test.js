$( document ).ready(function() {  
   
    $("#add").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow[0]);
            $("#user").find("input[type=checkbox]:checked").prop('checked', false);
            
        });
        var table = $('#adding_table')
        addTab(tab,table)
 
    });
    
    $("#delete").click(function(){
        var tab = []
        $('#adding_table input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow[0]);
            $("#adding_table").find("input[type=checkbox]:checked").prop('checked', false);
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

    $("#update").click(function(){
        var tab_add = []
        $("#adding_table tbody tr").each(function(){
            var user ={
                id : $(this).find('td:eq(1)').html()
            }
            tab_add.push(user)
        });
       

        $.ajax({
            url : $(location).attr('href'),
            type : 'post',
            data : JSON.stringify(tab_add),
            contentType:"application/json; charset=utf-8",
            dataType:"json"
        });

       
    });


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