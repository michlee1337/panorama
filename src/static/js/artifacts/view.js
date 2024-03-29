// _____ RENDER SEARCH SIDEBAR_____

$(document).ready(function () {
  $('#sidebarCollapse').on('click', function () {
      $('#search-sidebar').toggleClass('active');
      $('#related-tabs').toggleClass('active');
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

  search_sidebar_artifacts = document.createElement('div');
  search_sidebar_artifacts.setAttribute("id", "search-sidebar-artifacts");
  $("#search-sidebar-content").append(search_sidebar_artifacts);

  // render artifacts
  renderArtifacts(concept_id);
}

function renderArtifacts(concept_id) {
  // query for artifacts and call appropriate render
  $.ajax({
    type: 'GET',
    url: "/artifacts/by_concept",
    data: {
      concept_id: concept_id,
      exclude_id: artifact_id
    },
    dataType: "json",
    success: function(data){
      $("#search-sidebar-artifacts").append(`
        <h5>Artifacts</h5>
      `);
     if (data.artifacts === undefined || data.artifacts.length == 0) {
       $("#search-sidebar-artifacts").append(noresultsCard());
     }
     else {
       for (var i = 0; i < data.artifacts.length; i++) {
         renderArtifactCard(data.artifacts[i]);
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

function renderArtifactCard(artifact) {
  $("#search-sidebar-artifacts").append(`
    <a href="/artifacts/${artifact.id}">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">${artifact.title}</h5>
          <p>${artifact.description}</p>
          <p>${artifact.chunks}</p>
        </div>
      </div>
    </a>
  `);
}
