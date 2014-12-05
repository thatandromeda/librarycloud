/* Project specific Javascript goes here. */

var $j = jQuery.noConflict();

$j(document).ready(function() {
    // Sets all divs in a row to have the same height. Because CSS is bad at height.
    $j('.row').each(function() {
        var maxHeight = 0;
        var divs = $j(this).children('div');

        divs.each(function() {
            var currentHeight = $j(this).height();
            if (currentHeight > maxHeight) {
                maxHeight = currentHeight;
            }
        });

        divs.height(maxHeight);
    });
});
