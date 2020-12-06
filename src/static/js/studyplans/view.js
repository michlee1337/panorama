$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#search-sidebar').toggleClass('active');
        renderStudyplanSearch(studyplan_concept_id);
    });

});

function updateSearchSidebar(search_type) {
  var search_type_lookup = {
    "search-studyplan": 1,
    "search-resource": 2,
    "search-relationships": 3
  }
  switch (search_type_lookup[search_type]) {
    case 1:
      console.log("studyplan", concept_ids );
      //renderStudyplanSearch();
      break;
    case 2:
      console.log("resource");
      break;
    case 3:
      console.log("rel");
      break;
    default:
      console.log("error");
  }
}

function renderStudyplanSearch(concept_id) {
  $.ajax({
    type: 'GET',
    url: "/studyplans_by_concept",
    data: {
      concept_id: concept_id,
      cur_studyplan_id: studyplan_id
    },
    dataType: "json",
    success: function(data){
               if (data.studyplans === undefined || data.studyplans.length == 0) {
                 renderNoResults()
               }
               else {
                 for (var i = 0; i < data.studyplans.length; i++) {
                   renderStudyplanCard(data.studyplans[i]);
                 }
               }
             }
  });
}

function renderNoResults() {
  $("#search-sidebar-content").empty().append(`
    <div class="card">
      <h5 class="card-title">No results found :(</h5>
    </div>
  `);
}

function renderStudyplanCard(studyplan) {
  $("#search-sidebar-content").html(`
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
// var week = 2;
// // append child for a week
// function addWeek() {
//   $("#studyplans-creator_wrapper").append(`<div class="studyplans-creator_week">
//     <h4> Week ${week}</h4>
//     <div class="studyplans-creator_week_resources card" ondrop="drop(event)" ondragover="allowDrop(event)">
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
//     $(resource).attr("class", "studyplan_creator_week_resources_card btn-success");
//     ev.target.appendChild(resource);
//   }
// }
