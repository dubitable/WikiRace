BASE_URL = "https://en.wikipedia.org/wiki/"

source.value = "Wikipedia"
target.value = "Vugar Mustafayev (minister)"

go.addEventListener("click", () => {
    if (source.value === "" || target.value === "") return;

    chrome.storage.local.set({source: source.value, target: target.value})
    chrome.tabs.update(undefined, {url: BASE_URL + source.value})

    chrome.action.setPopup({popup: "active.html"});
})