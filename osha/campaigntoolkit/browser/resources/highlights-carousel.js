/*global document, jQuery*/

// initialize links to examples to open in an overlay
(function ($) {
    "use strict";

    $(document).ready(function () {

        var overlayOpts = {
            subtype: "ajax",
            filter: "#content"
        };

        $("div.examples a.exampleLink").prepOverlay(overlayOpts);
    });

}(jQuery));


// initialize examples highlights carousel
(function ($) {
    "use strict";

    $(document).ready(function () {
        $("#highlights-tabs").tabs("#highlights-content > div");
    });
}(jQuery));
