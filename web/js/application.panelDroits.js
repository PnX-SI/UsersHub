/*
 * ================  panelDroits config  =======================
 */

var panelFormDroits = {
	id:'formdroits'
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
			,name: 'id_droit'
			,allowBlank:false
			,blankText: 'L\'identifiant du droit est obligatoire.</br>il s\'agit de la clef primaire de la table "bib_droits".</br>Ce doit être un nombre entier.'
			,width:300
		},{
			fieldLabel: 'Nom du droit'
			,name: 'nom_droit'
			,allowBlank:false
			,blankText: 'Le nom du droit est obligatoire.'
			,width:300
		},{
			id:'champ_desc-droit'
			,xtype:'textarea'
			,name: 'desc_droit'
			,fieldLabel: 'Description'
			,width:300
			,height:250
		},{
			id:'champ_action-droit' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-droit' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'droitSaveButton'
		,handler: function(){submitFormDroits();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.storeDroits;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-droit').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_droit', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formdroits').getForm().reset();
			loadFormDroits(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	,height:400
};

var panelDroits = new Ext.Panel({ 
	id:'griddroits-panel'
	,bodyStyle: 'padding:5px'
	,title: 'Gestion des droits'
	,items: [panelFormDroits]
	,layout:'column'
});

//remplissage du formulaire
var loadFormDroits = function(record){
	var form = Ext.getCmp('formdroits').getForm();
	form.findField('id_droit').setValue(record.data.id_droit);
	form.findField('champ_id_initial-droit').setValue(record.data.id_droit);
	form.findField('nom_droit').setValue(record.data.nom_droit);
	form.findField('desc_droit').setValue(record.data.desc_droit);
};
var supprimeDroit = function(record) {
	Ext.Ajax.request({
		url: 'update_droits.php?id_droit='+ record.data.id_droit+'&action=delete&nom_droit='+ record.data.nom_droit
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				Ext.getCmp('formdroits').getForm().reset();
				gridPanelDroits.getSelectionModel().selectFirstRow();
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

var submitFormDroits = function() {
	var form = Ext.getCmp('formdroits').getForm();
	var bouton = Ext.getCmp('droitSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_droits.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.storeDroits.reload();
				Ext.getCmp('champ_action-droit').setValue("update");
				bouton.setText('Enregistrer');
			}
			,failure: function(form, action) {
				Ext.getCmp('droitSaveButton').setText('Enregistrer');
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
