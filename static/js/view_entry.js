
const preview=document.getElementById('media-preview')
preview.addEventListener("click", function (e) {
    e.preventDefault()
    let wrapper = e.target.closest(".media_wrapper");
    if (!wrapper) return;

    if (e.target.closest(".maximize_image")) {
        let img = wrapper.querySelector("img");
        if (img) {
            window.open(img.src, "_blank");
        }
    }
});
