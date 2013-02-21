// simple accordion
(function ($) {
    "use strict";

    $(document).ready(function () {

        $('.collapsed-on-load').hide();
        $('.collapse-head').click(function () {
            var $this = $(this),
                collapsible = $this.prev('.collapse-content');

            collapsible.slideToggle(300);
            $this.toggleClass('collapsed');

            if ($this.hasClass('collapsed')) {
                $this.text('Read more');
            } else {
                $this.text('Read less');
            }

            return false;
        });

    });

}(jQuery));
