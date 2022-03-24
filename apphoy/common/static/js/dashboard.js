let checkboxes = $("input[type='checkbox']");
let removeButton = $("#group-remove");
let table = $(".item-list")
let headerChecks = table.find("th").has("input[type='checkbox']")
let checkboxCells = headerChecks.add(table.find("td").has("input[type='checkbox']"))

checkboxes.click(function() {
    removeButton.prop("disabled", !checkboxes.is(":checked"));
});

checkboxCells.on("click", function() {
    let checkbox = $(this).find("input[type='checkbox']");
    checkbox.prop("checked", !checkbox.prop("checked"));
});

function selectAll(selectAllCheckbox)
{
    checkboxes.not(selectAllCheckbox).prop("checked", !selectAllCheckbox.checked);
}

let ids = [];
const pluralize = (count, noun, suffix = "s") => `${noun}${count !== 1 ? suffix : ""}`;

removeButton.click(function() {
    $(":checkbox:checked").each(function(i) {
        ids[i] = $(this).val();
    });
    let count = ids.length;
    if(count > 0) {
        if (confirm("Are you sure you want to remove " + count + " " + pluralize(count, "object") + "?")) {
            $.ajax({
                type: "POST",
                url: "",
                data: { "action": "Delete", ids },
                success: function(response, status) {
                    console.log(status);
                    for(let i=0; i < count; i++) {
                        let removedRow = $("tr#" + ids[i]);
                        removedRow.css("background-color", "#ccc");
                        removedRow.fadeOut("slow");
                        let removedCheckbox = $("input[type='checkbox'][value=" + ids[i] + "]");
                        removedCheckbox.prop("checked", false);
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
