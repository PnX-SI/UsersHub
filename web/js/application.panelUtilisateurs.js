/*
 * ================  panelUtilisateurs config  =======================
 */
var storeUnites = new Ext.data.JsonStore({
	url: 'get_unites.php'
	,method: 'GET'
	,fields: ['id_unite', 'nom_unite']
	,sortInfo: {field: 'id_unite',direction: 'ASC'}
	,autoLoad:true
});
var comboUnite = new Ext.form.ComboBox({
	fieldLabel: 'Unite',
	name: 'id_unite',
	store: storeUnites,
	displayField:'nom_unite',
	hiddenName:'id_unite',
	valueField: 'id_unite',
	allowBlank:false,
	blankText: 'L\'unité est obligatoire. Choisir "autres" dans la liste si besoin.',
	typeAhead: true,
	mode: 'local',
	triggerAction: 'all',
	selectOnFocus:true,
	forceSelection:true,
	editable:false,
	width:300,
	resizable:true
});
var storeOrganismes = new Ext.data.JsonStore({
	url: 'get_organismes.php'
	,method: 'GET'
	,fields: ['id_organisme', 'nom_organisme']
	,sortInfo: {field: 'id_organisme',direction: 'ASC'}
	,autoLoad:true
});
var comboOrganisme = new Ext.form.ComboBox({
	fieldLabel: 'Organisme',
	name: 'id_organisme',
	store: storeOrganismes,
	displayField:'nom_organisme',
	hiddenName:'id_organisme',
	valueField: 'id_organisme',
	allowBlank:false,
	blankText: 'L\'organisme est obligatoire. Choisir "autres" dans la liste si besoin.',
	typeAhead: true,
	mode: 'local',
	triggerAction: 'all',
	selectOnFocus:true,
	forceSelection:true,
	editable:false,
	width:300,
	resizable:true
});
Ext.apply(Ext.form.VTypes, {
  password: function(val, field) {
    if (field.initialPassField) {
      var pwd = Ext.getCmp(field.initialPassField);
      return (val == pwd.getValue());
    }
    return true;
  },
  passwordText: 'Les deux mots de passe entrés ne sont pas identiques'
});
var panelFormUtilisateurs = {
	id:'formutilisateurs'
	,xtype: 'form'
	,title:'L\'utilisateur'
	,region:'center'
	,width:500
    ,height:510
	,labelWidth: 125 // label settings here cascade unless overridden
	,frame:true
	,bodyStyle:'padding:15px'
	,defaultType: 'textfield'
	,items: [
		{
			id:'champ-id_role'
			,xtype:'hidden'
			,name: 'id_role'
		},{
			fieldLabel: 'Nom '
			,name: 'nom_role'
			,allowBlank:false
			,blankText: 'Le nom de l\'utilisateur est obligatoire.'
			,width:300
			,enableKeyEvents:true
			,listeners: {
				keyup: function (textField,e) {
					var txt = Ext.getCmp('formutilisateurs').getForm().findField('prenom_role').getValue()+'.'+textField.getValue();
					Ext.getCmp('champ_identifiant').setValue(txt.toLowerCase());
					Ext.getCmp('champ_email').setValue(txt.toLowerCase()+'@'+emailSuffix);
				}
			}
		},{
			fieldLabel: 'Prénom '
			,name: 'prenom_role'
			,allowBlank:true
			,width:300
			,enableKeyEvents:true
			,listeners: {
				keyup: function (textField,e) {
					var txt = textField.getValue()+'.'+Ext.getCmp('formutilisateurs').getForm().findField('nom_role').getValue();
					Ext.getCmp('champ_identifiant').setValue(txt.toLowerCase());
					Ext.getCmp('champ_email').setValue(txt.toLowerCase()+'@'+emailSuffix);
				}
			}
		},{
			id:'champ_email'
			,name: 'email'
			,fieldLabel: 'E-mail '
			,width:300
		}
        // ,{
			// id:'organisme'
			// ,name: 'organisme'
			// ,fieldLabel: 'Organisme '
			// ,width:300
		// }
        ,comboOrganisme
		,comboUnite
		,{
			id:'pn'
			,xtype:'checkbox'
			,name: 'pn'
			,fieldLabel: 'Agent interne '
			,width:300
			,checked:true
		},{
			id:'user-remarques'
			,xtype:'textarea'
			,name: 'remarques'
			,fieldLabel: 'Remarques'
			,width:300
			,height:100
		},{	
			xtype: 'label'
			,id: 'label-identification'
			,cls: 'label-bold'
			,html: '<br/>----------------------------- Paramètres d\'identification ----------------------------- <br /><br />'
		},{
			id:'champ_identifiant'
			,name: 'identifiant'
			,fieldLabel: 'Login '
			,width:300
		},{	
			xtype: 'label'
			,id: 'label-pass'
			,cls: 'label-pass-blue'
			,html: ''
		},{
			id:'champ_mdp1'
			,name: 'pass'
			,fieldLabel: 'Mot de passe '
			,width:300
			,inputType: 'password'
			//,minLength: 6
			,maxLength: 20
			,minLengthText: 'Le mot de passe doit avoir au moins 6 caractères.'
		},{
			id:'champ_mdp2'
			,name: 'pass2'
			,fieldLabel: 'Confirmation '
			,width:300
			,inputType: 'password'
			//,minLength: 6
			,maxLength: 20
			,minLengthText: 'Le mot de passe doit avoir au moins 6 caractères.'
			,vtype: 'password' 
			,initialPassField: 'champ_mdp1'

		},{
			id:'suppr-pass'
			,xtype:'checkbox'
			,name: 'supprpass'
			,fieldLabel: 'Supprimer le mot de passe '
			,width:300
			,checked:false
            ,listeners: {
				check: function (box,check) {
					if(check){Ext.getCmp('formutilisateurs').getForm().findField('identifiant').setValue(null);}
				}
			}
		},{
			id:'champ_action-utilisateur' 
			,xtype:'hidden'
			,name: 'action'
		},{
			id:'champ_id_initial-utilisateur' 
			,xtype:'hidden'
			,name: 'id_initial'
		}
	]
	,buttons: [{
		text:'Enregistrer'
		,id:'utilisateurSaveButton'
		,handler: function(){submitFormUtilisateurs();}
	},{
		text: 'Annuler'
		,handler: function(){
			var store = application.layout.storeUtilisateurs;//récupération du dépot de données (store) à modifier
			var id = Ext.getCmp('champ_id_initial-utilisateur').getValue(); //valeur de la valeur initiale de l'id chargé
			var reg=new RegExp("^"+id+"$", "g");
			var meslignes = store.query('id_role', reg);//retourne un tableau mais avec une seule ligne, celle correspondant à l'id
			var record = meslignes.first(); //retourne l'enregistrement de la bonne ligne dans le store
			Ext.getCmp('formutilisateurs').getForm().reset();
			loadFormUtilisateurs(record); //on recharge le formulaire depuis le store qui n'a pas changé
		}
	}]
	
};

