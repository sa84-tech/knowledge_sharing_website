'use strict'

const settings = {
    contentBlock:'#post-list',
    filterBlock: '#filter-btn-group',
}

const search = {
    url: '/search/sorting/',
    contentBlock: null,
    filterBlock: null,

    init({contentBlock, filterBlock}) {
        this.contentBlock = document.querySelector(contentBlock);
        this.filterBlock = document.querySelector(filterBlock),
        this.addEventHandlers();
    },

    displayContentBlock(html_string) {
        this.renderHTML(html_string, this.contentBlock);
    },

    clearBlock(wrapper) {
        while (wrapper.firstChild) {
            wrapper.firstChild.remove();
        }
    },

    getUrl(sorting='') {
        const url = this.url;
        const params = {}
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

    async displayItems(sorting='') {
        const {url, params} = this.getUrl(sorting);
        const response = await this.fetchData(url, params);
        console.log('response.result', response.result)
        this.renderHTML(response.result);
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
        this.filterBlock.addEventListener(
            'click',
            this.onSortingSelected.bind(this)
        );
    },

    onSortingSelected(event) {
        const target = event.target;
        if (target.classList.contains('sorting')) {
            this.toggleButtonActivity('.sorting', target);
            this.displayItems(target.dataset.sorting);
        }
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
    search.init(settings);
});
