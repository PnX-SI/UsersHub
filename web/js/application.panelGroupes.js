/*
 * ================  panelGroupes config  =======================
 */

var panelFormGroupes = {
	id:'formgroupes'
	,xtype: 'form'
	,title:'Le groupe'
	,region:'center'
	,width:500
	,labelWidth: 125 // label settings here cascade unless overridden
	,frame:true
	,bodyStyle:'padding:15px'
	,defaultType: 'textfield'
	,items: [
		{
			id:'champ_id_groupe' 
			,xtype:'hidden'
			,name: 'id_groupe'
		},{
			fieldLabel: 'Nom du groupe'
			,name: 'nom_groupe'
			,allowBlank:false
			,blankText: 'Le nom du groupe est obligatoire.'
			,width:300
		},{
			id:'champ_desc-groupe'
			,xtype:'textarea'
			,name: 'desc_groupe'
			,fieldLabel: 'Description'
			,width:300
			,height:250
		},{
			id:'champ_action-groupe' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-groupe' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'groupeSaveButton'
		,handler: function(){submitFormGroupes();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeGroupes;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-groupe').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_groupe', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formgroupes').getForm().reset();
			loadFormGroupes(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};

var tabPanelGroupes = new Ext.TabPanel({ 
	activeTab: 0
	,id:'gridgroupes-panel'
	,frame:true
	,defaults:{autoScroll: true}
	,plugins: Ext.ux.TabCloseMenu
	//,bodyStyle: 'padding:5px'
	,title: 'Gestion des groupes'
	,items: [panelFormGroupes]
});

//remplissage du formulaire
var loadFormGroupes = function(record){
	var form = Ext.getCmp('formgroupes').getForm();
	form.findField('id_groupe').setValue(record.data.id_groupe);
	form.findField('champ_id_initial-groupe').setValue(record.data.id_groupe);
	form.findField('nom_groupe').setValue(record.data.nom_groupe);
	form.findField('desc_groupe').setValue(record.data.desc_groupe);
};
var supprimeGroupe = function(record) {
	Ext.Ajax.request({
		url: 'update_groupes.php?id_groupe='+ record.data.id_groupe +'&action=delete&nom_groupe='+record.data.nom_groupe
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formgroupes').getForm().reset();
				gridPanelGroupes.getSelectionModel().selectFirstRow();
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

var submitFormGroupes = function() {
	var form = Ext.getCmp('formgroupes').getForm();
	var bouton = Ext.getCmp('groupeSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_groupes.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeGroupes.reload();
				Ext.getCmp('champ_action-groupe').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('groupeSaveButton').setText('Enregistrer');
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
var loadTabGroupe = function(record){
	var id = 'tabpanel-'+record.data.id_groupe;
	var tab = tabPanelGroupes.getComponent(id);
	if(tab){
		tabPanelGroupes.setActiveTab(tab);
	}else{
		tabPanelGroupes.remove(tabPanelGroupes.getComponent(1));
		var p = tabPanelGroupes.add(application.peuplerGroupes(record)).show();
		//tabPanel.setActiveTab(p);
	}
};
//------------------------------------gestion de la composition du groupe------------------------------------------------------------------
	