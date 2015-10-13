/*
 * ================  panelApplications config  =======================
 */

var panelFormApplications = {
	id:'formapplications'
	,xtype: 'form'
	,title:'L\'application'
	,region:'center'
	,width:500
	,labelWidth: 125 // label settings here cascade unless overridden
	,frame:true
	,bodyStyle:'padding:15px'
	,defaultType: 'textfield'
	,items: [
		{
			fieldLabel: 'ID'
			,xtype : 'numberfield'
			,allowDecimals :false
			,allowNegative: false
			,name: 'id_application'
			,allowBlank:false
			,blankText: 'L\'identifiant de l\'application est obligatoire.</br>il s\'agit de la clef primaire de la table "t_applications".</br>Ce doit être un nombre entier.'
			,width:300
		},{
			fieldLabel: 'Nom de l\'application'
			,name: 'nom_application'
			,allowBlank:false
			,blankText: 'Le nom de l\'application est obligatoire.'
			,width:300
		},{
			id:'champ_desc-application'
			,xtype:'textarea'
			,name: 'desc_application'
			,fieldLabel: 'Description'
			,width:300
			,height:250
		},{
			id:'champ_action-application' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-application' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'applicationSaveButton'
		,handler: function(){submitFormApplications();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeApplications;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-application').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_application', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formapplications').getForm().reset();
			loadFormApplications(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};
var panelInfoApplications = new Ext.Panel({ 
	id:'infoapplications-panel'
	,bodyStyle:'padding:25px; background:transparent'
	,style:'margin-left:15px;'
	,title: 'Informations'
	,html : 'Cet onglet permet de gérer les différentes applications existantes.<br />L\'affectation des utilisateurs ou des groupes avec des droits se fait via l\'onglet "Gestion des utilisateurs". <br />Attention aux répercussions possiblement facheuses des modifications de l\'identifiant lors de la synchronisation vers les bases avec Talend.'
	,layout:'fit'
	,region:'East'
	,width:300
	,height:374
});
var tabPanelApplications = new Ext.TabPanel({ 
	activeTab: 0
	,id:'gridapplications-panel'
	,frame:true
	,defaults:{autoScroll: true}
	,plugins: Ext.ux.TabCloseMenu
	//,bodyStyle: 'padding:5px'
	,title: 'Gestion des applications'
	,items: [panelFormApplications]
});

//remplissage du formulaire
var loadFormApplications = function(record){
	var form = Ext.getCmp('formapplications').getForm();
	form.findField('id_application').setValue(record.data.id_application);
	form.findField('champ_id_initial-application').setValue(record.data.id_application);
	form.findField('nom_application').setValue(record.data.nom_application);
	form.findField('desc_application').setValue(record.data.desc_application);
};
var supprimeApplication = function(record) {
	Ext.Ajax.request({
		url: 'update_applications.php?id_application='+ record.data.id_application +'&action=delete&nom_application='+record.data.nom_application
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formapplications').getForm().reset();
				storeApplis.reload();
				gridPanelApplications.getSelectionModel().selectFirstRow();
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

var submitFormApplications = function() {
	var form = Ext.getCmp('formapplications').getForm();
	var bouton = Ext.getCmp('applicationSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_applications.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeApplications.reload();
				storeApplis.reload();
				Ext.getCmp('champ_action-application').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('applicationSaveButton').setText('Enregistrer');
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
var loadTabApplication = function(record){
	var id = 'tabpanel-'+record.data.id_application;
	var tab = tabPanelApplications.getComponent(id);
	if(tab){
		tabPanelApplications.setActiveTab(tab);
	}else{
		tabPanelApplications.remove(tabPanelApplications.getComponent(1));
		var p = tabPanelApplications.add(application.peuplerApplications(record)).show();
	}
};
var supprimeTabApplication = function(record){
	var id = 'tabpanel-'+record.data.id_application;
	var tab = tabPanelApplications.getComponent(id);
	if(tab){
		tabPanelApplications.remove(tab);
	}
};

