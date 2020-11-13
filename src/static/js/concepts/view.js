$(document).ready(function () {

    $('#sidebarCollapse').on('click', function () {
        $('#studyplan_creator').toggleClass('active');
    });

});

// append child for a week
function addWeek() {
  console.log('yo');
}

// // append child for a resource
function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("resource_id", ev.target.id);
  ev.dataTransfer.setData("resource_name", ev.target.text);
  console.log("dragging")
  console.log(ev.dataTransfer.getData("resource_id"));
  console.log(ev.dataTransfer.getData("resource_name"));
}

function drop(ev) {
  ev.preventDefault();
  var resource_id = ev.dataTransfer.getData("resource_id");
  var resource_name = ev.dataTransfer.getData("resource_name");
  var resource = document.createElement('div'); // is a node
  if (resource_name != "undefined") {
    $(resource).attr("id", resource_id);
    $(resource).text(resource_name);
    $(resource).attr("class", "studyplan_creator_week_resources_card btn-success");
    ev.target.appendChild(resource);
  }
}
