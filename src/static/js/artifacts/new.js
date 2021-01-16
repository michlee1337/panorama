
$( document ).ready(function() {
  new Taggle('prereqs-taggle', {
    duplicateTagClass: 'bounce',
    hiddenInputName: 'prereqs[]',
  });

});
// ______ UPDATE NESTED FORM _____

var chunk_card_template = `<div class="artifacts-creator_chunk card">
    <div class="form-group">
      <h4>
        <input type="text" name="chunk_titles[]" placeholder="Title">
      </h4>
      <h3>
        <input type="text" name="chunk_concepts[]" placeholder="concept"></h4>
      </h3>
    </div>
    <div class="form-group">
      <input type="textarea" rows="15" name="chunk_contents[]" placeholder="Type content here">
    </div>

  </div>`;

function addChunk() {
  $("#artifacts-creator_wrapper").append(chunk_card_template);
}
