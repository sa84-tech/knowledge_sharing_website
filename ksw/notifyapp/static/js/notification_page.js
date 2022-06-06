const notification_settings = {
    notification_header_block_classname: ".notification-block",
    notification_header_list_classname: ".live_notify_list",
    notification_header_badge_classname: '.live_notify_badge',
    notification_page_filters_classname: "#filter-btn-group",
    notification_page_list_classname: ".content-list",
    notification_update_period: 10 * 1000,
}

const notification_api_urls = {
    unread_list_url: '/notifications/get-unread-list',
    mark_read_url: '/notifications/mark-as-read',
    mark_all_read_url: '/notifications/mark-all-as-read',
    delete_notification_url: '/notifications/delete-notification',
}

const notifications_list_page = {
    headerBlock: {},
    headerList: {},
    headerBadge: {},
    pageFilters: {},
    pageList: {},
    apiUrls: {},
    notificationUpdatePeriod: 10000,

    init({notification_header_block_classname,
          notification_header_list_classname,
          notification_header_badge_classname,
          notification_page_filters_classname,
          notification_page_list_classname,
          notification_update_period},
          notification_api_urls) {

        this.headerBlock = document.querySelector(notification_header_block_classname);
        this.headerList = document.querySelector(notification_header_list_classname);
        this.headerBadge = document.querySelector(notification_header_badge_classname);
        this.pageFilters = document.querySelector(notification_page_filters_classname);
        this.pageList = document.querySelector(notification_page_list_classname);
        this.apiUrls = notification_api_urls;
        this.notificationUpdatePeriod = notification_update_period;

        this.headerBlock && this.headerBlock.addEventListener('click', this.onHeaderBlockClicked.bind(this));
        this.pageFilters && this.pageFilters.addEventListener('click', this.onPageFiltersClicked.bind(this));
        this.pageList && this.pageList.addEventListener('click', this.onPageListClicked.bind(this));

        this.fetchNotifications();
    },

    onHeaderBlockClicked(e) {
        if (e.target.classList.contains('follow-notification-target')) {
            e.preventDefault();
            const notificationId = e.target.dataset.target;
            const headerListItem = e.target.closest('li');
            const pageListItem = document.querySelector(`#page-notification-${notificationId}`);
            this.followTargetUrl(notificationId, e.target, headerListItem, pageListItem);
        }
        else if (e.target.classList.contains('mark-all-as-read')) {
            e.preventDefault();
            this.markAllNotificationRead();
        }
        else if (e.target.classList.contains('mark-read')) {
            const notificationId = e.target.dataset.target;
            const headerListItem = e.target.closest('li');
            const pageListItem = document.querySelector(`#page-notification-${notificationId}`);
            this.markNotificationRead(notificationId, headerListItem, pageListItem);
        }
    },

    onPageFiltersClicked(e) {
        console.log('onPageFiltersClicked', e.target)
        const target = event.target;
        if (target.classList.contains('filtering')) {
            const sortingButton = document.querySelector('.sorting.active');
            this.toggleButtonActivity('.filters', target);
            this.displayPane(this.activePane, target.dataset.filter, sortingButton?.dataset.sorting);
        }
        else if (target.classList.contains('sorting')) {
            const filterButton = document.querySelector(`.${this.activePane} .filters.active`);
            this.toggleButtonActivity('.sorting', target);
            this.displayPane(this.activePane, filterButton?.dataset.filter,  target.dataset.sorting);
        }
    },

    onPageListClicked(e) {
        if (e.target.classList.contains('follow-notification-target')) {
            e.preventDefault();
            const notificationId = e.target.dataset.target;
            const headerListItem = document.querySelector(`#header-notification-${notificationId}`);
            const pageListItem = document.querySelector(`#page-notification-${notificationId}`);
            this.followTargetUrl(notificationId, e.target, headerListItem, pageListItem);
        }
        else if (e.target.classList.contains('mark-read')) {
            const notificationId = e.target.dataset.target;
            const headerListItem = document.querySelector(`#header-notification-${notificationId}`);
            const pageListItem = document.querySelector(`#page-notification-${notificationId}`);
            e.target.classList.remove('mark-read');
            this.markNotificationRead(notificationId, headerListItem, pageListItem);
        }
        else if (e.target.classList.contains('notification-delete')) {
            const notificationId = e.target.dataset.target;
            const headerListItem = document.querySelector(`#header-notification-${notificationId}`);
            const pageListItem = document.querySelector(`#page-notification-${notificationId}`);
            this.deleteNotification(notificationId, headerListItem, pageListItem)
        }
    },

    async followTargetUrl(notificationId, clickedLink, headerListItem, pageListItem) {
        const url = this.apiUrls.mark_read_url;
        const response = await this.fetchData(url, {id: notificationId});
        if (response)
            this.fillNotificationBadge(+this.headerBadge.innerText && +this.headerBadge.innerText - 1);
            headerListItem && this.clearBlock(headerListItem, true);
            window.location.href = clickedLink.href;
    },

    async markNotificationRead(notificationId, headerListItem, pageListItem) {
        const url = this.apiUrls.mark_read_url;
        const pageItemBadge = pageListItem.querySelector('.fa-circle');
        const response = await this.fetchData(url, {id: notificationId});
        if (response)
            pageItemBadge.classList.remove('fa-solid');
            pageItemBadge.classList.add('fa-regular');
            this.clearBlock(headerListItem, true);
            this.fillNotificationBadge(+this.headerBadge.innerText - 1);
    },

    async markAllNotificationRead(href) {
        const url = this.apiUrls.mark_all_read_url;
        const data = await this.fetchData(url);
        if (data)
            this.clearBlock(this.headerList, false);
            this.fillNotificationBadge(0);
            this.renderHtml(data.list_html, this.pageList, this.pageList);
    },

    async deleteNotification(notificationId, headerListItem, pageListItem) {
        const url = this.apiUrls.delete_notification_url;
        const data = await this.fetchData(url, {id: notificationId});
        if (data) {
            headerListItem && this.clearBlock(headerListItem, true);
            this.fillNotificationBadge(+this.headerBadge.innerText && +this.headerBadge.innerText - 1);
            this.clearBlock(pageListItem, true);
        }
    },

    async fetchNotifications() {
        const url = this.apiUrls.unread_list_url;
        const data = await this.fetchData(url)
        if (data) {
            this.fillNotificationBadge(data.unread_count);
            this.renderHtml(data.unread_list_html, this.headerList, this.headerList)
        }
        this.setUpdateTimeout();
    },

    setUpdateTimeout() {
        setTimeout(this.fetchNotifications.bind(this),
        this.notificationUpdatePeriod);
    },

    fillNotificationBadge(unreadCount) {
        if (unreadCount) {
            this.headerBadge.innerHTML = unreadCount;
            this.headerBadge.classList.remove('visually-hidden');
        } else {
            this.headerBadge.classList.add('visually-hidden');
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
        this.renderHTML(html_string, this.pageList);
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
            console.error('Error with fetching data from api. Status:', error.message);
            return null;
        }
    },
}

document.addEventListener('DOMContentLoaded', function (event) {
    notifications_list_page.init(notification_settings, notification_api_urls);
});
