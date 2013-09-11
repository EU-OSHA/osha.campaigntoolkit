/*global document, jQuery*/

// initialize examples highlights carousel
(function ($) {
    "use strict";

    $(document).ready(function () {
        $("#highlights-tabs").tabs("#highlights-content > div");
    });
}(jQuery));
