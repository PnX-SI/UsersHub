Ext.QuickTips.init();
// reference local blank image
Ext.BLANK_IMAGE_URL = 'js/ext-3.2.0/resources/images/default/s.gif';

Ext.namespace("application");

application = function() {
    return { 
		user:{
			prenom: null
			,nom:null
			,droits:null
			,id_user:null
		}
        ,init: function() { 
			Ext.Ajax.request({
                url: 'get_user.php'
				,method: 'GET'
                ,success: function(request) {
                    this.user = Ext.decode(request.responseText);
                    // initialisation du layout après récupération des paramètres utilisateurs
                    application.layout.init();
                }
                ,failure: function() {
                    alert("pas bon ça");
                }
                ,scope: this
                ,synchronous: true
            });

			//store des groupes 
			this.storeGroupes = new Ext.data.JsonStore({
				url: 'get_groupes.php'
				,method: 'GET'
				,fields: ['id_groupe', 'nom_groupe', 'desc_groupe']
				,sortInfo: {field: 'nom_groupe',direction: 'ASC'}
				,autoLoad:true
			});
			//store des applications 
			this.storeApplications = new Ext.data.JsonStore({
				url: 'get_applications.php'
				,method: 'GET'
				,fields: ['id_application', 'nom_application', 'desc_application']
				,sortInfo: {field: 'nom_application',direction: 'ASC'}
				,autoLoad:true
			});
            //store des droits 
			this.storeDroits = new Ext.data.JsonStore({
				url: 'get_droits.php'
				,method: 'GET'
				,fields: ['id_droit', 'nom_droit', 'desc_droit']
				,sortInfo: {field: 'id_droit',direction: 'ASC'}
				,autoLoad:true
			});
            //store des organismes 
			this.storeOrganismes = new Ext.data.JsonStore({
				url: 'get_organismes.php'
				,method: 'GET'
				,fields: ['id_organisme', 'nom_organisme', 'adresse_organisme', 'cp_organisme', 'ville_organisme', 'tel_organisme', 'fax_organisme', 'mail_organisme']
				,sortInfo: {field: 'nom_organisme',direction: 'ASC'}
				,autoLoad:true
			});
            //store des unites 
			this.storeUnites = new Ext.data.JsonStore({
				url: 'get_unites.php'
				,method: 'GET'
				,fields: ['id_unite', 'nom_unite', 'adresse_unite', 'cp_unite', 'ville_unite', 'tel_unite', 'fax_unite', 'mail_unite']
				,sortInfo: {field: 'nom_unite',direction: 'ASC'}
				,autoLoad:true
			});
			//store des menus 
			this.storeMenus = new Ext.data.JsonStore({
				url: 'get_menus.php'
				,method: 'GET'
				,fields: ['id_menu', 'nom_menu', 'desc_menu', 'id_application']
				,sortInfo: {field: 'id_menu',direction: 'ASC'}
				,autoLoad:true
			});
        }
        //RAZ formulaire et mise en  place d'un comportement d'ajout
        ,resetFormUtilisateur: function(){
            Ext.getCmp('formutilisateurs').setTitle('Ajout d\'un nouvel utilisateur');
            Ext.getCmp('formutilisateurs').getForm().reset();
            Ext.getCmp('champ_action-utilisateur').setValue("insert");
            Ext.getCmp('label-pass').setText('');
            Ext.getCmp('champ_id_initial-utilisateur').setValue(null);//conserver l'id initialement charger dans le formulaire pour la bouton annuler
        }
    
    } 
}();

	Ext.onReady(function(){
		application.init();
	});


// les actions sont dans le fichiers actions.js
