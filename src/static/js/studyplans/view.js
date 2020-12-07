$(document).ready(function () {
  $('#sidebarCollapse').on('click', function () {
      $('#search-sidebar').toggleClass('active');
  });

});

// _____ RENDER SEARCH SIDEBAR_____

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

// var week = 2;
// // append child for a week
// function addWeek() {
//   $("#studyplans-creator_wrapper").append(`<div class="studyplans-creator_week">
//     <h4> Week ${week}</h4>
//     <div class="studyplans-creator_week_readings card" ondrop="drop(event)" ondragover="allowDrop(event)">
//     </div>
//   </div>`);
//   week += 1;
// }
//
// // // append child for a resource
// function allowDrop(ev) {
//   ev.preventDefault();
// }
//
// function drag(ev) {
//   ev.dataTransfer.setData("resource_id", ev.target.id);
//   ev.dataTransfer.setData("resource_name", ev.target.text);
//   console.log("dragging")
//   console.log(ev.dataTransfer.getData("resource_id"));
//   console.log(ev.dataTransfer.getData("resource_name"));
// }
//
// function drop(ev) {
//   ev.preventDefault();
//   var resource_id = ev.dataTransfer.getData("resource_id");
//   var resource_name = ev.dataTransfer.getData("resource_name");
//   var resource = document.createElement('div'); // is a node
//   if (resource_name != "undefined") {
//     $(resource).attr("id", resource_id);
//     $(resource).text(resource_name);
//     $(resource).attr("class", "studyplan_creator_week_readings_card btn-success");
//     ev.target.appendChild(resource);
//   }
// }
