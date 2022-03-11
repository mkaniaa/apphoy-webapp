let checkboxes = $("input[type='checkbox']");
let removeButton = $("#group-remove");
let selectAllCheck = $("#select-all");

selectAllCheck.click(function() {
    checkboxes.not(this).prop("checked", this.checked);
});

checkboxes.click(function() {
    removeButton.prop("disabled", !checkboxes.is(":checked"));
});

let ids = [];
const pluralize = (count, noun, suffix = 's') => `${noun}${count !== 1 ? suffix : ''}`;

removeButton.click(function() {
    $(':checkbox:checked').each(function(i) {
        ids[i] = $(this).val();
    });
    let count = ids.length;
    if(count > 0) {
        if (confirm("Are you sure you want to remove " + count + " " + pluralize(count, 'object') + "?")) {
            $.ajax({
                type: "POST",
                url: "",
                data: { "action": "Delete", ids },
                success: function(response, status) {
                    console.log(status);
                    for(let i=0; i < count; i++) {
                        let removedRow = $('tr#' + ids[i]);
                        removedRow.css('background-color', '#ccc');
                        removedRow.fadeOut('slow');
                        removedCheckbox = $("input[type='checkbox'][value=" + ids[i] + "]");
                        removedCheckbox.prop('checked', false);
                    }
                },
                statusCode: {
                    403: function() {
                        window.location.reload();
                    }
                }
            });
        }
    }
});
