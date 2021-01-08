// ______ STUDYPLAN CREATOR INTERNAL STATE ______
let chunks = [],
  chunk_descriptions = [],
  readings_to_chunk_idx = [],   // DEV: maybe post-calc this
  reading_names = [],
  reading_links = [],
  reading_descriptions = [],
  reading_depths = [],
  reading_times = [],
  reading_types = [],
  prereqs = [],
  chunk_idx = 0,
  reading_idx = 0;

$( document ).ready(function() {
  // ______ HIDDEN INPUTS ______
  let hiddenInput_prereqs = document.getElementById('hiddenInput_prereqs'),
  hiddenInput_chunks = document.getElementById('hiddenInput_chunks'),
  hiddenInput_chunk_descriptions = document.getElementById('hiddenInput_chunk_descriptions'),
  hiddenInput_readings_to_chunk_idx = document.getElementById('hiddenInput_readings_to_chunk_idx'),
  hiddenInput_reading_names = document.getElementById('hiddenInput_reading_names'),
  hiddenInput_reading_links = document.getElementById('hiddenInput_reading_links'),
  hiddenInput_reading_descriptions = document.getElementById('hiddenInput_reading_descriptions'),
  hiddenInput_reading_depths = document.getElementById('hiddenInput_reading_depths'),
  hiddenInput_reading_times = document.getElementById('hiddenInput_reading_times'),
  hiddenInput_reading_types = document.getElementById('hiddenInput_reading_types');


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


// ______ UPDATE NESTED FORM _____
function addChunk() {
  $("#artifacts-creator_wrapper").append(`
    <div class="artifacts-creator_chunk card">
      <div class="form-group chunk-group">
        <h4><input type="text" onChange="UpdateChunk(${chunk_idx}, this.value)" placeholder="Chunk"></h4>
        <input type="text" onChange="UpdateChunkDescription(${chunk_idx}, this.value)" placeholder="ex: This chunk is the study of ... and relates to the the main chunk as ...">
      </div>
      <div id="artifacts-creator_chunk_readings${chunk_idx}">
      </div>
      <button type="button" class="btn btn-secondary" onclick="addReading(${chunk_idx})">Add a Reading</button>
    </div>`);
    chunk_idx += 1;
    chunks.push(null);
    hiddenInput_chunks.value = chunks.join(',');
}

function addReading(chunk_idx) {
  $(`#artifacts-creator_chunk_readings${chunk_idx}`).append(`
    <div class="form-reading">
      <label for="reading-name">Name</label>
      <input type="text" onChange="UpdateReadingName(${reading_idx}, this.value)" placeholder="ex: Head First Design Patterns">
      <div class="form-row">
        <div class="col-auto">
          Difficulty:
          <select name="difficulty" onChange="UpdateReadingDepth(${reading_idx}, this.value)">
            <option value="1">Beginner</option>
            <option value="2">Intermediate</option>
            <option value="3">Advanced</option>
          </select>
        </div>
        <div class="col-auto">
          Media type:
          <select name="difficulty" onChange="UpdateReadingType(${reading_idx}, this.value)">
            <option value="1">Text</option>
            <option value="2">Video</option>
            <option value="0">Other</option>
          </select>
        </div>

        <div class="col-auto">
          Time it takes:
          <input type"number" onChange="UpdateReadingTime(${reading_idx}, this.value)"> mins
        </div>
      </div>
      <label for="reading-link">Link</label>
      <input type="text" onChange="UpdateReadingLink(${reading_idx}, this.value)" placeholder="ex: https://www.amazon.com/Head-First-Design-Patterns-Brain-Friendly/dp/0596007124">

      <label for="reading-description">Description</label>
      <input type="text" onChange="UpdateReadingDescription(${reading_idx}, this.value)" placeholder="ex: Focus on understanding X. Read pages 10-15/ watch from minute 05:03-11:30">

    </div>
    `);
  reading_idx += 1;
  readings_to_chunk_idx.push(chunk_idx);
  reading_names.push(null);
  reading_links.push(null);
  reading_descriptions.push(null);
  reading_depths.push(null);
  reading_times.push(null);
  reading_types.push(null);

  hiddenInput_readings_to_chunk_idx.value = readings_to_chunk_idx.join(',');
  hiddenInput_reading_names.value = reading_names.join(',');
  hiddenInput_reading_links.value = reading_links.join(',');
  hiddenInput_reading_descriptions.value = reading_descriptions.join(',');
  hiddenInput_reading_depths.value = reading_depths.join(',');
  hiddenInput_reading_times.value = reading_times.join(',');
  hiddenInput_reading_types.value = reading_types.join(',');

}
// ______ UPDATE HIDDEN FIELDS _____
function UpdateChunk(chunk_idx, chunk_name) {
  chunks[chunk_idx] = chunk_name;
  hiddenInput_chunks.value = chunks.join(',');
}

function UpdateChunkDescription(chunk_idx, chunk_description) {
  chunk_descriptions[chunk_idx] = chunk_description;
  hiddenInput_chunk_descriptions.value = chunk_descriptions.join(',');
}

function UpdateReadingName(reading_idx, reading_name) {
  reading_names[reading_idx] = reading_name;
  hiddenInput_reading_names.value = reading_names.join(',');
}

function UpdateReadingLink(reading_idx, reading_link) {
  reading_links[reading_idx] = reading_link;
  hiddenInput_reading_links.value = reading_links.join(',');
}

function UpdateReadingDescription(reading_idx, reading_description) {
  reading_descriptions[reading_idx] = reading_description;
  hiddenInput_reading_descriptions.value = reading_descriptions.join(',');
}

function UpdateReadingDepth(reading_idx, reading_depth) {
  reading_depths[reading_idx] = reading_depth;
  hiddenInput_reading_depths.value = reading_depths.join(',');
}

function UpdateReadingTime(reading_idx, reading_time) {
  reading_times[reading_idx] = reading_time;
  hiddenInput_reading_times.value = reading_times.join(',');
}

function UpdateReadingType(reading_idx, reading_type) {
  reading_types[reading_idx] = reading_type;
  hiddenInput_reading_types.value = reading_types.join(',');
}
