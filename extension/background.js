// background.js
chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
    let words = message.title.split(' ');
    // remove special characters 
    words = words.map(word => word.replace(/[^a-zA-Z ]/g, ""));
    new_title = '';

    let titleWords = [];
    for (let word of words) {
        let rhymingWord = await getRhymingWord(word);
        if (rhymingWord) {
            titleWords.push(rhymingWord);
        }
        else {
            titleWords.push(word);
        }

    }

    new_title = titleWords.join(' ');
    new_desciption = titleWords.join(' ') + '\n' + message.description;

    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { title: new_title, description: new_desciption });
    });

    data = {
        'title': message.title,
        'url': message.url,
        'new_title': new_title,
        'summary': message.description,
        'new_summary': new_desciption

    }

    console.log("sending data to backend......");
    sendJsonData(data);

});

async function getRhymingWord(word) {
    let rhymingWord = null;
    await fetch(`https://api.datamuse.com/words?rel_rhy=${word}`)
        .then(response => response.json())
        .then(data => {

            if (data.length > 0) {
                rhymingWord = data[0].word;
                console.log(`Rhyming word for ${word} is ${rhymingWord}`);
            }
        })
        .catch(error => {
            return null;
        });
    return rhymingWord;
}

// send json data to backend

async function sendJsonData(data) {
    await fetch('http://localhost:5000/new', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });

}

