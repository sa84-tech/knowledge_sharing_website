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

const comment = {
    _getCommentHtml(comment) {
        return `
            <div class="col px-3 ">
                <a href="${comment.author.url}" class="d-flex align-items-center nav-link p-0 text-small text-muted">
                    <img class="rounded-circle shadow-1-strong me-2"
                        src="${comment.author.avatar}"
                        alt="avatar" width="32" height="32">
                    <span class="fw-bold me-2">${comment.author.name}</span>
                    <span class="date_info">${comment.created}</span>
                </a>

                <div class="mt-1 mb-3">
                    ${comment.body}
                </div>

                <div class="small d-flex justify-content-start mb-3">
                <a href="#" class="reply-form d-flex align-items-center me-4">Ответить</a>
                <span
                    class="ms-1 me-3 text-muted point-events-none addLike"
                    data-target="${comment.id}"
                    data-type="comment"
                >
                    <i
                        class="me-1 text-primary opacity-75 fa-thumbs-up fa-regular"
                        data-target="${comment.id}"
                    ></i>
                    <span>0</span>
                </span>
                <span
                    class="me-3 text-muted point-events-none addBookmark"
                    data-target="${comment.id}"
                    data-type="comment"
                >
                    <i
                        class="me-1 text-primary opacity-75 fa-bookmark fa-regular"
                        data-target="{{ comment.id }}"
                    ></i>
                    <span>0</span>
                </span>
                </div>
            </div>
        `
    },
    getComment(comment) {
        //  <div id="comment_${comment.id}" class="commentBlock mb-4" data-target="${comment.id}" data-type="comment">
        const commentHtmlString = this._getCommentHtml(comment);
        console.log('commentHtmlString', commentHtmlString);
        const newComment = document.createElement('div');
        newComment.id = `comment_${comment.id}`;
        newComment.classList.add('commentBlock', 'mb-4');
        newComment.setAttribute('data-target', comment.id);
        newComment.setAttribute('data-type', 'comment');
        newComment.innerHTML = commentHtmlString;
        return newComment;
    }
}

const postPage = {
    contentBlock: {},
    commentInput: {},
    commentCancelBtn: {},
    rating: {},
    csrfBlock: {},
    currentCommentForm: null,
    replyForm: {},
    commentBlock: {},
    user: {},
    formActionUrl: '',

    init({contentBlock, commentInput, commentCancelBtn, rating, csrfBlockClass},replyForm, comment, currentUser, formActionUrl) {
        this.contentBlock = document.querySelector(contentBlock)
        this.commentInput = document.querySelector(commentInput)
        this.commentCancelBtn = document.querySelector(commentCancelBtn)
        this.csrfBlock = document.querySelector(csrfBlockClass)
        this.rating = document.querySelector(rating)
        this.user = currentUser
        this.formActionUrl = formActionUrl
        this.replyForm = replyForm
        this.commentBlock = comment
        this.contentBlock.addEventListener('click', this.onContentBlockClicked.bind(this));
        this.contentBlock.addEventListener('submit', this.onCommentFormSubmit.bind(this));
        console.log('user', this.user)
    },

    onContentBlockClicked(e) {
        console.log(e.target)
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
            const commentBlock = e.target.closest('.commentBlock')
            this.onReplyButtonClicked(e.target, commentBlock);
        }
        else if (e.target.classList.contains('reply-cancel')) {
            e.preventDefault();
            console.log('onReplyCancelClicked', e.target)
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
        console.log('getComment(comment)', newComment)
        this.renderElement(newComment, commentBlock, this.currentCommentForm);
    },

    onReplyButtonClicked(clickedBtn, commentBlock) {
        console.log('this.user', this.user)
        const postId = this.contentBlock.dataset.post;
        const targetId = commentBlock.dataset.target;
        const formElement = this.replyForm.getReplyForm(this.formActionUrl, targetId, this.user.avatar,
                                                        this.user.name, this.csrfBlock.value);

        this.renderElement(formElement, commentBlock, this.currentCommentForm);
        this.currentCommentForm = formElement;

    },

    onReplyCancelClicked() {
        this.clearBlock(this.currentCommentForm, true)
        console.log(this.currentCommentForm)

    },

    async onCommentFormSubmit(e) {
        e.preventDefault();
        const form = e.target
        console.log('action', form.action);
        console.log('comment_text', form.comment_text.value);
        const postId = this.contentBlock.dataset.post;
        const curCommentBlock = form.closest('.commentBlock')
        const targetType = curCommentBlock.dataset.type;
        const targetId = curCommentBlock.dataset.target;

        const params = {
            csrf: this.contentBlock.dataset.csrf,
            body: {target_type: targetType, target_id: targetId, post_id: postId, text: form.comment_text.value},
        }
        const data = await this.fetchData(form.action, params, 'POST');

        if (data) {
            const comment = data[0].fields
            comment.author = this.user;
            comment.id = data[0].pk;
//            console.log('*** NEW COMMENT', comment)
            this.addComment(comment, curCommentBlock);
        }

    },

    clearBlock(wrapper, removeWrapper = false) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
        if (removeWrapper) wrapper.remove()
    },

    renderHtml(html_string, wrapper, clearBlock=null) {
        if (clearBlock) this.clearBlock(clearBlock);
        wrapper.insertAdjacentHTML('beforeend', html_string);
    },

    renderElement(domElement, wrapper, clearBlock=null) {
        console.log('clearBlock', clearBlock)
        if (clearBlock) this.clearBlock(clearBlock, true);
        console.log('domElement', domElement)
        console.log('wrapper', wrapper)

        wrapper.insertAdjacentElement('beforeend', domElement);
//        wrapper.append(domElement);
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
    postPage.init(settings, replyForm, comment, currentUser, formActionUrl);
});
