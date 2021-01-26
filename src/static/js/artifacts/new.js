$(function() {
    $("div[data-toggle=fieldset]").each(function() {
        var $this = $(this);

        //Add new entry
        $this.find("button[data-toggle=fieldset-add-row]").click(function() {
            var target = $($(this).data("target"))
            console.log(target);
            var oldrow = target.find("[data-toggle=fieldset-entry]:last");
            var row = oldrow.clone(true, true);
            console.log(row.find(":input")[0]);
            var elem_id = row.find(":input")[0].id;
            var elem_num = parseInt(elem_id.replace(/.*-(\d{1,4})-.*/m, '$1')) + 1;
            row.attr('data-id', elem_num);
            row.find(":input").each(function() {
                console.log(this);
                var id = $(this).attr('id').replace('-' + (elem_num - 1) + '-', '-' + (elem_num) + '-');
                $(this).attr('name', id).attr('id', id).val('').removeAttr("checked");
            });
            oldrow.after(row);
        }); //End add new entry

        //Remove row
        $this.find("button[data-toggle=fieldset-remove-row]").click(function() {
            if($this.find("[data-toggle=fieldset-entry]").length > 1) {
                var thisRow = $(this).closest("[data-toggle=fieldset-entry]");
                thisRow.remove();
            }
        }); //End remove row
    });
});
// 
// $( document ).ready(function() {
//   // new Taggle('prereqs-taggle', {
//   //   duplicateTagClass: 'bounce',
//   //   hiddenInputName: 'prereqs[]',
//   // });
//
// });
//
//
// // ______ UPDATE NESTED FORM _____
// var chunk_card_template = `<div class="artifacts-creator_chunk card">
//     <div class="form-group">
//       <h4>
//         <input type="text" name="chunk_titles[]" placeholder="Title">
//       </h4>
//       <h3>
//         <input type="text" name="chunk_concepts[]" placeholder="concept"></h4>
//       </h3>
//     </div>
//     <div class="form-group">
//       <input type="textarea" rows="15" name="chunk_contents[]" placeholder="Type content here">
//     </div>
//
//   </div>`;
//
// function addChunk() {
//   $("#artifacts-creator_wrapper").append(chunk_card_template);
// }
