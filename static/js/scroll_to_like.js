window.onload = function () {
    if (window.location.hash === '#postlikeDislike') {
        let postFooter = document.getElementById('postlikeDislike');
        postFooter.scrollIntoView();
    }
    if (window.location.hash === '#comments') {
        let commentsFooter = document.getElementById('comments');
        commentsFooter.scrollIntoView();
    }
    if (window.location.hash.includes('#likeComment')) {
        let commentFooter = document.getElementById(window.location.hash.slice(1));
        if (commentFooter) {
            commentFooter.scrollIntoView();
        }
    }
}
