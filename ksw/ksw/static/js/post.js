'use strict';

const settings = {
    contentBlock:'.content_wrapper',
    commentInput: '#add_comment',
    rating: '.rating',
    commentCancelBtn: '.cancel',
    postLike: '.post_like',
    postBookmark: '.post_bookmark',
}

const post = {
    contentBlock: null,
    commentInput: null,
    commentCancelBtn: null,
    postLike: null,
    postBookmark: null,
    rating: null,

    init({contentBlock, commentInput, commentCancelBtn, postLike, postBookmark, rating}) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.postLike = document.querySelector(postLike)
        this.postBookmark = document.querySelector(postBookmark)
        this.rating = document.querySelector(rating)
        this.contentBlock.addEventListener('click', this.onLikeClicked.bind(this));
    },


    addBookmark(postPk) {
        console.log('ADD BOOKMARK', postPk)
    },

    onLikeClicked(e) {

        if (e.target == this.commentCancelBtn) {
            console.log('comment', e.target)
            this.commentInput.value = '';
        }
        else if (e.target == this.postLike) {
            console.log('like', e.target)
            const post_pk = this.contentBlock.dataset.post;
            this.addLike(e.target, post_pk);
        }
        else if (e.target == this.postBookmark) {
            console.log('bookmark', e.target)
            const post_pk = this.contentBlock.dataset.post;
            this.addBookmark(e.target, post_pk);
        }
    },

    async addLike(clickedBtn, postPk) {
        const params = {
            csrf: clickedBtn.dataset.csrf,
            body: {target_type: 'post', target_id: postPk},
        }
        const data = await this.fetchData('/like/', params, 'POST');

        if (data) {
            const {total_likes, user_rating} = data;
            this.postLike.lastChild.innerText = total_likes;
            this.postLike.firstChild.classList.toggle('fa-regular');
            this.postLike.firstChild.classList.toggle('fa-solid');
            this.rating.innerText = user_rating;
        }
    },

    async addBookmark(clickedBtn, postPk) {

        const params = {
            csrf: clickedBtn.dataset.csrf,
            body: {target_type: 'post', target_id: postPk},
        }
        const data = await this.fetchData('/bookmark/', params, 'POST');

        if (data) {
            const {total_bookmarks, user_rating} = data;
            this.postBookmark.lastChild.innerText = total_bookmarks;
            this.postBookmark.firstChild.classList.toggle('fa-regular');
            this.postBookmark.firstChild.classList.toggle('fa-solid');
            this.rating.innerText = user_rating;
        }
    },

    async fetchData(url, params = {}, method='GET') {

        const myHeaders = new Headers({'X-Requested-With': 'XMLHttpRequest',
                                       'Content-type': 'application/json; cqharset=utf-8',
                                       'X-CSRFToken': params?.csrf});

        let options = {
            method,
            headers: myHeaders
        }

        console.log('method', method)

        if (method === 'GET')
            url += '?' + new URLSearchParams(params).toString();
        else
            options.body = JSON.stringify(params?.body);
            console.log(options)

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(response);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error with fetching data from api', error);
            return null;
        }
    },
}

document.addEventListener('DOMContentLoaded', function (event) {
    post.init(settings);
});
