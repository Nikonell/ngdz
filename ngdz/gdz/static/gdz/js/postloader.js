function postloader() {
    const postloader = document.querySelector('#postloader');
    postloader.style.display = 'flex';
}

window.onunload = function() {
    const postloader = document.querySelector('#postloader');
    postloader.style.display = 'none';
}
