const BASE_URL = "http://127.0.0.1:3000"

async function main() {
    const source = (await chrome.storage.local.get("source"))?.source;
    const target = (await chrome.storage.local.get("target"))?.target;

    if (!source || !target) return;

    const result = await fetch(`${BASE_URL}/path?source=${source}&target=${target}`)
    if (result.status != 200) return;

    const { next, distance } = await result.json();

    console.log(`${distance} away!`)
    console.log(`Go to ${next} next...`);
    
    chrome.storage.local.set({ source: next, target })
}

main();