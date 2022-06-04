'use strict'

const settings = {
    contentBlock:'#tab-content-block',
    menuBlock: '#pills-tab',
    filterBlock: '#filter-btn-group',
    triggerTabList: '#pills-tab button',
    triggeredTabPanes: '.switchable-tab',
}

const account = {
    url: '/account/api/users/',
    user: null,
    activePane: 'posts',
    menuBlock: null,
    contentBlock: null,
    triggerTabList: null,
    triggeredTabPanes: null,
    filterBlock: null,

    init({menuBlock, contentBlock, filterBlock, triggerTabList, triggeredTabPanes}) {
        this.user = document.querySelector.innerText;
        this.menuBlock = document.querySelector(menuBlock);
        this.contentBlock = document.querySelector(contentBlock);
        this.filterBlock = document.querySelector(filterBlock),
        this.triggerTabList = [...document.querySelectorAll(triggerTabList)],
        this.triggeredTabPanes = [...document.querySelectorAll(triggeredTabPanes)],
        this.displayContentBlock();
        this.addEventHandlers();
        this.displayPane(this.activePane);
    },

    displayContentBlock(html_string) {
        this.renderHTML(html_string, this.contentBlock);
    },

    clearBlock(wrapper) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
    },

    getUrl(filter='', sorting='') {
        const url = `${this.url}${this.user}/${this.activePane}/`;
        const params = {}
        if (filter && filter !== 'all')
            params['filter'] = filter;

        if (sorting)
            params['sorting'] = sorting;

        return {url, params}
    },

    renderHTML(html_string) {
        this.clearBlock(this.contentBlock);
        this.contentBlock.insertAdjacentHTML('beforeend', html_string);
    },

    renderErrorAlert(error) {
        const html_string = `<div class="alert alert-danger" role="alert">
                Ошибка: status ${error.status}. ${error.statusText}
            </div>`;
        this.renderHTML(html_string, this.contentBlock);
    },

    async displayPane(tabName='posts', filter='', sorting='') {
        const {url, params} = this.getUrl(filter, sorting);
        const response = await this.fetchData(url, params);

        this.renderHTML(response.result);
        this.togglePaneVisibility(tabName);
    },

    togglePaneVisibility(tabName) {
        this.triggeredTabPanes.forEach(item => {
            item.classList.remove('show');
            item.classList.remove('active');
            if (item.id.includes(tabName)) {
                item.classList.add('show');
                item.classList.add('active');
            }
        });
    },

    toggleButtonActivity(buttons_class, button) {
        const buttons = document.querySelectorAll(buttons_class)
        buttons.forEach(item => {
            item.classList.remove('active');
            if (item === button) {
                item.classList.add('active');
            }
        });
    },

    addEventHandlers() {
        this.menuBlock.addEventListener(
            'click',
            this.onMenuItemSelected.bind(this)
        );
        this.filterBlock.addEventListener(
            'click',
            this.onFilterSelected.bind(this)
        );
        this.contentBlock.addEventListener(
            'click',
            this.onContentBlockClicked.bind(this)
        );
    },

    onMenuItemSelected(event) {
        if (event.target.nodeName === 'BUTTON') {
            this.activePane = event.target.id.split('-')[1];
            const sortingButton = document.querySelector('.sorting.active');
            const filterButton = document.querySelector(`.${this.activePane} .filters.active`);
            this.displayPane(this.activePane, filterButton?.dataset.filter, sortingButton?.dataset.sorting);
        }
    },

    onFilterSelected(event) {
        const target = event.target;
        if (target.classList.contains('filters')) {
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

    onContentBlockClicked(event) {
        console.log('*** onContentBlockClicked(event) called ***\n',event)
    },

    async fetchData(url, params = {}, method='GET') {

        const myHeaders = new Headers({'X-Requested-With': 'XMLHttpRequest'});

        let options = {
            method,
            headers: myHeaders
        }

        if (method === 'GET')
            url += '?' + new URLSearchParams(params).toString();
        else
            options.body = JSON.stringify(params);

        try {
            const response = await fetch(url, options);
            if (!response.ok) {
                throw new Error(response);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            this.renderErrorAlert(error);
        }
    },
}

document.addEventListener('DOMContentLoaded', function (event) {
    account.init(settings);
});
