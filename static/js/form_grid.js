document.addEventListener("DOMContentLoaded", () => {
    addClassBySelector("input[type=\"checkbox\"]", "visually-hidden");

    // addClassToObjects(document.querySelectorAll().map(obj => ), "vacant")
});


function addClassBySelector(selector, className) {
    addClassToObjects(document.querySelectorAll(selector), className);
}

function addClassToObjects(objects, className) {
    objects.forEach(obj => {
        obj.classList.add(className);
    });
} 
