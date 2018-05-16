$( document ).ready(function() {  
   
    $("#transfert").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            var user ={
                id : getRow.find('td:eq(1)').html(),
                name : getRow.find('td:eq(2)').html()
            }
            tab.push(user);
            addTab(tab)
        });
        console.log(tab)
    });    




    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    
    
});


function addTab(tab){
    for(var i = 0; i<tab.length;i++){
        var sHtml = "<tr>"+
                "   <td class='m1'>"+tab[i].id+"</td>"+
                "   <td class='m2'>"+tab[i].name+"</td>"+
                "</tr>";
    }    
    
    $("#test").append(sHtml);
}


var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
        if (c == true)
           window.location.href = path;  
    }