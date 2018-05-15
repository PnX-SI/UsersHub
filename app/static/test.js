$( document ).ready(function() {  
   
    $("#transfert").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow.find('td:eq(1)').html());
        
        });
        console.log(tab)
    });    
    console.log('coucou')
  
    $("table tbody tr td #delete").click(function(event){
        console.log(event.target)
        confirm("Etes vous sur de vouloir supprimer cette élement ? ");
    });

});