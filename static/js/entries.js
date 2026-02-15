async function loadEntries() {
    let response = await fetch("/API/entries")

    if (response.status===401) {
        window.location.href="/login"
        return
    }

    let entries = await response.json();
    window.allEntries = entries;   
    displayEntries(entries);
}

function displayEntries(entries) {
    const listContainer = document.getElementById("entries_list")
    listContainer.innerHTML=""

    if (entries.length===0) {
        listContainer.innerHTML = `<p class="no-results">No entries found</p>`
        return
    }

    entries.forEach(entry => {
        let div = document.createElement("div");
        div.className = "entry-item"
        
        div.innerHTML=`
            <h2 class="date">${entry.ENTRY_DATE}</h3>

            <p class="title">${entry.TITLE  || "(No Title)"}</p>
        `
        div.addEventListener("click", () => {
            window.location.href = `/entry/${entry.ENTRY_ID}`
        });

        listContainer.appendChild(div)
    });
}

document.getElementById("search_entry").addEventListener("input", function () {
    let searchValue = this.value.toLowerCase()

    let filtered = window.allEntries.filter(entry =>
        (entry.TITLE && entry.TITLE.toLowerCase().includes(searchValue)) ||
        entry.ENTRY_DATE.toLowerCase().includes(searchValue)
    )
    displayEntries(filtered)
})
loadEntries()