var tabPanelUtilisateurs = new Ext.Panel({ 
	id:'gridutilisateurs-panel'
	,bodyStyle: 'padding:5px'
	,title: 'Gestion des utilisateurs'
	,items: [panelFormUtilisateurs]
	,layout:'column'
    ,autoScroll:true
});

//remplissage du formulaire
var loadFormUtilisateurs = function(record){
	var form = Ext.getCmp('formutilisateurs').getForm();
	form.findField('id_role').setValue(record.data.id_role);
	form.findField('champ_id_initial-utilisateur').setValue(record.data.id_role);
	form.findField('nom_role').setValue(record.data.nom_role);
	form.findField('prenom_role').setValue(record.data.prenom_role);
	form.findField('identifiant').setValue(record.data.identifiant);
	form.findField('email').setValue(record.data.email);
	form.findField('id_organisme').setValue(record.data.id_organisme);
	form.findField('pn').setValue(record.data.pn=='oui');
	form.findField('remarques').setValue(record.data.remarques);
	form.findField('id_unite').setValue(record.data.id_unite);
	Ext.getCmp('label-pass').setText(record.data.pass,false);
    Ext.getCmp('champ_action-utilisateur').setValue("update");
    Ext.getCmp('formutilisateurs').setTitle('Modification de l\'utilisateur '+record.data.prenom_role+ ' '+record.data.nom_role);
	if(record.data.pass=='oui'){
		Ext.getCmp('label-pass').addClass('label-pass-red');
		Ext.getCmp('label-pass').removeClass('label-pass-blue');
		Ext.getCmp('label-pass').setText('Cet utilisateur dispose d\'un mot de passe. <br />Vous pouvez toutefois en saisir un nouveau ci-dessous.<br /> <br /> ',false);
	}
	else{
		Ext.getCmp('label-pass').addClass('label-pass-blue');
		Ext.getCmp('label-pass').removeClass('label-pass-red');
		Ext.getCmp('label-pass').setText('Cet utilisateur n\'a actuellement pas de mot de passe. <br />Vous pouvez en saisir un ci-dessous.<br /> <br />',false);
	}
};

