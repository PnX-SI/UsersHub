/*
 * ================  panelUnites config  =======================
 */

var panelFormUnites = {
	id:'formunites'
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
			,name: 'id_unite'
			,allowBlank:false
			,blankText: 'L\'identifiant de l\'unité est obligatoire.</br>il s\'agit de la clef primaire de la table "bib_unites".</br>Ce doit être un nombre entier.'
			,width:300
		},{
			fieldLabel: 'Nom de l\'unité'
			,name: 'nom_unite'
			,allowBlank:false
			,blankText: 'Le nom de l\'unité est obligatoire.'
			,width:300
		},{
			id:'champ_adresse-unite'
			,xtype:'textarea'
			,name: 'adresse_unite'
			,fieldLabel: 'Adresse'
			,width:300
			,height:75
		},{
			fieldLabel: 'Code postal'
			,name: 'cp_unite'
			,width:300
		},{
			fieldLabel: 'Ville'
			,name: 'ville_unite'
			,width:300
		},{
			fieldLabel: 'Téléphone'
			,name: 'tel_unite'
			,width:300
		},{
			fieldLabel: 'Fax'
			,name: 'fax_unite'
			,width:300
		},{
			fieldLabel: 'Courriel'
			,name: 'email_unite'
			,width:300
		},{
			id:'champ_action-unite' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-unite' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'uniteSaveButton'
		,handler: function(){submitFormUnites();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeUnites;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-unite').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_unite', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formunites').getForm().reset();
			loadFormUnites(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};

var panelUnites = new Ext.Panel({ 
	id:'gridunites-panel'
	,bodyStyle: 'padding:5px'
	,title: 'Gestion des unités'
	,items: [panelFormUnites]
	,layout:'column'
});

//remplissage du formulaire
var loadFormUnites = function(record){
	var form = Ext.getCmp('formunites').getForm();
	form.findField('id_unite').setValue(record.data.id_unite);
	form.findField('champ_id_initial-unite').setValue(record.data.id_unite);
	form.findField('nom_unite').setValue(record.data.nom_unite);
	form.findField('adresse_unite').setValue(record.data.adresse_unite);
	form.findField('cp_unite').setValue(record.data.cp_unite);
	form.findField('ville_unite').setValue(record.data.ville_unite);
	form.findField('tel_unite').setValue(record.data.tel_unite);
	form.findField('fax_unite').setValue(record.data.fax_unite);
	form.findField('email_unite').setValue(record.data.email_unite);
};
var supprimeUnite = function(record) {
	Ext.Ajax.request({
		url: 'update_unites.php?id_unite='+ record.data.id_unite+'&action=delete&nom_unite='+ record.data.nom_unite
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formunites').getForm().reset();
				gridPanelUnites.getSelectionModel().selectFirstRow();
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

var submitFormUnites = function() {
	var form = Ext.getCmp('formunites').getForm();
	var bouton = Ext.getCmp('uniteSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_unites.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeUnites.reload();
				Ext.getCmp('champ_action-unite').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('uniteSaveButton').setText('Enregistrer');
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
