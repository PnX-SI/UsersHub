	 
application.layout = function() {
	return {
	init: function() {
// _____________________Creation du tableau des droits_________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeDroits = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer ce droit',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer ce droit ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeDroit(record);
										grid.getStore().remove(record);
										//grid.getStore().reload();                                      
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeDroits = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
    gridPanelDroits = new Ext.grid.GridPanel({
		id:"griddroits"
        ,title: "Droits"
        ,store: application.storeDroits
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_droit"
				,sortable: true
			},{
				header: "Droit"
				,width: 240
				,dataIndex: "nom_droit"
				,sortable: true
			}
			,rowActionsSupprimeDroits
		] 
		,tbar:[
			{
				text: 'Ajouter un droit'
				,tooltip: 'Ajouter une nouveau niveau de droit'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formdroits').getForm().reset();
					Ext.getCmp('champ_action-droit').setValue("insert");
					Ext.getCmp('champ_id_initial-droit').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
				}
			},{
				id: 'btInfoDroits'
				,tooltip:'des informations concernant cet onglet droit'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les différents type de droits disponibles pour être ensuite attribués aux utilisateurs ou aux groupes.'+
							'<br />Dans la base de données, les droits sont stockés dans la table bib_droits. '+
							'Une table cor_role_droit_application permet d\'attribuer des droits aux différents rôles selon les applications (voir l\'onglet "Applications").'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
        ,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormDroits(record);
					Ext.getCmp('champ_action-droit').setValue("update");
					Ext.getCmp('champ_id_initial-droit').setValue(record.data.id_droit);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
				}
			}
		})
		,plugins: rowActionsSupprimeDroits
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelDroits.getSelectionModel().selectFirstRow();
			}
		}
    });
	
// _____________________Creation du tableau des menus_________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeMenus = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer ce menu',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer ce menu ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeMenu(record);
										grid.getStore().remove(record);
										//grid.getStore().reload();                                      
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeMenus = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
    gridPanelMenus = new Ext.grid.GridPanel({
		id:"gridmenus"
        ,title: "Listes"
        ,store: application.storeMenus
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_menu"
				,sortable: true
			},{
				header: "Menu"
				,width: 240
				,dataIndex: "nom_menu"
				,sortable: true
			}
			,rowActionsSupprimeMenus
		] 
		,tbar:[
			{
				text: 'Ajouter une liste'
				,tooltip: 'Ajouter une nouvelle liste'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formmenus').getForm().reset();
					Ext.getCmp('champ_action-menu').setValue("insert");
					Ext.getCmp('champ_id_initial-menu').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
					tabPanelMenus.setActiveTab(0);
				}
			},{
				id: 'btInfoMenus'
				,tooltip:'des informations concernant cet onglet liste'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les listes déroulantes des applications.'+
							'<br />Dans la base de données, les listes sont stockés dans la table t_menus. '+
							'Une table cor_role_menu permet de placer des rôles dans ces listes déroulantes.'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
        ,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormMenus(record);
					loadTabMenu(record);
					Ext.getCmp('champ_action-menu').setValue("update");
					Ext.getCmp('champ_id_initial-menu').setValue(record.data.id_menu);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
				}
			}
		})
		,plugins: rowActionsSupprimeMenus
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelMenus.getSelectionModel().selectFirstRow();
			}
		}
    });
	
