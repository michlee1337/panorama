// ______ STUDYPLAN CREATOR INTERNAL STATE ______
let chunk_names = [],
  chunk_descriptions = [],
  chunk_contents = [],
  chunk_concepts = [],
  prereqs = ['enter as tags'],
  chunk_idx = 0;

$( document ).ready(function() {
  // ______ HIDDEN INPUTS ______
  let hiddenInput_prereqs = document.getElementById('hiddenInput_prereqs'),
  hiddenInput_chunk_names = document.getElementById('hiddenInput_chunk_names'),
  hiddenInput_chunk_descriptions = document.getElementById('hiddenInput_chunk_descriptions'),
  hiddenInput_chunk_contents = document.getElementById('hiddenInput_chunk_contents');
  hiddenInput_chunk_concepts = document.getElementById('hiddenInput_chunk_concepts');

  new Taggle('prereqs-taggle', {
    tags: prereqs,
    duplicateTagClass: 'bounce',
    hiddenInputName: 'prereqs[]',
  });

});
// ______ UPDATE NESTED FORM _____

// DEV: There is probably a better way to template dynamically
var chunk_card_template = `<div class="artifacts-creator_chunk card">
    <div class="form-group">
      <h4>
        <input type="text" onChange="UpdateChunk(%CHUNK_IDX%, this.value)" placeholder="Title">
      </h4>
      <h3>
        <input type="text" onChange="UpdateChunkConcept(%CHUNK_IDX%, this.value)" placeholder="concept"></h4>
      </h3>
    </div>
    <div class="form-group">
      <input type="textarea" onChange="UpdateChunkDescription(%CHUNK_IDX%, this.value)" placeholder="description">
    </div>
    <div class="form-group">
      <input type="textarea" rows="15" onChange="UpdateChunkContent(%CHUNK_IDX%, this.value)" placeholder="Type content here">
    </div>

  </div>`;

function addChunk() {
  var chunk_card = chunk_card_template;
  chunk_card = chunk_card_template.replaceAll("%CHUNK_IDX%", chunk_idx);
  $("#artifacts-creator_wrapper").append(chunk_card);
  chunk_idx += 1;
  chunk_names.push(null);
  chunk_descriptions.push(null);
  chunk_contents.push(null);
  console.log(chunk_names, chunk_descriptions, chunk_contents);
}

// ______ UPDATE HIDDEN FIELDS _____
function UpdateChunk(chunk_idx, chunk_name) {
  chunk_names[chunk_idx] = chunk_name;
}

function UpdateChunkConcept(chunk_idx, chunk_concept) {
  chunk_concepts[chunk_idx] = chunk_concept;
}


function UpdateChunkDescription(chunk_idx, chunk_description) {
  chunk_descriptions[chunk_idx] = chunk_description;
}

function UpdateChunkContent(chunk_idx, chunk_content) {
  chunk_contents[chunk_idx] = chunk_content;
}

function SubmitHiddenInputs() {
    hiddenInput_prereqs.value = prereqs.join(',');
    hiddenInput_chunk_names.value = chunk_names.join(',');
    hiddenInput_chunk_descriptions.value = chunk_descriptions.join(',');
    hiddenInput_chunk_contents.value = chunk_contents.join(',');
    hiddenInput_chunk_concepts.value = chunk_concepts.join(',');
    return True;
}
