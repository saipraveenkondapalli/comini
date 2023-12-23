// contentScript.js

let title = document.querySelector('meta[property="og:title"]').getAttribute('content');
let description = document.querySelector('meta[property="og:description"]').getAttribute('content');

// Now you can use the title and description
console.log(title, description);
console.log("Hello from contentScript.js");
// get current page url 
let url = window.location.href;

chrome.runtime.sendMessage({ title: title, description: description, url: url });


chrome.runtime.onMessage.addListener(
    function (request, sender, sendResponse) {
        console.log("Message received!");

        // wait for page to load
        // get element #main > div > div > div.content__section > main > div > div.jsx-ace90f4eca22afc7.Story_story__content__body__qCd5E.story__content__body.widgetgap > h1
        var title = document.querySelector("body > div.content > div > div > section > div > div.sp-hd > div > h1");
        if (title) {
            title.innerHTML = request.title;
        }
        var summary = document.querySelector("body > div.content > div > div > section > div > div.sp-hd > h2")
        if (summary) {
            summary.innerHTML = request.description;
        }
    }
);