// ___________________________________Creation du tableau des groupes___________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeGroupes = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer ce role-groupe',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer ce role de niveau groupe ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeGroupe(record);
										grid.getStore().remove(record);                                  
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeGroupes = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}

    gridPanelGroupes = new Ext.grid.GridPanel({
		id:"gridgroupes"
        ,title: "Groupes"
        ,store: application.storeGroupes
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_groupe"
				,sortable: true
			},{
				header: "Groupe"
				,width: 215
				,dataIndex: "nom_groupe"
				,sortable: true
			}
			//,rowActionsPeuplerGroupes
			,rowActionsSupprimeGroupes
		]
		,tbar:[
			{
				text: 'Ajouter un groupe'
				,tooltip: 'Ajouter un nouveau role de niveau groupe'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formgroupes').getForm().reset();
					Ext.getCmp('champ_action-groupe').setValue("insert");
					Ext.getCmp('champ_id_initial-groupe').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
					tabPanelGroupes.setActiveTab(0);
				}
			},{
				id: 'btInfoGroupes'
				,tooltip:'des informations concernant cet onglet groupe'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les différents groupes disponibles pour y affecter des utilisateurs.'+
							'<br />Dans la base de données, les groupes et les utilisateurs sont stockés dans la table t_roles. '+
							'Une table cor_roles permet de lier les utilisateurs aux différents rôles (groupes).'+
							'Un rôle de niveau groupes a le champ "groupe" = true.'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}			
		]
		,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormGroupes(record);
					loadTabGroupe(record);
					Ext.getCmp('champ_action-groupe').setValue("update");
					Ext.getCmp('champ_id_initial-groupe').setValue(record.data.id_groupe);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
				}
			}
		})
		,plugins:[rowActionsSupprimeGroupes]
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelGroupes.getSelectionModel().selectFirstRow();
			}
		}
    });
	
// ___________________Creation du tableau des applications_________________________________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeApplications = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer cette application',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer cette application ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeApplication(record);
										grid.getStore().remove(record);                                  
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeApplications = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
    gridPanelApplications = new Ext.grid.GridPanel({
		id:"gridapplications"
        ,title: "Applications"
        ,store: application.storeApplications
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_application"
				,sortable: true
			},{
				header: "Application"
				,width: 240
				,dataIndex: "nom_application"
				,sortable: true
			}
			,rowActionsSupprimeApplications
		]
		,tbar:[
			{
				text: 'Ajouter une application'
				,tooltip: 'Ajouter une nouvelle application'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formapplications').getForm().reset();
					Ext.getCmp('champ_action-application').setValue("insert");
					Ext.getCmp('champ_id_initial-application').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
					tabPanelApplications.setActiveTab(0);
				}
			},{
				id: 'btInfoApplications'
				,tooltip:'des informations concernant cet onglet application'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les informations relatives aux applications.'+
							'<br />Dans la base de données, les applications sont stockées dans la table t_applications. '+
							'<br />Une table cor_role_droit_application permet d\'attribuer des droits aux différents rôles selon les applications.'+
							'<br />Cet onglet permet de gérer cette table par glisser/déposer entre grille. N\'oubliez pas d\'attribuer des droits à chaque rôle avant d\'enregistrer'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
		,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormApplications(record);
					loadTabApplication(record);
					Ext.getCmp('champ_action-application').setValue("update");
					Ext.getCmp('champ_id_initial-application').setValue(record.data.id_application);//conserver l'id initialement charger dans le formulaire pour le bouton annuler
				}
			}
		})
		,plugins:rowActionsSupprimeApplications
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelApplications.getSelectionModel().selectFirstRow();
			}
		}
    });
    
