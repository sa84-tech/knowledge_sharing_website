'use strict';

const settings = {
    contentBlock:'.content_wrapper',
    commentInput: '#add_comment',
    rating: '.rating',
    commentCancelBtn: '.cancel',
    likeBtnClass: 'likeBtn',
    bookmarkBtnClass: 'bookmarkBtn'
}

const post = {
    contentBlock: null,
    commentInput: null,
    commentCancelBtn: null,
    rating: null,

    init({contentBlock, commentInput, commentCancelBtn, rating}) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.rating = document.querySelector(rating)
        this.contentBlock.addEventListener('click', this.onContentBlockClicked.bind(this));
    },

    addBookmark(postPk) {
        console.log('ADD BOOKMARK', postPk)
    },

    onContentBlockClicked(e) {
        if (e.target == this.commentCancelBtn) {
            this.commentInput.value = '';
        }
        else if (e.target.classList.contains('addLike')) {
            const target_id = e.target.dataset.target;
            const target_type = e.target.dataset.type;
            this.addLike(e.target, target_type, target_id);
        }
        else if (e.target.classList.contains('addBookmark')) {
            const target_id = e.target.dataset.target;
            const target_type = e.target.dataset.type;
            this.addBookmark(e.target, target_type, target_id);
        }
    },

    async addLike(clickedBtn, target_type, target_id) {
        const postId = this.contentBlock.dataset.post;
        const params = {
            csrf: this.contentBlock.dataset.csrf,
            body: {target_type: target_type, target_id: target_id, post_id: postId, btn_type: 'like'},
        }
        const data = await this.fetchData('/icon-btn/', params, 'POST');

        if (data) {
            const {counter_value, user_rating} = data;
            clickedBtn.lastElementChild.innerText = counter_value;
            clickedBtn.firstElementChild.classList.toggle('fa-regular');
            clickedBtn.firstElementChild.classList.toggle('fa-solid');
            this.rating.innerText = user_rating;
        }
    },

    async addBookmark(clickedBtn, target_type, target_id) {
        const postId = this.contentBlock.dataset.post;
        const params = {
            csrf: this.contentBlock.dataset.csrf,
            body: {target_type: target_type, target_id: target_id, post_id: postId, btn_type: 'bookmark'},
        }
        const data = await this.fetchData('/icon-btn/', params, 'POST');

        if (data) {
            const {counter_value, user_rating} = data;
            clickedBtn.lastElementChild.innerText = counter_value;
            clickedBtn.firstElementChild.classList.toggle('fa-regular');
            clickedBtn.firstElementChild.classList.toggle('fa-solid');
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

        if (method === 'GET')
            url += '?' + new URLSearchParams(params).toString();
        else
            options.body = JSON.stringify(params?.body);

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
