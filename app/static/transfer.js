var tab_add = [];
var tab_del = [];
var data_select = [];
var profil = [];
var membershipTables = {
  enabled: false,
  available: null,
  selected: null,
  ajaxUrl: null
};

function getDataTableLanguage() {
  return {
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
    }
  };
}

function getDataTableLengthMenu() {
  return [[10, 25, 50, 75, -1], [10, 25, 50, 75, "All"]];
}

function fill_select() {
  var td_profil =
    '<td class = "profil"><select class="custom-select" id="inputGroupSelect02">';
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

function isMembershipMode() {
  return membershipTables.enabled;
}

function normalizeId(value) {
  return String(value);
}

function reloadMembershipTables() {
  if (!isMembershipMode()) {
    return;
  }
  membershipTables.available.ajax.reload(null, false);
  membershipTables.selected.ajax.reload(null, false);
}

function getMembershipCheckedIds(tableSelector) {
  if (!isMembershipMode()) {
    return [];
  }
  var dataTable = $(tableSelector).DataTable();
  var ids = [];
  $(tableSelector + " tbody input.membership-check:checked").each(function() {
    var rowData = dataTable.row($(this).closest("tr")).data();
    if (rowData && rowData.id_role != null) {
      ids.push(normalizeId(rowData.id_role));
    }
  });
  return ids;
}

var add = function(app) {
  if (isMembershipMode()) {
    var idsToAdd = getMembershipCheckedIds("#user");
    idsToAdd.forEach(function(id) {
      if (!isInTabb(tab_add, id)) {
        tab_add.push(id);
      }
      if (isInTabb(tab_del, id)) {
        tab_del.splice(tab_del.indexOf(id), 1);
      }
    });
    reloadMembershipTables();
    return;
  }

  var tab = [];
  $('#user input[type="checkbox"]:checked').each(function() {
    var row;
    if (app != null) {
      row = $(this)
        .parents("tr")
        .append(fill_select());
    } else {
      row = $(this)
        .parents("tr")
        .append();
    }
    tab.push(row[0]);
    $("#user")
      .find("input[type=checkbox]:checked")
      .prop("checked", false);
    var id = $(this)
      .parents("tr")
      .find("td:eq(1)")
      .html();
    tab_add.push(id);

    if (isInTabb(tab_del, id) === true) {
      tab_del.splice(tab_del.indexOf(id), 1);
      tab_add.splice(tab_add.indexOf(id), 1);
    }
  });
  addTab(tab, $("#adding_table"));
};

var del = function(app) {
  if (isMembershipMode()) {
    var idsToRemove = getMembershipCheckedIds("#adding_table");
    idsToRemove.forEach(function(id) {
      if (!isInTabb(tab_del, id)) {
        tab_del.push(id);
      }
      if (isInTabb(tab_add, id)) {
        tab_add.splice(tab_add.indexOf(id), 1);
      }
    });
    reloadMembershipTables();
    return;
  }

  var tab = [];
  $('#adding_table input[type="checkbox"]:checked').each(function() {
    var row = $(this).parents("tr");
    var id = row.find("td:eq(1)").html();
    var currentProfil = row.find("option:selected").val();
    if (app != null) {
      profil.push({ id_role: id, id_profil: currentProfil });
      row.find(".profil").remove();
    }
    tab.push(row[0]);
    $("#adding_table")
      .find("input[type=checkbox]:checked")
      .prop("checked", false);
    tab_del.push(id);
    if (isInTabb(tab_add, id) === true) {
      tab_add.splice(tab_add.indexOf(id), 1);
      tab_del.splice(tab_del.indexOf(id), 1);
    }
  });
  addTab(tab, $("#user"));
};

var get_profil = function(data) {
  var tab = [];
  var data_id = data["tab_add"];
  $("#adding_table tr").each(function() {
    var id = $(this)
      .find("td:eq(1)")
      .html();
    var currentProfil = $(this)
      .find("option:selected")
      .val();
    for (var d in data_id) {
      if (id == data_id[d]) {
        tab.push({ id_role: id, id_profil: currentProfil });
      }
    }
  });
  return tab;
};

var get_profil_delete = function(data) {
  for (var i = profil.length - 1; i >= 0; i--) {
    if (isInTabb(data["tab_del"], profil[i]["id_role"]) === true) {
      profil.splice(i, 1);
    }
  }
};

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
    .done(function() {})
    .fail(function() {
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
  var normalized = normalizeId(id);
  var bool = false;
  tab.forEach(function(element) {
    if (normalizeId(element) === normalized) {
      bool = true;
    }
  });
  return bool;
}

function moveExtraFiltersNearSearch(tableId) {
  var filterContainer = $("#" + tableId + "_filter");
  var extraFiltersContainer = $(".datatable-extra-filters");
  if (!filterContainer.length || !extraFiltersContainer.length) {
    return;
  }

  extraFiltersContainer
    .removeClass("form-row align-items-end mb-3")
    .addClass("d-inline-flex align-items-center flex-wrap mr-3 mb-0");

  extraFiltersContainer.find(".datatable-extra-filter-group").each(function() {
    $(this)
      .removeClass("col-auto")
      .addClass("d-inline-flex align-items-center mr-3 mb-0");
    $(this)
      .find("label")
      .removeClass("mb-1")
      .addClass("mb-0 mr-2");
  });

  extraFiltersContainer.find(".datatable-extra-filter").addClass("custom-select-sm");
  filterContainer.css({
    display: "flex",
    alignItems: "center",
    justifyContent: "flex-end",
    gap: "0.75rem",
    flexWrap: "wrap"
  });
  filterContainer.prepend(extraFiltersContainer);
}

function buildTableDatabaseOptions(triTable) {
  var extraFilters = $(".datatable-extra-filter");
  var triOptions = {
    language: getDataTableLanguage(),
    lengthMenu: getDataTableLengthMenu(),
    pageLength: 25,
    aaSorting: []
  };

  if (triTable.data("server-side")) {
    triOptions.processing = true;
    triOptions.serverSide = true;
    triOptions.searchDelay = 300;
    triOptions.deferRender = true;
    triOptions.ajax = {
      url: triTable.attr("data-ajax-url"),
      type: "GET",
      data: function(requestData) {
        extraFilters.each(function() {
          var filter = $(this);
          requestData[filter.data("param")] = filter.val();
        });
      }
    };
    triOptions.order = JSON.parse(
      triTable.attr("data-order") || "[[1, \"asc\"]]"
    );
    triOptions.pageLength = parseInt(
      triTable.attr("data-page-length") || "25",
      10
    );
    triOptions.columns = JSON.parse(
      triTable.attr("data-columns") || "[]"
    ).map(function(column) {
      var normalized = $.extend({}, column);
      if (normalized.data.indexOf("action_") !== 0) {
        normalized.render = $.fn.dataTable.render.text();
      }
      return normalized;
    });
  }

  return triOptions;
}

function buildMembershipColumns(tableElement) {
  return JSON.parse(tableElement.attr("data-membership-columns") || "[]").map(
    function(column) {
      var normalized = $.extend({}, column);
      if (normalized.data === "select") {
        normalized.render = function(data) {
          return data;
        };
      } else {
        normalized.render = $.fn.dataTable.render.text();
      }
      return normalized;
    }
  );
}

function getMembershipPanel(tableElement) {
  return tableElement.attr("data-membership-panel") || "available";
}

function buildMembershipTableOptions(tableElement) {
  return {
    processing: true,
    serverSide: true,
    searchDelay: 250,
    deferRender: true,
    pageLength: 25,
    order: [[2, "asc"]],
    language: getDataTableLanguage(),
    lengthMenu: getDataTableLengthMenu(),
    ajax: {
      url: membershipTables.ajaxUrl,
      type: "GET",
      data: function(requestData) {
        requestData.panel = getMembershipPanel(tableElement);
        requestData.pending_add = JSON.stringify(tab_add);
        requestData.pending_del = JSON.stringify(tab_del);
      }
    },
    columns: buildMembershipColumns(tableElement),
    createdRow: function(row, data) {
      if (data.groupe === "True") {
        $(row).find("td").not(":first").addClass("table-primary");
      }
    }
  };
}

function initMembershipTables() {
  var manager = $("#membership-manager");
  if (!manager.length || manager.attr("data-membership-mode") !== "true") {
    return;
  }

  membershipTables.enabled = true;
  membershipTables.ajaxUrl = manager.attr("data-ajax-url");
  membershipTables.available = $("#user").DataTable(
    buildMembershipTableOptions($("#user"))
  );
  membershipTables.selected = $("#adding_table").DataTable(
    buildMembershipTableOptions($("#adding_table"))
  );
}

var deleteRaw = function(path) {
  var c = confirm("Etes vous sur de vouloir supprimer cet élément ? ");
  if (c === true) {
    window.location.href = path;
  }
};

var current_url = window.location.href;
var url_array = current_url.split("/");
if (
  url_array.indexOf("application") != -1 &&
  url_array.indexOf("rights") != -1
) {
  var id_application = url_array[url_array.length - 1];
  $.ajax({
    url: url_app + "/api/profils?id_application=" + id_application,
    type: "get",
    data: JSON.stringify(data_select),
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(response) {
      data_select = response;
    },
    error: function() {}
  });
}

$(document).ready(function() {
  initMembershipTables();

  if (!isMembershipMode()) {
    if ($("#user").length) {
      $("#user").DataTable({
        language: getDataTableLanguage(),
        lengthMenu: getDataTableLengthMenu(),
        pageLength: 25
      });
    }

    if ($("#adding_table").length) {
      $("#adding_table").DataTable({
        language: getDataTableLanguage(),
        lengthMenu: getDataTableLengthMenu(),
        pageLength: 25
      });
    }
  }

  var triTable = $("#tri");
  if (triTable.length) {
    var triDataTable = triTable.DataTable(buildTableDatabaseOptions(triTable));
    moveExtraFiltersNearSearch(triTable.attr("id"));
    $(".datatable-extra-filter").on("change", function() {
      triDataTable.ajax.reload();
    });
  }
});
