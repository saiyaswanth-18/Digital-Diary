const today = new Date().toISOString().split('T')[0];
document.getElementById('diary-date').value = today;

const preview=document.getElementById('media-preview')

const save_btn=document.getElementById('save-diary')
const diaryform=document.getElementById('diary-form')
const diary_content=document.getElementById('diary-content')
let allfiles=[]
const f=document.getElementById('file_upload')
f.addEventListener('change',function(e){
        let selected_files=Array.from(e.target.files)
       
        let start_index=allfiles.length
        allfiles.push(...selected_files)

        selected_files.forEach((file,i)=>{

            let file_url=URL.createObjectURL(file)
            let index=start_index+i
            let wrapper = document.createElement("div");
            wrapper.className = "media_wrapper";
            wrapper.dataset.index = index;
            wrapper.style.position = "relative"

        if (file.type.startsWith("image/")) {
            wrapper.innerHTML = `
                <img src="${file_url}" class="files_media">
                <button class="remove_btn" type="button"><i class="fa-solid fa-trash"></i></button>
                <button class="maximize_image" type="button"><i class="fa-solid fa-expand"></i></button>
            `;
        }
        else if (file.type.startsWith("video/")) {
            wrapper.innerHTML = `
                <video src="${file_url}" class="files_media" controls></video>
                <button class="remove_btn" type="button"><i class="fa-solid fa-trash"></i></button>
            `;
        }
            preview.appendChild(wrapper)
        })
        f.value=""
})
preview.addEventListener("click", function (e) {
    e.preventDefault()
    let wrapper = e.target.closest(".media_wrapper");
    if (!wrapper) return;

    let index = parseInt(wrapper.dataset.index);

    if (e.target.closest(".remove_btn")) {
        wrapper.remove();
        allfiles[index] = null;   
        return;
    }

    if (e.target.closest(".maximize_image")) {
        let img = wrapper.querySelector("img");
        if (img) {
            window.open(img.src, "_blank");
        }
    }
});

save_btn.addEventListener("click", function (e) {

    e.preventDefault()

    const finalFiles = allfiles.filter(f => f !== null);
    let dataT = new DataTransfer();
    finalFiles.forEach(f => dataT.items.add(f));
    f.files = dataT.files;
    if(diary_content.value.trim())
        diaryform.submit();
    else{
        alert("Write Something in Diary..")
    }
});