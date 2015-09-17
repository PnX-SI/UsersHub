application.peuplerApplications = function(record) {
    if (record==null){id_application = 0;}
	else{
		var id_application = record.data.id_application;
		var nom_application = record.data.nom_application;
	;}
	
	// store du grid de gauche
    var firstGridStore = new Ext.data.JsonStore({
		url: 'get_utilisateurs.php?role=tous&panel=application&id_application='+id_application
		,method: 'GET'
		,fields: [
			{name: 'id_role'}
			,{name: 'role'}
			,{name: 'nom_unite'}
            ,{name: 'groupe'}
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
        ,title            : 'Rôles n\'ayant pas de droits dans l\''+nom_application
		,tbar 			 : [
			new Ext.form.ComboBox({
				id:'combo-filtre-unite-application',
				name: 'unite',
				store: application.storeUnites,
				fieldLabel: 'Unite',
				displayField:'nom_unite',
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
						var reg=new RegExp("^"+record.data.nom_unite+"$");
						firstGridStore.filter('nom_unite',reg);
		            }
		            ,scope: this
		        }
			})
            ,new Ext.Button({
				iconCls: 'group'
				,tooltip: 'Afficher uniquement les groupes'
				,handler: function() {
					var reg=new RegExp("^t$");
					firstGridStore.filter('groupe',reg);
				}
			})
            ,new Ext.Button({
				iconCls: 'user'
				,tooltip: 'Afficher uniquement les utilisateurs'
				,handler: function() {
					// firstGridStore.clearFilter();
                    var reg=new RegExp("^f$");
					firstGridStore.filter('groupe',reg);
				}
			})
            ,new Ext.Button({
				iconCls: 'raz'
				,tooltip: 'Afficher tous les rôles'
				,handler: function() {
					firstGridStore.clearFilter();
					Ext.getCmp('combo-filtre-unite-application').reset();
				}
			})
		]
    });
	
	// store du grid de droite	
   var secondGridStore = new Ext.data.JsonStore({
		url: 'get_role_droit_application.php?id_application='+id_application
		,method: 'GET'
		,fields: [
			{name: 'id_role', mapping : 'id_role'}
			,{name: 'role', mapping : 'role'}
			,{name: 'nom_unite'}
			,{name: 'id_droit'}
		]
		//,sortInfo: {field: 'role',direction: 'ASC'}
		,autoLoad:true
		,synchronous: true
	});
	var rowActionsSupprimeRole = new Ext.ux.grid.RowActions({
		actions: [{
			tooltip: 'Supprimer ce role de l\'application',
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
			,{header: 'Droits',dataIndex: 'id_droit',width: 100
                ,editor: new Ext.form.ComboBox({
					name: 'id_droit',
					store: application.storeDroits,
					displayField:'nom_droit',
					valueField: 'id_droit',
					allowBlank:false,
					blankText: 'Vous devez choisir un droit.',
                    typeAhead: true,
                    mode: 'local',
					triggerAction: 'all',
					selectOnFocus:true,
					forceSelection:true,
                    //lazyRender: true,
                    listClass: 'x-combo-list-small'
                })
            }
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
        title: 'Affectation des droits pour l\''+nom_application
    });
	//le submit qui n'envoi aucun paramètre car pas de champ dans le formulaire donc on passe tout en GET dans l'URL
	var saveDroits = function(){
		var nb = secondGridStore.getCount();
		var ar = new  Array();//un tableau de tableau
		var compt = 0;
		for(i=0;i<nb;i++){
			var r = secondGridStore.getAt(i);
			var idDroit= r.data.id_droit;
			if (idDroit==null){compt++}
			var idUtilisateur= r.data.id_role;
			var v = [idUtilisateur,idDroit];//un tableau par ligne
			ar.push(v);//le tableau de ligne rempli le tableau de tableau
		}
		var tab = ar.join("-"); //Les valeurs à envoyer php
		
		var url = 'update_cor_role_droit_application.php?id_application='+id_application+'&valeurs='+tab+'&nom_application='+nom_application
		if (compt==0){
			Ext.getCmp('tabpanel-'+id_application).getForm().submit({
				url: url
				,method: 'GET'
				,success: function(result, action) {
					var result = Ext.util.JSON.decode(action.response.responseText);
					Ext.ux.Toast.msg('OK !', result.msg);
				}
			});
		}
		else{Ext.Msg.alert('Attention !', 'Vous n\'avez pas attribué de droit à tous les utilisateurs');}
	};

	return{
		//Simple 'border layout' panel to house both grids
		id: 'tabpanel-'+id_application,
		xtype:'form',
		title:nom_application,
		width: 650,
		height: 300,
		layout: 'hbox',
		defaults: { flex : 1 }, //auto stretch
		layoutConfig: { align : 'stretch' },
		closable:true,
		items: [
			firstGrid,
			secondGrid
		],
		bbar: [
			'->', // Fill
			{
				text    : 'Enregistrer',
				handler : function() {
					saveDroits();
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
								//secondGrid.store.sort('id_role', 'ASC');
								return true
						}
				});
			}
		}
	}
};
