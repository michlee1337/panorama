// _____ RENDER SEARCH SIDEBAR_____

$(document).ready(function () {
  $('#sidebarCollapse').on('click', function () {
      $('#search-sidebar').toggleClass('active');
  });

});

function searchRelated(concept_id, concept_title) {
  // open the search sidebar if closed
  if (!$('#search-sidebar.active').length) {
    $('#search-sidebar').toggleClass('active');
  }

  // update introduction
  $("#search-sidebar-title").html(`Related to ${concept_title}`);

  // empty current search contents and add search result divs
  $("#search-sidebar-content").empty();

  search_sidebar_studyplans = document.createElement('div');
  search_sidebar_studyplans.setAttribute("id", "search-sidebar-studyplans");
  $("#search-sidebar-content").append(search_sidebar_studyplans);

  search_sidebar_readings = document.createElement('div');
  search_sidebar_readings.setAttribute("id", "search-sidebar-readings");
  $("#search-sidebar-content").append(search_sidebar_readings);

  // render studyplans
  renderStudyplans(concept_id);

  // render readings
  renderReadings(concept_id);
}

function renderStudyplans(concept_id) {
  // query for studyplans and call appropriate render
  $.ajax({
    type: 'GET',
    url: "/studyplans/concept",
    data: {
      concept_id: concept_id,
      cur_studyplan_id: studyplan_id
    },
    dataType: "json",
    success: function(data){
      $("#search-sidebar-studyplans").append(`
        <h5>Studyplans</h5>
      `);
     if (data.studyplans === undefined || data.studyplans.length == 0) {
       $("#search-sidebar-studyplans").append(noresultsCard());
     }
     else {
       for (var i = 0; i < data.studyplans.length; i++) {
         renderStudyplanCard(data.studyplans[i]);
       }
     }
   }
  });
}

function renderReadings(concept_id) {
  // query for readings and call appropriate render
  console.log("rendering")
  $.ajax({
    type: 'GET',
    url: "/readings/concept",
    data: {
      concept_id: concept_id,
    },
    dataType: "json",
    success: function(data){
      $("#search-sidebar-readings").append(`
        <h5>Readings</h5>
      `);
       if (data.readings === undefined || data.readings.length == 0) {
         $("#search-sidebar-readings").append(noresultsCard());
       }
       else {
         for (var i = 0; i < data.readings.length; i++) {
           renderReadingCard(data.readings[i]);
         }
       }
     }
  });
}

function noresultsCard() {
  return(`
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">No results found :(</h5>
      </div>
    </div>
  `);
}

function renderStudyplanCard(studyplan) {
  $("#search-sidebar-studyplans").append(`
    <a href="/studyplans/${studyplan.id}">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${studyplan.title}</h5>
          <p>${studyplan.description}</p>
        </div>
      </div>
    </a>
  `);
}

function renderReadingCard(reading) {
  $("#search-sidebar-readings").append(`
    <a href="${reading.link}" target="_blank"">
      <div class="card reading_card">
        <div class="card-body">
          ${reading.name}
          <p>${reading.description}</p>
        </div>
      </div>
    </a>
  `);
}
