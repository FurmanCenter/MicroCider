
var NAVBAR_HEIGHT = 100;

// This allows for script caching to speed up the load times?
jQuery.cachedScript = function( url, options ) {
 
  // Allow user to set any option except for dataType, cache, and url
  options = $.extend( options || {}, {
    dataType: "script",
    cache: true,
    url: url
  });
 
  // Use $.ajax() since it is more flexible than $.getScript
  // Return the jqXHR object so we can chain callbacks
  return jQuery.ajax( options );
};


/********************
SHARING
**********************/
/* Add AddToAny callback to handle sharing */
$(function() {
    var a2a_config = a2a_config || {};
    a2a_config.callbacks = a2a_config.callbacks || [];
    a2a_config.callbacks.push({
        share: shareSlide
    });
});


/* Function called when sharing a slide */
function shareSlide(share_data) {
    var activeSlide = getActiveSlide();
    
    if (share_data.service == "Facebook") {
        if ($(activeSlide).hasClass('section-first')) {
            // Share whole section page
            return {
                url: $(activeSlide).parent('section').find('a.section-url').attr('href')
                // title is set in meta tags
            };
        } else {
            // Share individual slide
            return {
                url: activeSlide.attr("data-href")
            };
        }
        
    } else {
        if ($(activeSlide).hasClass('section-first')) {
            return {
                url: $(activeSlide).parent('section').find('a.section-url').attr('href'),
                title: activeSlide.find('.slide-title').text()
            };
        }
        else {
            return {
                //url: window.location.href + "#" + $(activeSlide).attr('id'),
                url: activeSlide.attr("data-href"),
                title: activeSlide.find('.slide-title').text()
            };
        }
    }
}

/*************************

 SCROLLING 

**************************/
/* activate scrollspy menu */
$('body').scrollspy({
    target: '#section-nav',
    offset: $(window).height()/2.0
});


/* Return slide currently displayed */
function getActiveSlide() {
    var activeSlide = null;
    /* Go through each slide and test to see if it is on screen */
    $('article').each(function(i, article) {
        var position = $(article).offset().top - $(window).scrollTop() - $('nav.navbar').first().outerHeight();
        if (Math.abs(position) < ($(window).height() - $('nav.navbar').first().outerHeight())/2.0) {
            activeSlide = $(article);
        }
    });
    return activeSlide;
};

// When scrolling, check to see if first/last section, to change scroll buttons
function checkFirstOrLast() {
    var active = getActiveSlide();

    if ($('article').length > 1 ) {
        var isFirst = $(active).attr('id') == $('article').first().attr('id');
        var isLast = $(active).attr('id') == $('article').last().attr('id');
    } else {
        var isFirst = false;
        var isLast = false;
    }

    $('.prev-btn .prev-section').toggleClass('hidden', isFirst);
    $('.prev-btn .prev-chapter').toggleClass('hidden', !isFirst);

    $('.next-btn .next-section').toggleClass('hidden', isLast);
    $('.next-btn .next-chapter').toggleClass('hidden', !isLast);
}

// Check first or last on scroll
$(window).scroll(function(event) {
    checkFirstOrLast();
});


// Return adjacent slide
// This will wrap around section breaks, so if at the end of one section,
// it will return the first article of the next section
function getAdjacent(adjacentFunction) {
    var active = getActiveSlide();
    var adjacentArticles = adjacentFunction.call($(active), 'article');
    if (! adjacentArticles.length) {
        // If at start/end of section, so no adjacent article, get prev/next section
        var parentSection = $(active).closest('section');
        adjacentArticles = adjacentFunction.call($(parentSection), 'section').find('article');
    }
    return adjacentArticles;
}

var scrollToNext = function() {
    var nextArticles = getAdjacent($().next);
    if (!nextArticles.length) {

    } else {
        scrollTo(nextArticles.first());
        if (nextArticles.first() == $('article').last()) {
            console.log("end of chapter");
        }
    }
};

var scrollToPrev = function() {    
    var prevArticles = getAdjacent($().prev);
    if (!prevArticles.length) {

    } else {
        scrollTo(prevArticles.last());
    }
};


function scrollTo(target) {
    console.log("Scroll to: ", target);
    $('html,body').animate({
            // Offset 50 for the header
            scrollTop: target.offset().top - NAVBAR_HEIGHT
        }, 500);
}

// Attach the scrolling functions to the click event on the next/previous buttons
$('.next-btn').click(scrollToNext);
$('.prev-btn').click(scrollToPrev);



/* smooth scrolling sections */
// Select all anchors with hashes in the href, excluding anchors where "href=#"
$('a[href*="#"]:not([href="#"])').click(function () {
    // If the target has the same path as the current page, then smooth scroll
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        // Escape colons, periods, etc. from the hash (which will match the target's ID)
        var target = $(this.hash.replace(/(:|\.|\[|\]|,)/g, "\\$1" ));

        // If no matching target, look for elements where name matches
        target = target.length ? target : $('[name="' + this.hash.slice(1) + '"]');

        // If a target found, scroll to it
        if (target.length) {
            $('html,body').animate({
                // Offset 50 for the header
                scrollTop: target.offset().top - NAVBAR_HEIGHT
            }, 500);

            // activate animations in this section
            target.find('.animate').delay(1200).addClass("animated");
            setTimeout(function () {
                target.find('.animated').removeClass("animated");
            }, 2000);

            return false;
        }
    }
});


// The initial delay settings for the legend tooltip
var delay = {'show': 500, 'hide': 1000};


/***************************************

This function gets executed when the page loads
****************************************/

$(function () {
    // Resize all figures
    resizeAll();
    // Attach the resizeAll function to the windows resize event, so it fires whenever the window
    // is resized
    $(window).resize(resizeAll);
    // Also resize on clicking tab buttons
    $('.figure-tab-button').click(resizeAll);
    

    // Show left bar
    // If we're coming from the index page, #fromIntro will be added to the web address bar
    // If that happens, we animate showing the left bar
    if (location.hash == "#fromIntro") {
        if (typeof window.history.replaceState == 'function') {
            window.history.replaceState(null, null,location.origin + location.pathname);
        }
        $('#section-nav').removeClass("hidden").addClass("animated slideInLeft");
    } else {
        $('#section-nav').removeClass("hidden");
    }

    
    // Initialize Blazy lazy loader
    var bLazy = new Blazy({
        offset: 1000
    });

    // Initialize scroll buttons (in case page is scrolled to an anchor mid-page)
    checkFirstOrLast();
    setHighchartsOptions();
    
});

