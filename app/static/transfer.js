var tab_add = [];
var tab_del = [];
var data_select = [];
var profil = [];

function fill_select() {
  td_profil =
    '<td class = "profil"><select class="custom-select", id="inputGroupSelect02">';
  for (var i = 0; i < data_select.length; i++) {
    td_profil =
      td_profil +
      '<option value="' +
      data_select[i]["id_profil"] +
      '">' +
      data_select[i]["nom_profil"] +
      "</option>";
  }
  td_profil = td_profil + "</select></td>";
  return td_profil;
}

function addTab(tab, table) {
  for (var i = 0; i < tab.length; i++) {
    table.append(tab[i]);
  }
}

var add = function(app) {
  var tab = [];
  i = 0;
  $('#user input[type="checkbox"]:checked').each(function() {
    if (app != null) {
      var Row = $(this)
        .parents("tr")
        .append(fill_select());
    } else {
      var Row = $(this)
        .parents("tr")
        .append();
    }
    tab.push(Row[0]);
    $("#user")
      .find("input[type=checkbox]:checked")
      .prop("checked", false);
    var ID = $(this)
      .parents("tr")
      .find("td:eq(1)")
      .html();
    tab_add.push(ID);

    if (isInTabb(tab_del, ID) == true) {
      tab_del.splice(tab_del.indexOf(ID), 1);
      tab_add.splice(tab_add.indexOf(ID), 1);
    }
  });
  var table = $("#adding_table");
  addTab(tab, table);
};

var del = function(app) {
  var tab = [];
  $('#adding_table input[type="checkbox"]:checked').each(function() {
    var Row = $(this).parents("tr");
    var ID = $(this)
      .parents("tr")
      .find("td:eq(1)")
      .html();
    var PROFIL = $(this)
      .parents("tr")
      .find("option:selected")
      .val();
    if (app != null) {
      profil.push({ id_role: ID, id_profil: PROFIL });
      Row.find(".profil").remove();
    }
    var Row = $(this).parents("tr");
    tab.push(Row[0]);
    $("#adding_table")
      .find("input[type=checkbox]:checked")
      .prop("checked", false);
    tab_del.push(ID);
    if (isInTabb(tab_add, ID) == true) {
      tab_add.splice(tab_add.indexOf(ID), 1);
      tab_del.splice(tab_del.indexOf(ID), 1);
    }
  });
  var table = $("#user");
  addTab(tab, table);
};

var get_profil = function(data) {
  var tab = [];
  data_id = data["tab_add"];
  $("#adding_table tr").each(function() {
    var ID = $(this)
      .find("td:eq(1)")
      .html();
    var PROFIL = $(this)
      .find("option:selected")
      .val();
    for (d in data_id) {
      if (ID == data_id[d]) {
        tab.push({ id_role: ID, id_profil: PROFIL });
      }
      //tab.push({ id_role: ID, id_profil: PROFIL });
    }
  });
  return tab;
};

var get_profil_delete = function(data) {
  for (r in profil) {
    if (isInTabb(data["tab_del"], r["id_role"]) == true) {
      profil.splice(profil.indexOf(r), 1);
    }
  }
};

// TODO: pourquoi faire une requeste AJAX pour ce post ?
// est-ce qu'on pourrait pas utiliser un formulaire simple ?
var update_right = function() {
  var data = {};
  data["tab_add"] = tab_add;
  data["tab_del"] = tab_del;
  data["tab_add"] = get_profil(data);
  get_profil_delete(data);
  data["tab_del"] = profil;
  $.ajax({
    url: $(location).attr("href"),
    type: "post",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json"
  })
    .done(function(data) {
      //window.location.href = data.redirect;
    })
    .fail(function(data) {
      alert("Une erreur c'est produite");
    });

  tab_add = [];
  tab_del = [];
  tab_profil = [];
};

var update = function() {
  var data = {};
  data["tab_add"] = tab_add;
  data["tab_del"] = tab_del;

  $.ajax({
    url: $(location).attr("href"),
    type: "post",
    data: JSON.stringify(data),
    contentType: "application/json; charset=utf-8",
    dataType: "json"
  })
    .done(function(data) {
      window.location.href = data.redirect;
    })
    .fail(function(data) {
      console.log(data);
      alert("Une erreur s'est produite");
    });

  tab_add = [];
  tab_del = [];
};

function isInTabb(tab, id) {
  var bool = false;
  tab.forEach(element => {
    if (element == id) {
      bool = true;
    }
  });
  return bool;
}

var deleteRaw = function(path) {
  var c = confirm("Etes vous sur de vouloir supprimer cet élement ? ");
  if (c == true) window.location.href = path;
};

// MAIN executed

// get the app profils
// TODO: ne devrait être déclenché que quand on en a besoin
// parse the url to get the id_application
var current_url = window.location.href;
url_array = current_url.split("/");
if (
  url_array.indexOf("application") != -1 &&
  url_array.indexOf("rights") != -1
) {
  id_application = url_array[url_array.length - 1];
  console.log(id_application);
  $.ajax({
    url: url_app + "/api/profils?id_application=" + id_application,
    type: "get",
    data: JSON.stringify(data_select),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
      data_select = response;
    },
    error: function(error) {}
  });
}

$(document).ready(function() {
  var tab_add = [];
  var tab_del = [];
  var data_select = {};

  // init the left table
  $("#user").DataTable({
    language: {
      lengthMenu: "Afficher _MENU_ éléments par page",
      zeroRecords: "Aucune donnée",
      info: "Affiche la page _PAGE_ sur _PAGES_",
      infoEmpty: "Aucune donnée",
      infoFiltered: "(filtrer sur _MAX_ total d'éléments)",
      search: "Recherche:",
      paginate: {
        first: "Première",
        last: "Dernière",
        next: "Suivante",
        previous: "Précédente"
      },
      aLengthMenu: [[10, 25, 50, 75, -1], [10, 25, 50, 75, "All"]],
      iDisplayLength: 25
    }
  });

  // init the right table
  $("#adding_table").DataTable({
    language: {
      lengthMenu: "Afficher _MENU_ éléments par page",
      zeroRecords: "Aucune donnée",
      info: "Affiche la page _PAGE_ sur _PAGES_",
      infoEmpty: "Aucune donnée",
      infoFiltered: "(filtrer sur _MAX_ total d'éléments)",
      search: "Recherche:",
      paginate: {
        first: "Première",
        last: "Dernière",
        next: "Suivante",
        previous: "Précédente"
      },
      aLengthMenu: [[10, 25, 50, 75, -1], [10, 25, 50, 75, "All"]],
      iDisplayLength: 25
    }
  });

  // init table from table_database.html
  $("#tri").DataTable({
    language: {
      lengthMenu: "Afficher _MENU_ éléments par page",
      zeroRecords: "Aucune donnée",
      info: "Affiche la page _PAGE_ sur _PAGES_",
      infoEmpty: "Aucune donnée",
      infoFiltered: "(filtrer sur _MAX_ total d'éléments)",
      search: "Recherche:",
      paginate: {
        first: "Première",
        last: "Dernière",
        next: "Suivante",
        previous: "Précédente"
      },
      aLengthMenu: [[10, 25, 50, 75, -1], [10, 25, 50, 75, "All"]],
      iDisplayLength: 25
    },
    aaSorting: []
  });

  // end main
});
