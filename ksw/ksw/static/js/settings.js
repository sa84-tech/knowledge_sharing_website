'use strict'

document.addEventListener('DOMContentLoaded', function (event) {
    const triggerTabList = [...document.querySelectorAll('#pills-tab button')];
    const triggeredTabPanes = [...document.querySelectorAll('.switchable-tab')];
    const filterBtnGroup = document.querySelector('#filter-btn-group')
    const triggeredToast = document.querySelector('.showSuccess')

    if (triggeredToast) {
        const toast = new bootstrap.Toast(triggeredToast)
        toast.show()
    }

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
});
