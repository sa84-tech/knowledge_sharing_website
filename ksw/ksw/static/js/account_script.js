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
        this.user = document.querySelector('#username').innerText;
        this.menuBlock = document.querySelector(menuBlock);
        this.contentBlock = document.querySelector(contentBlock);
        this.filterBlock = document.querySelector(filterBlock),
        this.triggerTabList = [...document.querySelectorAll(triggerTabList)],
        this.triggeredTabPanes = [...document.querySelectorAll(triggeredTabPanes)],
        this.displayContentBlock();
        this.addEventHandlers();
        this.displayPane(`${this.url}${this.user}/${this.activePane}/`);
    },

    displayContentBlock(html_string) {
        this.renderHTML(html_string, this.contentBlock);
    },

    clearBlock(wrapper) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
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

    async displayPane(url) {
        const response = await this.fetchData(url);
        if (!response.error) {
            this.renderHTML(response.result);
        }
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
        this.activePane = event.target.id.split('-')[1];
        const url = `${this.url}${this.user}/${this.activePane}/`
        this.displayPane(url)
    },

    onFilterSelected(event) {
        console.log('*** onFilterSelected(event) called ***\n', event)
    },

    onContentBlockClicked(event) {
        console.log('*** onContentBlockClicked(event) called ***\n',event)
    },

    async fetchData(url, options = {}) {
        options['headers'] = {
            "X-Requested-With": "XMLHttpRequest"
        }
        const response = await fetch(url, options);
        if (response.ok) {
            const json = await response.json();
            return json;
        }
        else {
            this.renderErrorAlert(response);
            return { error: true, objects: [] };
        }
    },
}

document.addEventListener('DOMContentLoaded', function (event) {
    account.init(settings);
});