// ___________________Creation du tableau des organismes_________________________________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeOrganismes = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer cet organisme',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer cet organisme ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeOrganisme(record);
										grid.getStore().remove(record);                                  
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeOrganismes = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
    gridPanelOrganismes = new Ext.grid.GridPanel({
		id:"gridorganismes"
        ,title: "Organismes"
        ,store: application.storeOrganismes
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_organisme"
				,sortable: true
			},{
				header: "Organisme"
				,width: 240
				,dataIndex: "nom_organisme"
				,sortable: true
			}
			,rowActionsSupprimeOrganismes
		]
		,tbar:[
			{
				text: 'Ajouter un organisme'
				,tooltip: 'Ajouter un nouvel organisme'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formorganismes').getForm().reset();
					Ext.getCmp('champ_action-organisme').setValue("insert");
					Ext.getCmp('champ_id_initial-organisme').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
					panelOrganismes.setActiveTab(0);
				}
			},{
				id: 'btInfoOrganismes'
				,tooltip:'des informations concernant cet onglet organisme'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les informations relatives aux organismes.'+
							'<br />Dans la base de données, les organismes sont stockés dans la table bib_organismes.'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
		,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormOrganismes(record);
					Ext.getCmp('champ_action-organisme').setValue("update");
					Ext.getCmp('champ_id_initial-organisme').setValue(record.data.id_organisme);//conserver l'id initialement charger dans le formulaire pour le bouton annuler
				}
			}
		})
		,plugins:rowActionsSupprimeOrganismes
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelOrganismes.getSelectionModel().selectFirstRow();
			}
		}
    });

// ___________________Creation du tableau des unites_________________________________________________________________________
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeUnites = new Ext.ux.grid.RowActions({
			actions: [{
				tooltip: 'Supprimer cett unité',
				iconCls: 'action-remove'
			}]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
					case 'action-remove':
						Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer cette unité ?'
                                ,function(btn) {
                                    if (btn == 'yes') {
										supprimeUnite(record);
										grid.getStore().remove(record);                                  
                                    }
                                }
                                ,this // scope
                            );
							break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeUnites = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
    gridPanelUnites = new Ext.grid.GridPanel({
		id:"gridunites"
        ,title: "Unites"
        ,store: application.storeUnites
        ,columns: [
			{
				header: "N°"
				,width: 30
				,dataIndex: "id_unite"
				,sortable: true
			},{
				header: "Unite"
				,width: 240
				,dataIndex: "nom_unite"
				,sortable: true
			}
			,rowActionsSupprimeUnites
		]
		,tbar:[
			{
				text: 'Ajouter une unité'
				,tooltip: 'Ajouter une nouvelle unité'
				,iconCls:'add'
				,handler: function() {
					Ext.getCmp('formunites').getForm().reset();
					Ext.getCmp('champ_action-unite').setValue("insert");
					Ext.getCmp('champ_id_initial-unite').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
					panelUnites.setActiveTab(0);
				}
			},{
				id: 'btInfoUnites'
				,tooltip:'des informations concernant cet onglet unite'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les informations relatives aux unités.'+
							'<br />Dans la base de données, les unités sont stockées dans la table bib_unites.'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
		,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormUnites(record);
					Ext.getCmp('champ_action-unite').setValue("update");
					Ext.getCmp('champ_id_initial-unite').setValue(record.data.id_unite);//conserver l'id initialement charger dans le formulaire pour le bouton annuler
				}
			}
		})
		,plugins:rowActionsSupprimeUnites
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				gridPanelUnites.getSelectionModel().selectFirstRow();
			}
		}
    });	

