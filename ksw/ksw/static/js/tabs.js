'use strict'

const triggerTabList = [...document.querySelectorAll('#pills-tab button')];
const triggeredTabPanes = [...document.querySelectorAll(`h1.tab-pane`)];

triggerTabList.forEach(function (triggerEl) {
    const tabTrigger = new bootstrap.Tab(triggerEl);
    triggerEl.addEventListener('click', function (event) {
        event.preventDefault();
        tabTrigger.show();

        triggeredTabPanes.forEach(item => {
            item.classList.remove('show');
            item.classList.remove('active');
            if (item.id.includes(event.target.dataset.bsTarget.slice(1))) {
                item.classList.add('show');
                item.classList.add('active');
            }
        });
    });
});
