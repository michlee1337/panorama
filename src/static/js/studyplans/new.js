// ______ STUDYPLAN CREATOR INTERNAL STATE ______
let topics = [],
  readings_to_topic_idx = [],   // DEV: maybe post-calc this
  reading_names = [],
  reading_links = [],
  prereqs = [],
  topic_idx = 0,
  reading_idx = 0;

$( document ).ready(function() {
  // ______ HIDDEN INPUTS ______
  let hiddenInput_prereqs = document.getElementById('hiddenInput_prereqs'),
  hiddenInput_topics = document.getElementById('hiddenInput_topics'),
  hiddenInput_readings_to_topic_idx = document.getElementById('hiddenInput_readings_to_topic_idx'),
  hiddenInput_reading_names = document.getElementById('hiddenInput_reading_names'),
  hiddenInput_reading_links = document.getElementById('hiddenInput_reading_links');

  // ______ PREREQUISITES ____
  // hiddenInput_prereqs = document.createElement('input'),

  let mainInput = document.createElement('input');
  var prereqs_input_div = document.getElementById('prereqs-input');
  // hiddenInput_prereqs.setAttribute('type', 'hidden');
  // hiddenInput_prereqs.setAttribute('name','prerequisites');

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
  // prereqs_input_div.appendChild(hiddenInput_prereqs);

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
  // ______ PREREQUISITES END _____
});


// ______ UPDATE FORM _____
function addTopic() {
  $("#studyplans-creator_wrapper").append(`
    <div class="studyplans-creator_topic card">
      <div class="form-group topic-group">
        <h4><input type="text" class="form-control" onChange="UpdateTopic(${topic_idx}, this.value)" placeholder="Topic"></h4>
      </div>
      <div id="studyplans-creator_topic_readings${topic_idx}">
      </div>
      <button type="button" class="btn btn-secondary" onclick="addReading(${topic_idx})">Add a Reading</button>
    </div>`);
    topic_idx += 1;
    topics.push(null);
    hiddenInput_topics.value = topics.join(',');
}

function addReading(topic_idx) {
  $(`#studyplans-creator_topic_readings${topic_idx}`).append(`
    <div class="form-group">
      <label for="reading-name">Name</label>
      <input type="text" class="form-control" onChange="UpdateReadingName(${reading_idx}, this.value)" placeholder="ex: Head First Design Patterns">
    </div>
    <div class="form-group">
      <label for="reading-link">Link</label>
      <input type="text" class="form-control" onChange="UpdateReadingLink(${reading_idx}, this.value)" placeholder="ex: https://www.amazon.com/Head-First-Design-Patterns-Brain-Friendly/dp/0596007124">
    </div>
    `);
  reading_idx += 1;
  readings_to_topic_idx.push(topic_idx);
  reading_names.push(null);
  reading_links.push(null);
  hiddenInput_readings_to_topic_idx.value = readings_to_topic_idx.join(',');
  hiddenInput_reading_names.value = reading_names.join(',');
  hiddenInput_reading_links.value = reading_links.join(',');

}

// ______ UPDATE HIDDEN FIELDS _____
function UpdateTopic(topic_idx, topic_name) {
  topics[topic_idx] = topic_name;
  hiddenInput_topics.value = topics.join(',');
}

function UpdateReadingName(reading_idx, reading_name) {
  reading_names[reading_idx] = reading_name;
  hiddenInput_reading_names.value = reading_names.join(',');
}

function UpdateReadingLink(reading_idx, reading_link) {
  reading_links[reading_idx] = reading_link;
  hiddenInput_reading_links.value = reading_links.join(',');
}
