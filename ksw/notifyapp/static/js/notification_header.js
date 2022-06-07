'use strict';

const notification_block = ".notification-block";
const notify_menu_class = ".live_notify_list";
const notify_badge_class = '.live_notify_badge';

const apiUrls = {
    unread_list_url: '/notifications/get-unread-list',
    mark_read_url: '/notifications/mark-as-read',
    mark_all_read_url: '/notifications/mark-all-as-read',
}

const notifications = {
    notificationBlock: {},
    contentBlock: {},
    notifyBadge: {},
    apiUrls: {},
    notification_update_period: 15 * 1000,

    init(notificationBlock, contentBlock, notifyBadge, apiUrl) {
        this.notificationBlock = document.querySelector(notificationBlock);
        this.contentBlock = document.querySelector(contentBlock);
        this.notifyBadge = document.querySelector(notifyBadge);
        this.apiUrls = apiUrls;
        this.notificationBlock.addEventListener('click', this.onContentBlockClicked.bind(this));
        this.fetchNotifications();
    },

    onContentBlockClicked(e) {
        if (e.target.classList.contains('follow-notification-target')) {
            e.preventDefault();
            const notificationId = e.target.dataset.target;
            this.followTargetUrl(notificationId, e.target);
        }
        else if (e.target.classList.contains('mark-all-as-read')) {
            e.preventDefault();
            this.markAllNotificationRead();
        }
        else if (e.target.classList.contains('mark-read')) {
            const notificationId = e.target.dataset.target;
            this.markNotificationRead(notificationId, e.target);
        }
    },

    async followTargetUrl(notificationId, clickedLink) {
        const url = this.apiUrls.mark_read_url;
        const notificationListItem = clickedLink.closest('li');
        const response = await this.fetchData(url, {id: notificationId});
        if (response)
            this.fillNotificationBadge(+this.notifyBadge.innerText - 1);
            this.clearBlock(notificationListItem, true);
            window.location.href = clickedLink.href;
    },

    async markNotificationRead(notificationId, clickedMark) {
        const notificationListItem = clickedMark.closest('li');
        const url = this.apiUrls.mark_read_url;
        const response = await this.fetchData(url, {id: notificationId});
        if (response)
            this.clearBlock(notificationListItem, true);
            this.fillNotificationBadge(+this.notifyBadge.innerText - 1);
    },

    async markAllNotificationRead(href) {
        const url = this.apiUrls.mark_all_read_url;
        const response = await this.fetchData(url);
        if (response)
            this.clearBlock(this.contentBlock, false);
            this.fillNotificationBadge(0);
    },

    async fetchNotifications() {
        const url = this.apiUrls.unread_list_url;
        const data = await this.fetchData(url)
        if (data) {
            this.fillNotificationBadge(data.unread_count);
            this.renderHtml(data.unread_list_html, this.contentBlock, this.contentBlock)
        }
        this.setUpdateTimeout();
    },

    setUpdateTimeout() {
        setTimeout(this.fetchNotifications.bind(this),
        this.notification_update_period);
    },

    fillNotificationBadge(unreadCount) {
        if (unreadCount) {
            this.notifyBadge.innerHTML = unreadCount;
            this.notifyBadge.classList.remove('visually-hidden');
        } else {
            this.notifyBadge.classList.add('visually-hidden');
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
            this.clearBlock(clearBlock);
        }
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
                throw new Error(response.statusText);
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
    notifications.init(notification_block, notify_menu_class, notify_badge_class, apiUrls);
});
