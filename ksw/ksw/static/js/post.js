'use strict';

const settings = {
    contentBlock:'.content_wrapper',
    commentInput: '#add_comment',
    rating: '.rating',
    commentCancelBtn: '.cancel',
    likeBtnClass: 'likeBtn',
    bookmarkBtnClass: 'bookmarkBtn',
    csrfBlockClass: '[name=csrfmiddlewaretoken]',
    commentFormSelector: '.form-outline',
}

const replyForm = {
    _getReplyFormHtml(avatarSource='', userFullName='', csrfTokenValue) {
        return `
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfTokenValue}">
            <div class="text-muted form-label">Ответить <span class="text-primary">@${userFullName}</span></div>
            <div class="d-flex">
                <img class="rounded-circle shadow-1-strong me-3"
                    src="${avatarSource}" alt="avatar" width="42"
                    height="42">
                <div class="w-100">
                    <textarea
                        class="form-control" id="add_comment"
                        name="comment_text" rows="4" style="background: #fff;"
                    ></textarea>
                    <div class="mt-3 d-flex justify-content-end">
                        <input type="submit" class="btn btn-primary btn-sm opacity-75 me-2" value="Отправить">
                        <input type="button" class="reply-cancel btn btn-outline-primary btn-sm opacity-75" value="Отмена">
                    </div>
                </div>
            </div>
        `
    },

    getReplyForm(actionUrl='', targetCommentId, avatarSource='', userFullName='', csrfTokenValue) {
        const formHtmlString = this._getReplyFormHtml(avatarSource, userFullName, csrfTokenValue)
        const form = document.createElement('form');
        form.id = `comment_form_${targetCommentId}`;
        form.method = 'POST';
        form.action = actionUrl;
        form.classList.add('px-3', 'py-2', 'my-2', 'form-outline', 'ps-4', 'bg-light');
        form.innerHTML = formHtmlString;
        return form;
    },
};

const postPage = {
    contentBlock: {},
    commentInput: {},
    commentCancelBtn: {},
    rating: {},
    csrfBlock: {},
    currentCommentForm: null,
    replyForm: {},
    user: {},
    formActionUrl: '',

    init({contentBlock, commentInput, commentCancelBtn, rating, csrfBlockClass, commentFormSelector},replyForm, currentUser) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.csrfBlock = document.querySelector(csrfBlockClass)
        this.rating = document.querySelector(rating)
        this.user = currentUser
        this.formActionUrl = document.querySelector(commentFormSelector).action
        this.replyForm = replyForm
        this.contentBlock.addEventListener('click', this.onContentBlockClicked.bind(this));
        this.contentBlock.addEventListener('submit', this.onCommentFormSubmit.bind(this));
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
        else if (e.target.classList.contains('reply-form')) {
            e.preventDefault();
            this.onReplyButtonClicked(e.target);
        }
        else if (e.target.classList.contains('reply-cancel')) {
            e.preventDefault();
            this.onReplyCancelClicked();
        }
    },

    async addLike(clickedBtn, target_type, target_id) {
        const postId = this.contentBlock.dataset.post;
        const params = {
            csrf: this.contentBlock.dataset.csrf,
            body: {target_type: target_type, target_id: target_id, post_id: postId, btn_type: 'like'},
        }
        const data = await this.fetchData('/mark/', params, 'POST');

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
        const data = await this.fetchData('/mark/', params, 'POST');

        if (data) {
            const {counter_value, user_rating} = data;
            clickedBtn.lastElementChild.innerText = counter_value;
            clickedBtn.firstElementChild.classList.toggle('fa-regular');
            clickedBtn.firstElementChild.classList.toggle('fa-solid');
            this.rating.innerText = user_rating;
        }
    },

    addComment(comment, commentBlock) {
        const newComment = this.commentBlock.getComment(comment);
        this.renderElement(newComment, commentBlock, this.currentCommentForm);
    },

    onReplyButtonClicked(clickedBtn) {
        const commentBlock = clickedBtn.closest('.commentBlock');
        const commentItem = clickedBtn.closest('.commentItem');
        const postId = this.contentBlock.dataset.post;
        const targetId = commentBlock.dataset.target;
        const authorName = commentItem.querySelector('.authorName')?.innerText;
        const formElement = this.replyForm.getReplyForm(this.formActionUrl, targetId, this.user.avatar,
                                                        authorName, this.csrfBlock.value);

        this.renderElement(formElement, commentItem, this.currentCommentForm);
        this.currentCommentForm = formElement;

    },

    onReplyCancelClicked() {
        this.clearBlock(this.currentCommentForm, true)
        this.currentCommentForm = null;
    },

    async onCommentFormSubmit(e) {
        e.preventDefault();
        const form = e.target
        const postId = this.contentBlock.dataset.post;
        const curCommentBlock = form.dataset.targetType === 'post'
            ? document.querySelector('.card-body')
            : form.closest('.commentBlock')
        const targetType = curCommentBlock.dataset.type;
        const targetId = curCommentBlock.dataset.target;

        const params = {
            csrf: this.contentBlock.dataset.csrf,
            body: {target_type: targetType, target_id: targetId, post_id: postId, text: form.comment_text.value},
        }
        const response = await this.fetchData(form.action, params, 'POST');

        if (response) {
            this.renderHtml(response.result, curCommentBlock, this.currentCommentForm);
            if (form.dataset.targetType === 'post') this.commentInput.value = '';
        }

    },

    clearBlock(wrapper, removeWrapper = false) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
        if (removeWrapper) wrapper.remove()
    },

    renderHtml(html_string, wrapper, clearBlock=null) {
        if (clearBlock) {
            this.clearBlock(clearBlock, true);
            this.currentCommentForm = null;
        }
        wrapper.insertAdjacentHTML('beforeend', html_string);
    },

    renderElement(domElement, wrapper, clearBlock=null) {
        if (clearBlock) this.clearBlock(clearBlock, true);
        wrapper.insertAdjacentElement('afterend', domElement);
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
    const currentUser = {id, name, avatar}
    postPage.init(settings, replyForm, currentUser);
});