// ___________________Creation du tableau des utilisateurss_________________________________________________________________________
	this.storeUtilisateurs = new Ext.data.GroupingStore({
		reader: new Ext.data.JsonReader(
			{
			fields:[
				'id_role'
				,'role'
				,'nom_role'
				,'prenom_role'
				,'id_unite'
				,'nom_unite'
				,'id_organisme'
				,'nom_organisme'
				,'email'
				,'identifiant'
				,'pass'
				,'pn'
				,'remarques'
			]}
		)
		,groupField:'nom_organisme'
		,url: 'get_utilisateurs.php'
		,method: 'GET'
		,sortInfo: {field: 'nom_role',direction: 'ASC'}
		,autoLoad:true
	});
	//boutton '+' en début de ligne dans le grid visite
	var expander = new Ext.grid.RowExpander({
        tpl : new Ext.XTemplate(//Template pour le détail de la visite
			'<p><b>E-mail :</b> {email}</p>'
			,'<p><b>identifiant :</b> {identifiant}</p>'
			,'<p><b>Unité :</b> {nom_unite}</p>'
			,'<p><b>Remarques :</b> {remarques}</p>'
		),
		enableCaching:false //permet de reconstruire le contenu de l'expandder après modification du storeVisites depuis le formulaire visite Sinon le contenu est en cache et ne s'actualise pas
    });
	//préparation des colonnes avec les icones d'action dans les grids (pour le grid aires)
	if(application.user.droits == 6){ //bouton modifier si droit = admin
		var rowActionsSupprimeUtilisateurs = new Ext.ux.grid.RowActions({
			actions: [
				{
                iconCls: 'action-remove'
                ,tooltip: 'Supprimer ce role'
				}
			]
			,listeners: {
				action: function (grid, record, action) {
					switch (action) {
						case 'action-remove':
						    Ext.Msg.confirm('Attention','Etes-vous certain de vouloir supprimer ce role ?'
							,function(btn) {
								if (btn == 'yes') {
									supprimeUtilisateur(record);
									grid.getStore().remove(record);
								}
							}
							,this // scope
						);
						break;
					}
				}
			}
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}
	else{ //colonne bouton vide si droit différent de admin
		var rowActionsSupprimeUtilisateurs = new Ext.ux.grid.RowActions({
			actions: [{}]
			,fixed: true
			,autoWidth: false
			,width: 25
		});
	}

	gridPanelUtilisateurs = new Ext.grid.GridPanel({
		id:"gridutilisateurs"
		,title:'Utilisateurs'
		,store: this.storeUtilisateurs
		,colModel: new Ext.grid.ColumnModel({
			defaults: {
				width: 120,
				sortable: true
			}
			,columns: [
				expander
				,{id: 'id_role',header: 'Id', dataIndex: 'id_role', hidden: false}
				,{header: 'Organisme', width: 70, dataIndex: 'nom_organisme', hidden: true}
				,{header: 'Role',width: 130, dataIndex: 'role',sortable: true}
				,rowActionsSupprimeUtilisateurs
			]
		})
		,tbar:[
			{
				text: 'Ajouter un utilisateur'
				,tooltip: 'Ajouter un nouvel utilisateur'
				,iconCls:'add'
				,handler: function() {
					application.resetFormUtilisateur();
					//tabPanelUtilisateurs.setActiveTab(0);
				}
			},{
				id: 'btInfoUtilisateurs'
				,tooltip:'des informations concernant cet onglet utilisateur'
				,iconCls:'mf-info'
				,handler: function() {
					Ext.Msg.show({
						title: 'Information'
						,msg: 'Cet onglet permet de gérer les informations relatives aux utilisateurs.'+
							'<br />Dans la base de données, les utilisateurs sont stockées dans la table t_roles, avec les rôles de niveau groupe. '+
							'<br />Une table cor_roles permet de lier les utilisateurs aux différents rôles (groupes).'
						,icon: Ext.Msg.INFO
						,buttons: Ext.Msg.OK
					});
				}
			}
		]
		,sm: new Ext.grid.RowSelectionModel({
			singleSelect:true
			,listeners:{
				rowselect:function(sm, rowIndex, record) {
					loadFormUtilisateurs(record);
					Ext.getCmp('suppr-pass').setValue(false);
					Ext.getCmp('champ_mdp1').setValue(null);
					Ext.getCmp('champ_mdp2').setValue(null);
					Ext.getCmp('champ_action-utilisateur').setValue("update");
					Ext.getCmp('champ_id_initial-utilisateur').setValue(record.data.id_role);//conserver l'id initialement charger dans le formulaire pour le bouton annuler
				}
			}
		})
		,plugins: [expander,rowActionsSupprimeUtilisateurs]
		,view: new Ext.grid.GroupingView({
			forceFit:false,
			showGroupName:false,
			startCollapsed:true,
			groupTextTpl: '{text} ({[values.rs.length]} {[values.rs.length > 1 ? "roles" : "role"]})'
		})
		,stripeRows: true
		,autoExpandColumn: 'id_role'
		,loadMask: true
		,width: 300
		,height: 300
		,listeners: {
			expand: function (p) {
				Ext.getCmp('panelCentre').layout.setActiveItem(p.id + '-panel');
				application.resetFormUtilisateur();
			}
		}
	});

//-----------------------------------------------------fin de la partie de création des datapanels---------------------------------------------


//-------------------------Les 2 panels de l'onglet Gestion des roles--------------------
	//accordion de gauche à placer dans le datapanel
	var accordionGauche = new Ext.Panel({
		id:'accordeon-gauche'
        ,margins : '5 0 5 5'
        ,split  : true
        ,width  : 300
        ,layout :'accordion'
        ,items  : [gridPanelUtilisateurs, gridPanelGroupes, gridPanelApplications, gridPanelMenus, gridPanelDroits, gridPanelOrganismes, gridPanelUnites]
    });
	
     //  Panel de gauche contenant l'accordion
	var panelGauche = new Ext.Panel({
        title   : 'Gestion des tables'
		,region : 'west'
        ,layout : 'fit'
        ,width : 300
		,split: true
		,items  : [accordionGauche]		
    });
	// panel principal
	var panelCentre = new Ext.Panel({
		id:'panelCentre'
		,region : 'center'
        ,layout : 'card'
		,split: true
		,activeItem: 0
		,border: false
		,items: [
			// from basic.js:
			tabPanelUtilisateurs, panelDroits, panelOrganismes, panelUnites, tabPanelGroupes, tabPanelApplications, tabPanelMenus
			// from custom.js:
			//rowLayout, centerLayout,
		]	
    });

//----------Le tabpanel avec les deux onglets de l'application --------------------------------------------
//les deux onglets de l'application
	var tabUtilisateurs = new Ext.Panel({	
		layout: 'border'
		,title   : 'Utilisateurs'
		,items: [ panelGauche,panelCentre ]
	});

//création du tabpanel 
	var tabs = new Ext.TabPanel({
        id:'tabPanel'
        ,activeTab: 0
		,region : 'center'
		,frame:true
		,defaults:{autoScroll: true}
		,items:[
			tabUtilisateurs
			,{
                title: 'Aide'
                ,autoLoad: {url: 'aide.html'}
            }]
	});
	
//----------Les bandeaux haut et bas --------------------------------------------	
//bandeau du haut
	var bandeau = new Ext.Panel({
		region : 'north'
		,bodyStyle: 'background: transparent'
        ,layout : 'fit'
		,border:false
		,height: 60
		,cls: 'application-header'		
    });

//bandeau du bas
	var SudPanel = new Ext.Panel({
		region:"south"
        ,height:20
		,bbar: new Ext.Toolbar({
			items: [
			   '->',
			   '&copy; Parc national des Ecrins - 2015',
			   '-',
			   'Version ' + version
               ,{
                    text: 'Déconnexion'
                    ,iconCls: 'disconnect'
                    ,handler: function() {
                        window.location.href = 'index.php' 
                    }
                }
			]
		})
    });
 
//------------Le conteneur général avec le tabpanel (2 onglets de l'appli) + les 2 panels haut et bas --
	this.viewPort = new Ext.Viewport({
        layout: 'border'
		,defaults: {
			border: false
		}
        ,items: [ tabs,bandeau,SudPanel ]
    });
//-----------------------------------------------------------------------------------------------------------------------
//
//				fin de la construction du layout					     
//
//-----------------------------------------------------------------------------------------------------------------------
application.resetFormUtilisateur();//on initialise sur l'onglet utilisateurs donc on ouvre par défaut sur la création d'un nouvel utilisateur
}//fin du init
}//fin du return		
}();//fin de la fonction de construction de la page de l'appli

