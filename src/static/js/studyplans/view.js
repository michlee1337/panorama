$(document).ready(function () {
    $('#sidebarCollapse').on('click', function () {
        $('#search-sidebar').toggleClass('active');
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
      console.log("studyplan");
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

function renderStudyplanSearch() {
  // $.ajax({
  //   type: 'POST',
  //   url: "/_delete_student",
  //   data: {student_id: 1},
  //   dataType: "text",
  //   success: function(data){
  //              alert("Deleted Student ID "+ student_id.toString());
  //            }
  // });

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
