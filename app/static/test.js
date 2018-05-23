$( document ).ready(function() {  

    var tab_add = []
    var tab_del = []
   
    $("#add").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var Row = $(this).parents('tr');
            tab.push(Row[0]);
            $("#user").find("input[type=checkbox]:checked").prop('checked', false);
            var ID=$(this).parents('tr').find('td:eq(1)').html();
            tab_add.push(ID);
            if (isInTabb(tab_del,ID) == true){
                tab_del.splice(tab_del.indexOf(ID),1);
                tab_add.splice(tab_add.indexOf(ID),1);
            }
            

            console.log(tab_add)

        });
        
        var table = $('#adding_table')
        addTab(tab,table)
 
    });
    
    $("#delete").click(function(){
        var tab = []
        $('#adding_table input[type="checkbox"]:checked').each(function(){
            var Row = $(this).parents('tr');
            tab.push(Row[0]);
            $("#adding_table").find("input[type=checkbox]:checked").prop('checked', false);
            var ID=$(this).parents('tr').find('td:eq(1)').html();
            tab_del.push(ID)
            console.log(isInTabb(tab_add,ID))
            if (isInTabb(tab_add,ID) == true){
                tab_add.splice(tab_add.indexOf(ID),1);
                tab_del.splice(tab_del.indexOf(ID),1);
            }
            
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
        console.log("tableau d ajout : "+ tab_add);
        console.log("tablea de suppression : "+ tab_del );
        var data ={}
        data["tab_add"] = tab_add;
        data["tab_del"]= tab_del;

        $.ajax({
            url : $(location).attr('href'),
            type : 'post',
            data : JSON.stringify(data),
            contentType:"application/json; charset=utf-8",
            dataType:"json"
        });

       tab_add = []
       tab_del = []
    });


    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    
});

function isInTabb(tab,id){
    var bool = false
    tab.forEach(element => {
        if (element == id){
            bool = true
        }
    });
    return bool
}



// tab.forEach(element => {
    
// });

// tab_del = tab_del.filter(function(el) {
//     return el =! id
// });

// new = array.map(el => {
//     el +1
// })





var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
        if (c == true)
           window.location.href = path;  
    }


//  var user ={
    // id : getRow.find('td:eq(1)').html()}