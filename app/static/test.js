$( document ).ready(function() {  

    var tab_add = []
    var tab_del = []
   
    $("#add").click(function(){
        var tab = []
        $('#user input[type="checkbox"]:checked').each(function(){
            var getRow = $(this).parents('tr');
            tab.push(getRow[0]);
            $("#user").find("input[type=checkbox]:checked").prop('checked', false);
            var getID=$(this).parents('tr').find('td:eq(1)').html();
            tab_add.push(getID);
            if (include(tab_del,getID,tab_add)== true){
                tab_del.splice(tab_del.indexOf(getID),1);
                tab_add.splice(tab_add.indexOf(getID),1);
            }     


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
            var getID=$(this).parents('tr').find('td:eq(1)').html();
            tab_del.push(getID);
            if (include(tab_add,getID,tab_del)== false){
                console.log('salam ' + getID)
            }else{
                tab_add.splice(tab_add.indexOf(getID),1);
                tab_del.splice(tab_del.indexOf(getID),1);
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
        console.log(data);
        console.log(JSON.stringify(data))        

        $.ajax({
            url : $(location).attr('href'),
            type : 'post',
            data : JSON.stringify(data),
            contentType:"application/json; charset=utf-8",
            dataType:"json"
        });

       
    });


    console.log('coucou');
  
    function test(){
        console.log('test');
    };

    
    
    
});

function include (tab_a,id,tab_b){
    for(var i = 0; i<tab_a.length;i++){
        for(var j = 0; j<tab_b.length;j++){
            if (tab_a[i]==tab_b[j]){
                return true
            }
        }
    }
    console.log('je suis bien passer ici')
    return false
}



var deleteRaw = function (path){        
        var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
        if (c == true)
           window.location.href = path;  
    }


//  var user ={
    // id : getRow.find('td:eq(1)').html()}