var supprimeUtilisateur = function(record) {
	Ext.Ajax.request({
		url: 'update_utilisateurs.php?id_role='+ record.data.id_role+'&action=delete&nom_role='+ record.data.nom_role+'&prenom_role='+ record.data.prenom_role
		,method: 'GET'
		,success: function(request) {
			var result = Ext.util.JSON.decode(request.responseText);
			if (result.success) {
				application.resetFormUtilisateur();
                if(Ext.getCmp('grid-user-droits-gauche')){Ext.getCmp('grid-user-droits-gauche').getStore().reload();}
                if(Ext.getCmp('grid-user-groupes-gauche')){Ext.getCmp('grid-user-groupes-gauche').getStore().reload();}
				Ext.ux.Toast.msg('Ok !', result.msg);
			} else {
				Ext.Msg.alert('Attention', 'Une erreur s\'est produite.</br>L\'utilisateur n\'a pas été supprimé.');
			}
		}
		,failure: function() {
			alert("pas supprimé, erreur");
		}
		,scope: this
	});
};

var submitFormUtilisateurs = function() {
	var form = Ext.getCmp('formutilisateurs').getForm();
	var bouton = Ext.getCmp('utilisateurSaveButton');
	if(form.isValid()){
		bouton.setText('Enregistrement en cours...');
		form.submit({
			url: 'update_utilisateurs.php'
			,method: 'GET'
			,success: function(result, action) {
				var result = Ext.util.JSON.decode(action.response.responseText);
				Ext.ux.Toast.msg('OK !', result.msg);
				application.layout.storeUtilisateurs.reload();
				if(Ext.getCmp('grid-user-droits-gauche')){Ext.getCmp('grid-user-droits-gauche').getStore().reload();}
                if(Ext.getCmp('grid-user-groupes-gauche')){Ext.getCmp('grid-user-groupes-gauche').getStore().reload();}
				Ext.getCmp('champ_action-utilisateur').setValue("update");
				Ext.getCmp('champ-id_role').setValue(result.id_role);
				Ext.getCmp('champ_id_initial-utilisateur').setValue(result.id_role);
                Ext.getCmp('formutilisateurs').setTitle('Modification de l\'utilisateur '+Ext.getCmp('formutilisateurs').getForm().findField('prenom_role').getValue()+ ' ' +Ext.getCmp('formutilisateurs').getForm().findField('nom_role').getValue());
				bouton.setText('Enregistrer');
				Ext.getCmp('label-pass').setText('');
			}
			,failure: function(form, action) {
				Ext.getCmp('utilisateurSaveButton').setText('Enregistrer');
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
