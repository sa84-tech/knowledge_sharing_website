'use strict'

document.addEventListener('DOMContentLoaded', function (event) {
    const triggerTabList = [...document.querySelectorAll('#pills-tab button')];
    const triggeredTabPanes = [...document.querySelectorAll('.switchable-tab')];
    const filterBtnGroup = document.querySelector('#filter-btn-group')

    console.log(filterBtnGroup)

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



//    filterBtnGroup.addEventListener('click', function (event) {
//        if (event.target.id.includes('filter-posts')) {
//            console.log(event.target.dataset.filter)
//        }
//        else if (event.target.id.includes('filter-comments')) {
//            console.log(event.target.dataset.filter)
//        }
//        else if (event.target.id.includes('filter-bookmarks')) {
//            console.log(event.target.dataset.filter)
//        }
//        else if (event.target.id.includes('filter-subscriptions')) {
//            console.log(event.target.dataset.filter)
//        }
//    });

});


