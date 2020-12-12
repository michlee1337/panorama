// ______ RESOURCE SEARCH TOGGLE _____
$( document ).ready(function() {
  drowndown_btn = document.getElementById("dropdownMenuButton");
  drowndown_btn.addEventListener ("click", toggleFilter);
});

function toggleFilter() {
  search_filter = document.getElementById('search-filter');
  if (search_filter.style.display == "block") {
    search_filter.style.display = "none";
    $("#search-term-input").attr("placeholder","search studyplans")
  } else {
    search_filter.style.display = "block";
    $("#search-term-input").attr("placeholder","search readings")
  }
}
