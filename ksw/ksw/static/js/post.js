'use strict';

const settings = {
    contentBlock:'.content_wrapper',
    commentInput: '#add_comment',
    rating: '.rating',
    commentCancelBtn: '.cancel',
    likeBtnClass: 'likeBtn',
    bookmarkBtnClass: 'bookmarkBtn',
    csrfBlockClass: '[name=csrfmiddlewaretoken]',
}

const replyForm = {
    getReplyFormHtml(actionUrl='', targetId, imgSource='', fullName='', csrfTokenValue) {
        return `
            <form id="comment_form_${targetId}" action="${actionUrl}" method="post" class="px-3 py-2 my-2 form-outline ps-4 bg-light">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfTokenValue}">
                <div class="text-muted form-label">Ответить <span class="text-primary">@${fullName}</span></div>
                <div class="d-flex">
                    <img class="rounded-circle shadow-1-strong me-3"
                        src="${imgSource}" alt="avatar" width="42"
                        height="42">
                    <div class="w-100">
                        <textarea class="form-control" id="add_comment" name="comment_text" rows="4" style="background: #fff;"></textarea>
                        <div class="mt-3 d-flex justify-content-end">
                            <input type="submit" class="btn btn-primary btn-sm opacity-75 me-2" value="Отправить">
                            <input type="button" class="cancel btn btn-outline-primary btn-sm opacity-75" value="Отмена">
                        </div>
                    </div>
                </div>
            </form>
        `
    }

};

const post = {
    contentBlock: null,
    commentInput: null,
    commentCancelBtn: null,
    rating: null,
    csrfBlock: null,
    currentCommentBlock: null,
    replyForm: {},

    init({contentBlock, commentInput, commentCancelBtn, rating, csrfBlockClass}, replyForm) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.csrfBlock = document.querySelector(csrfBlockClass)
        this.rating = document.querySelector(rating)
        this.replyForm = replyForm
        this.contentBlock.addEventListener('click', this.onContentBlockClicked.bind(this));
    },

    addBookmark(postPk) {
        console.log('ADD BOOKMARK', postPk)
    },

    onContentBlockClicked(e) {
        console.log(e)
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
        else if (e.target.classList.contains('reply')) {
            e.preventDefault();
            const commentBlock = e.target.closest('.commentBlock')
            this.onReplyButtonClicked(e.target, commentBlock);
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

    onReplyButtonClicked(clickedBtn, commentBlock) {
        console.log('commentBlock', commentBlock)
        const postId = this.contentBlock.dataset.post;
        const targetId = commentBlock.dataset.target;
        const formElement = this.replyForm.getReplyFormHtml(`#`, targetId, '/media/seeder/users/f_4.webp', 'Иван Иванов', this.csrfBlock.value);
        console.log('formElement', formElement)

        this.renderHtml(formElement, commentBlock)
    },

    clearBlock(wrapper) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
    },

    renderHtml(html_string, wrapper, clearBlock=null) {
        if (clearBlock) this.clearBlock(clearBlock);
        wrapper.insertAdjacentHTML('beforeend', html_string);
    },

    renderErrorAlert(error) {
        const html_string = `<div class="alert alert-danger" role="alert">
                Ошибка: status ${error.status}. ${error.statusText}
            </div>`;
        this.renderHTML(html_string, this.contentBlock);
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
    post.init(settings, replyForm);
});
