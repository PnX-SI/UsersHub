
application.peuplerGroupes = function(record) {
	
	    if (record==null){id_groupe = 0;}
	else{
		var id_groupe = record.data.id_groupe;
		var nom_groupe = record.data.nom_groupe;
	;}
	
	// store du grid de gauche
    var firstGridStore = new Ext.data.JsonStore({
		url: 'get_utilisateurs.php?role=tous&panel=groupe&id_groupe='+id_groupe
		,method: 'GET'
		,fields: [
			{name: 'id_role'}
			,{name: 'role'}
			,{name: 'nom_unite'}
		]
		,sortInfo: {field: 'nom_unite',direction: 'ASC'}
		,autoLoad:true
		//,synchronous: true
	});
	
	// Column Model shortcut array
	var cols1 = [
		{id : 'id_role', header: "Id", width: 50, sortable: true, dataIndex: 'id_role'}
		,{header: "Role", width: 150, sortable: true, dataIndex: 'role'}
		,{header: "Unité", width: 150, sortable: true, dataIndex: 'nom_unite'}
	];
	// declare the source Grid
    var firstGrid = new Ext.grid.GridPanel({
        id                :'grid-user-groupes-gauche'
		,ddGroup          : 'secondGridDDGroup'
        ,store            : firstGridStore
        ,columns          : cols1
		,enableDragDrop   : true
        ,stripeRows       : true
        ,autoExpandColumn : 'id_role'
        ,title            : 'Liste des rôles disponibles'
		,tbar 			 : [
			new Ext.form.ComboBox({
				id:'combo-filtre-unite-groupe',
				name: 'unite',
				store: storeUnites,
				fieldLabel: 'Unite',
				displayField:'intitule',
				valueField: 'id_unite',
				typeAhead: true,
				mode: 'local',
				triggerAction: 'all',
				selectOnFocus:true,
				forceSelection:true,
				editable:false,
				width:200,
				resizable:true,
				listeners:{
		            select: function(combo,record,index) {
						var reg=new RegExp("^"+record.data.intitule+"$");
						firstGridStore.filter('nom_unite',reg);
		            }
		            ,scope: this
		        }
			})
			,new Ext.Button({
				iconCls: 'raz'
				,tooltip: 'Afficher tous les rôles'
				,handler: function() {
					firstGridStore.clearFilter();
					Ext.getCmp('combo-filtre-unite-groupe').reset();
				}
			})
		]
    });
	
	// store du grid de droite	
   var secondGridStore = new Ext.data.JsonStore({
		url: 'get_utilisateurs.php?mon_groupe='+id_groupe
		,method: 'GET'
		,fields: [
			{name: 'id_role', mapping : 'id_role'}
			,{name: 'role', mapping : 'role'}
			,{name: 'nom_unite', mapping : 'nom_unite'}
		]
		//,sortInfo: {field: 'nom_unite',direction: 'ASC'}
		,autoLoad:true
		,synchronous: true
	});
	var rowActionsSupprimeRole = new Ext.ux.grid.RowActions({
		actions: [{
			tooltip: 'Supprimer ce role du groupe',
			iconCls: 'action-remove'
		}]
		,listeners: {
			action: function (grid, rec, action) {
				switch (action) {
				case 'action-remove':
					grid.getStore().remove(rec); 
					break;
				default:
					break;
				}
			}
		}
		,fixed: true
		,autoWidth: false
		,width: 25
	});
	var cm = new Ext.grid.ColumnModel({
        // specify any defaults for each column
        defaults: {
            sortable: true // columns are not sortable by default           
        },
        columns: [
            {id : 'id_role', header: "Id", width: 50, dataIndex: 'id_role'}
			,{header: "Role", width: 150, dataIndex: 'role'}
			,{header: "Unité", width: 150, dataIndex: 'nom_unite'}
			//,rowActionsSupprimeRole
        ]
    });
    // create the destination Grid
    var secondGrid = new Ext.grid.EditorGridPanel({
		ddGroup: 'firstGridDDGroup',
        store: secondGridStore,
        cm: cm,
		enableDragDrop: true,
        stripeRows: true,
		sm: new Ext.grid.RowSelectionModel({singleSelect:true}),
        autoExpandColumn: 'id_role',
		clicksToEdit: 1,
		//plugins:[rowActionsSupprimeRole],
        title: 'Rôles du groupe "'+nom_groupe+'"'
    });
	//le submit qui n'envoi aucun paramètre car pas de champ dans le formulaire donc on passe tout en GET dans l'URL
	var saveGroupes = function(){
		var nb = secondGridStore.getCount();
		var ar = new  Array();//un tableau
		for(i=0;i<nb;i++){
			var r = secondGridStore.getAt(i);
			ar.push(r.data.id_role);//remplir le tableau
		}
		var tab = ar.join(","); //Les valeurs à envoyer php
		var url = 'update_cor_roles.php?id_groupe='+id_groupe+'&roles='+tab+'&nom_groupe='+nom_groupe
		Ext.getCmp('tabpanel-'+id_groupe).getForm().submit({
			url: url
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
			}
		});
	};

	return{
		//Simple 'border layout' panel to house both grids
		id: 'tabpanel-'+id_groupe,
		xtype:'form',
		title:nom_groupe,
		width: 650,
		height: 300,
		layout: 'hbox',
		defaults: { flex : 1 }, //auto stretch
		layoutConfig: { align : 'stretch' },
		closable:true,
		items: [
			firstGrid
			,secondGrid
		],
		bbar: [
			'->', // Fill
			{
				text    : 'Enregistrer',
				handler : function() {
					saveGroupes();
				}
			},{
				text    : 'Annuler',
				handler : function() {
					firstGridStore.reload();
					secondGridStore.reload();
				}
			}
		]
		,listeners:{
			afterlayout:function (p) {
				/****
					 * Setup Drop Targets
					 ***/
				// This will make sure we only drop to the  view scroller element
				var firstGridDropTargetEl =  firstGrid.getView().scroller.dom;
				var firstGridDropTarget = new Ext.dd.DropTarget(firstGridDropTargetEl, {
						ddGroup    : 'firstGridDDGroup',
						notifyDrop : function(ddSource, e, data){
								var records =  ddSource.dragData.selections;
								Ext.each(records, ddSource.grid.store.remove, ddSource.grid.store);
								firstGrid.store.add(records);
								firstGrid.store.sort('nom_unite', 'ASC');
								return true
						}
				});

				// This will make sure we only drop to the view scroller element
				var secondGridDropTargetEl = secondGrid.getView().scroller.dom;
				var secondGridDropTarget = new Ext.dd.DropTarget(secondGridDropTargetEl, {
						ddGroup    : 'secondGridDDGroup',
						notifyDrop : function(ddSource, e, data){
								var records =  ddSource.dragData.selections;
								Ext.each(records, ddSource.grid.store.remove, ddSource.grid.store);
								secondGrid.store.add(records);
								//secondGrid.store.sort('role', 'ASC');
								return true
						}
				});
			}
		}
	}
};