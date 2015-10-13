/*
 * ================  panelOrganismes config  =======================
 */

var panelFormOrganismes = {
	id:'formorganismes'
	,xtype: 'form'
	,title:'Formulaire'
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
			,name: 'id_organisme'
			,allowBlank:false
			,blankText: 'L\'identifiant de l\'organisme est obligatoire.</br>il s\'agit de la clef primaire de la table "bib_organismes".</br>Ce doit être un nombre entier.'
			,width:300
		},{
			fieldLabel: 'Nom de l\'organisme'
			,name: 'nom_organisme'
			,allowBlank:false
			,blankText: 'Le nom de l\'organisme est obligatoire.'
			,width:300
		},{
			id:'champ_adresse-organisme'
			,xtype:'textarea'
			,name: 'adresse_organisme'
			,fieldLabel: 'Adresse'
			,width:300
			,height:75
		},{
			fieldLabel: 'Code postal'
			,name: 'cp_organisme'
			,width:300
		},{
			fieldLabel: 'Ville'
			,name: 'ville_organisme'
			,width:300
		},{
			fieldLabel: 'Téléphone'
			,name: 'tel_organisme'
			,width:300
		},{
			fieldLabel: 'Fax'
			,name: 'fax_organisme'
			,width:300
		},{
			fieldLabel: 'Courriel'
			,name: 'email_organisme'
			,width:300
		},{
			id:'champ_action-organisme' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-organisme' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'organismeSaveButton'
		,handler: function(){submitFormOrganismes();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeOrganismes;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-organisme').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_organisme', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formorganismes').getForm().reset();
			loadFormOrganismes(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};

var panelOrganismes = new Ext.Panel({ 
	id:'gridorganismes-panel'
	,bodyStyle: 'padding:5px'
	,title: 'Gestion des organismes'
	,items: [panelFormOrganismes]
	,layout:'column'
});

//remplissage du formulaire
var loadFormOrganismes = function(record){
	var form = Ext.getCmp('formorganismes').getForm();
	form.findField('id_organisme').setValue(record.data.id_organisme);
	form.findField('champ_id_initial-organisme').setValue(record.data.id_organisme);
	form.findField('nom_organisme').setValue(record.data.nom_organisme);
	form.findField('adresse_organisme').setValue(record.data.adresse_organisme);
	form.findField('cp_organisme').setValue(record.data.cp_organisme);
	form.findField('ville_organisme').setValue(record.data.ville_organisme);
	form.findField('tel_organisme').setValue(record.data.tel_organisme);
	form.findField('fax_organisme').setValue(record.data.fax_organisme);
	form.findField('email_organisme').setValue(record.data.email_organisme);
};
var supprimeOrganisme = function(record) {
	Ext.Ajax.request({
		url: 'update_organismes.php?id_organisme='+ record.data.id_organisme+'&action=delete&nom_organisme='+ record.data.nom_organisme
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formorganismes').getForm().reset();
				gridPanelOrganismes.getSelectionModel().selectFirstRow();
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

var submitFormOrganismes = function() {
	var form = Ext.getCmp('formorganismes').getForm();
	var bouton = Ext.getCmp('organismeSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_organismes.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeOrganismes.reload();
				Ext.getCmp('champ_action-organisme').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('organismeSaveButton').setText('Enregistrer');
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