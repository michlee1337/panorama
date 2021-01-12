// ______ STUDYPLAN CREATOR INTERNAL STATE ______
let chunk_names = [],
  chunk_descriptions = [],
  chunk_contents = [],
  prereqs = [],
  chunk_idx = 0;

$( document ).ready(function() {
  // ______ HIDDEN INPUTS ______
  let hiddenInput_prereqs = document.getElementById('hiddenInput_prereqs'),
  hiddenInput_chunk_names = document.getElementById('hiddenInput_chunk_names'),
  hiddenInput_chunk_descriptions = document.getElementById('hiddenInput_chunk_descriptions'),
  hiddenInput_chunk_contents = document.getElementById('hiddenInput_chunk_contents');


  // ______ PREREQUISITE DYNAMIC RENDER ____
  let mainInput = document.createElement('input');
  var prereqs_input_div = document.getElementById('prereqs-input');

  mainInput.setAttribute('type', 'text');
  mainInput.classList.add('main-input');
  mainInput.addEventListener('input', function () {
      let enteredPrereqs = mainInput.value.split(',');
      if (enteredPrereqs.length > 1) {
          enteredPrereqs.forEach(function (t) {
              let filteredTag = filterTag(t);
              if (filteredTag.length > 0)
                  addTag(filteredTag);
          });
          mainInput.value = '';
      }
  });

  mainInput.addEventListener('keydown', function (e) {
      let keyCode = e.which || e.keyCode;
      if (keyCode === 8 && mainInput.value.length === 0 && prereqs.length > 0) {
          removeTag(prereqs.length - 1);
      }
  });

  prereqs_input_div.appendChild(mainInput);

  addTag('hello!');

  function addTag (text) {
      let prereq = {
          text: text,
          element: document.createElement('span'),
      };

      prereq.element.classList.add('prereq');
      prereq.element.textContent = prereq.text;

      let closeBtn = document.createElement('span');
      closeBtn.classList.add('close');
      closeBtn.addEventListener('click', function () {
          removeTag(prereqs.indexOf(prereq));
      });
      prereq.element.appendChild(closeBtn);

      prereqs.push(prereq);

      prereqs_input_div.insertBefore(prereq.element, mainInput);

      refreshPrereqs();
  }

  function removeTag (index) {
      let prereq = prereqs[index];
      prereqs.splice(index, 1);
      prereqs_input_div.removeChild(prereq.element);
      refreshPrereqs();
  }

  function refreshPrereqs () {
      let prereqsList = [];
      prereqs.forEach(function (t) {
          prereqsList.push(t.text);
      });
      hiddenInput_prereqs.value = prereqsList.join(',');
  }

  function filterTag (prereq) {
          return prereq.replace(/[^\w -]/g, '').trim().replace(/\W+/g, '-');
      }
  // ______ PREREQUISITES DYNAMIC RENDER END _____
});


// ______ MULTIPLE TAG INPUT _____

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
  chunk_card = chunk_card_template.replace(/%CHUNK_IDX%/, chunk_idx);
  $("#artifacts-creator_wrapper").append(chunk_card);
  chunk_idx += 1;
  chunk_names.push(null);
  hiddenInput_chunk_names.value = chunk_names.join(',');
}

// ______ UPDATE HIDDEN FIELDS _____
function UpdateChunk(chunk_idx, chunk_name) {
  chunk_names[chunk_idx] = chunk_name;
  hiddenInput_chunk_names.value = chunk_names.join(',');
}

function UpdateChunkDescription(chunk_idx, chunk_description) {
  chunk_descriptions[chunk_idx] = chunk_description;
  hiddenInput_chunk_descriptions.value = chunk_descriptions.join(',');
}

function UpdateChunkContent(chunk_idx, chunk_content) {
  reading_names[reading_idx] = reading_name;
  hiddenInput_reading_names.value = reading_names.join(',');
}
