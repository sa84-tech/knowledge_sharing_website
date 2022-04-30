'use strict';

const settings = {
    contentBlock:'.content_wrapper',
    commentInput: '#add_comment',
    rating: '.rating',
    commentCancelBtn: '.cancel',
    postLike: '.post_like'
}

const post = {
    contentBlock: null,
    commentInput: null,
    commentCancelBtn: null,
    postLike: null,
    rating: null,

    init({contentBlock, commentInput, commentCancelBtn, postLike, rating}) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.postLike = document.querySelector(postLike)
        this.rating = document.querySelector(rating)
        this.contentBlock.addEventListener('click', this.onLikeClicked.bind(this));
    },

    async onLikeClicked(e) {

        if (e.target == this.commentCancelBtn) {
            this.commentInput.value = '';
        }

        else if (e.target == this.postLike) {

            const post_pk = this.contentBlock.dataset.post;
            const response = await fetch('/like/', {
                headers: {
                    'X-CSRFToken': e.target.dataset.csrf,
                    'Content-type': 'application/json; cqharset=utf-8',
                },
                method: 'POST',
                body: JSON.stringify({target_type: 'post', target_id: post_pk})

            });

            if (response.ok) {
                const {total_likes, user_rating} = await response.json();
                this.postLike.lastChild.innerText = total_likes;
                this.postLike.firstChild.classList.toggle('fa-regular');
                this.postLike.firstChild.classList.toggle('fa-solid');
                console.log(this.rating)
                console.log(user_rating)
                this.rating.innerText = user_rating;
            } else {
                console.error('Error with fetching data from api');
            }

        }
    },
}

document.addEventListener('DOMContentLoaded', function (event) {
    post.init(settings);
});
