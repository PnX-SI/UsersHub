/*
 * ================  panelMenus config  =======================
 */
 var storeApplis = new Ext.data.JsonStore({
	url: 'get_applications.php'
	,method: 'GET'
	,fields: ['id_application', 'nom_application']
	,sortInfo: {field: 'id_application',direction: 'ASC'}
	,autoLoad:true
});
var comboApplications = new Ext.form.ComboBox({
	fieldLabel: 'Application',
	name: 'id_application',
	store: storeApplis,
	displayField:'nom_application',
	hiddenName:'id_application',
	valueField: 'id_application',
	allowBlank:false,
	blankText: 'Vous devez choisir une application.',
	typeAhead: true,
	mode: 'local',
	triggerAction: 'all',
	selectOnFocus:true,
	forceSelection:true,
	editable:false,
	width:170,
	resizable:true
});
var panelFormMenus = {
	id:'formmenus'
	,xtype: 'form'
	,title:'La liste'
	,region:'center'
	,width:500
	,labelWidth: 125 // label settings here cascade unless overridden
	,frame:true
	,bodyStyle:'padding:15px'
	,defaultType: 'textfield'
	,items: [
		{
			id:'champ_id_menu' 
			,xtype:'hidden'
			,name: 'id_menu'
		},{
			fieldLabel: 'Nom de la liste'
			,name: 'nom_menu'
			,allowBlank:false
			,blankText: 'Le nom de la liste est obligatoire.'
			,width:300
		},{
			id:'champ_desc-menu'
			,xtype:'textarea'
			,name: 'desc_menu'
			,fieldLabel: 'Description'
			,width:300
			,height:250
		}
		,comboApplications
		,{
			id:'champ_action-menu' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-menu' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'menuSaveButton'
		,handler: function(){submitFormMenus();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeMenus;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-menu').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_menu', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formmenus').getForm().reset();
			loadFormMenus(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};

var tabPanelMenus = new Ext.TabPanel({ 
	activeTab: 0
	,id:'gridmenus-panel'
	,frame:true
	,defaults:{autoScroll: true}
	,plugins: Ext.ux.TabCloseMenu
	//,bodyStyle: 'padding:5px'
	,title: 'Gestion des listes'
	,items: [panelFormMenus]
});

//remplissage du formulaire
var loadFormMenus = function(record){
	var form = Ext.getCmp('formmenus').getForm();
	form.findField('id_menu').setValue(record.data.id_menu);
	form.findField('champ_id_initial-menu').setValue(record.data.id_menu);
	form.findField('nom_menu').setValue(record.data.nom_menu);
	form.findField('desc_menu').setValue(record.data.desc_menu);
	form.findField('id_application').setValue(record.data.id_application);
};
var supprimeMenu = function(record) {
	Ext.Ajax.request({
		url: 'update_menus.php?id_menu='+ record.data.id_menu +'&action=delete&nom_menu='+record.data.nom_menu
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formmenus').getForm().reset();
				gridPanelMenus.getSelectionModel().selectFirstRow();
				Ext.ux.Toast.msg('Ok !', result.msg);
			} else {
				Ext.Msg.alert('Attention', 'Une erreur s\'est produite.</br>L\'enregistrement n\'a pas été supprimée.');
			}
		}
		,failure: function() {
			alert("pas supprimé, erreur");
		}
		,scope: this
	});
};

var submitFormMenus = function() {
	var form = Ext.getCmp('formmenus').getForm();
	var bouton = Ext.getCmp('menuSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_menus.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeMenus.reload();
				Ext.getCmp('champ_action-menu').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('menuSaveButton').setText('Enregistrer');
				var msg;
				switch (action.failureType) {
					  case Ext.form.Action.CLIENT_INVALID:
						  msg = "Les informations saisies sont invalides";
						  break;
					  case Ext.form.Action.CONNECT_FAILURE:
						  msg = "Problème de connexion au serveur";
						  break;
					  case Ext.form.Action.SERVER_INVALID:
						  msg = "Erreur lors de l'enregistrement : vérifier les données saisies !";
						  break;
				}
				Ext.Msg.show({
				  title: 'Erreur'
				  ,msg: msg
				  ,buttons: Ext.Msg.OK
				  ,icon: Ext.MessageBox.ERROR
				});
			}
		});
	}
	else{
		Ext.Msg.alert('Attention', 'Une information est mal saisie ou n\'est pas valide.</br>Vous devez la corriger avant d\'enregistrer.');
	}
};
var loadTabMenu = function(record){
	var id = 'tabpanel-'+record.data.id_menu;
	var tab = tabPanelMenus.getComponent(id);
	if(tab){
		tabPanelMenus.setActiveTab(tab);
	}else{
		tabPanelMenus.remove(tabPanelMenus.getComponent(1));
		var p = tabPanelMenus.add(application.peuplerMenus(record)).show();
	}
};
var supprimeTabMenu = function(record){
	var id = 'tabpanel-'+record.data.id_menu;
	var tab = tabPanelMenus.getComponent(id);
	if(tab){
		tabPanelMenus.remove(tab);
	}
};

