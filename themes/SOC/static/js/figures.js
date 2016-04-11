/*******************************
figures.js

This script manages the figures, charts, and maps.
It is loaded by the base template.
********************************/


// Create an empty charts object. The charts themselves will be saved
// as properties of this object, which will make it easier to debug
var charts = {};


function setHighchartsOptions() {
    // Set default Highcharts Options for all figures
    // Options can be overridden for specific figures
    Highcharts.setOptions({
        lang: {
            thousandsSep: ","
        },
        colors: [
            /* Option 1 */
            '#66c2a5', //  0: Category Color 1
            '#fc8d62', //  1: Category Color 2
            '#8da0cb', //  2: Category Color 3
            '#e78ac3', //  3: Category Color 4
            '#a6d854', //  4: Category Color 5
            '#ffd92f', //  5: Category Color 6

            /* Option 2
                '#1b9e77', //  0: Category Color 1
                '#d95f02',  //  1: Category Color 2
                '#7570b3',  //  2: Category Color 3
                '#e7298a',  //  3: Category Color 4
                '#66a61e',  //  4: Category Color 5
                '#e6ab02',  //  5: Category Color 6
                */

            // '#0C4052', //  6: Primary Darkest
            // '#006C8F', //  7: Primary Darker*
            // '#3299BB', //  8: Primary Dark
            // '#80D2EC', //  9: Primary Light*
            // '#DEF7FF', // 10: Primary Lighter
            // '#F2FBFF', // 11: Primary Lightest

            // '#0c4052', //  6: Primary Darkest
            // '#396171', //  7: Primary Darker*
            // '#628493', //  8: Primary Dark
            // '#89a9b6', //  9: Primary Light*
            // '#b3cfda', // 10: Primary Lighter
            // '#def7ff', // 11: Primary Lightest

            // '#0c4052', //  6: Primary Darkest
            // '#106480', //  7: Primary Darker*
            // '#2589aa', //  8: Primary Dark
            // '#57afcd', //  9: Primary Light*
            // '#96d3e9', // 10: Primary Lighter
            // '#def7ff', // 11: Primary Lightest


            '#08519c', //  6: Primary Darkest
            '#3182bd', //  7: Primary Darker*
            '#6baed6', //  8: Primary Dark
            '#9ecae1', //  9: Primary Light*
            '#c6dbef', // 10: Primary Lighter
            '#eff3ff', // 11: Primary Lightest

            '#C9461A', // 12: Accent Darkest
            '#E85424', // 13: Accent Darker*
            '#E87A55', // 14: Accent Dark
            '#F8A278', // 15: Accent Light*
            '#F4C7B0', // 16: Accent Lighter
            '#F7E6DE', // 17: Accent Lightest

            '#000000', // 18: Gray Darkest
            '#2C2C2C', // 19: Gray Darker
            '#504F52', // 20: Gray Dark
            '#878787', // 21: Gray Light
            '#B4B4B4', // 22: Gray Lighter
            '#D0D0D0', // 23: Gray Lightest
            '#FFFFFF'
        ], // 24: White,
        credits: {
            enabled: false // Credits limited to one line, so we use subtitle for footnote
        },
        title: {
            /*text: null,*/
            useHTML: true,
            align: 'left'
        },
        subtitle: {
            /*text: null,*/
            useHTML: true,
            align: 'left',
            verticalAlign: 'bottom',
            x: 0,
            y: 20,
            floating: false,
            style: {
                color: '#909090',
                fontSize: '10px',
                lineHeight: '1em'
            }
        },

        plotOptions: {
            series: {
                dataLabels: {
                    style: {
                        textShadow: 'none'
                    }
                }
            },
            map: {
                borderColor: "#FFF",
                states: {
                    hover: {
                        color: "#FFF7AA"
                    }
                }
            }
        },
        chart: {
            backgroundColor: "rgba(255,255,255,.8)",
            borderRadius: 5,
            spacingBottom: 60,
            events: {
                load: function() {

                    // If not exporting, then setTitle.
                    /*If we do this when exporting, it will overwrite the title with undefined, since the closure doesn't work?*/
                    if (this.options.chart.forExport === undefined) {
                        var figureText = getFigureText(this);
                        this.setTitle({
                            text: figureText.title
                        }, { // Subtitle - Figure Note
                            text: figureText.footnote
                        });
                    }

                },
                beforePrint: function() {
                    /* This function gets called before being printed. Use it
                    to change the formatting, for example. */

                },
                afterPrint: function() {
                    // Scroll to nearest article element of printed chart
                    scrollTo($(this.renderTo).closest('article'));

                }
            }
        },
        exporting: {
            // Different settings for exporting
            allowHTML: true,
            sourceHeight: 600,
            sourceWidth: 600,
            chartOptions: {
                chart: {
                    marginTop: 120,
                    spacingTop: 10,
                    spacingLeft: 50,
                    spacingRight: 50,
                    spacingBottom: 100
                },
                plotOptions: {
                    // For example, you could display data labels when exporting line charts

                    map: {},
                    column: {

                    },
                    line: {}
                },
                title: {
                    style: {
                        // "display": "inline"
                        // "font-size": "14px",
                        // "line-height": "16px",
                        // "margin-bottom": "-100px"
                    },
                    useHTML: true
                },
                subtitle: { // subtitle is actually the notes
                    style: {
                        // "font-size": "10px",
                        // "font-style": "italic",
                        // "line-height": "11px"
                    },
                    useHTML: true
                },

                legend: {
                    itemStyle: {
                        "fontSize": "12px"
                    }
                },
                yAxis: {
                    visible: true
                }

            },
            buttons: {
                contextButton: {
                    menuItems: [{
                        text: 'Print chart',
                        onclick: function() {
                            console.log('printing', this);
                            this.print();
                        }
                    }, {
                        text: 'Save as PDF',
                        onclick: function() {
                            this.exportChart({
                                filename: $(this.container).closest('article')
                                    .attr('data-filename'),
                                type: "application/pdf"
                            });
                        }
                    }, {
                        text: 'Save as JPG',
                        onclick: function() {
                            this.exportChart({
                                filename: $(this.container).closest('article')
                                    .attr('data-filename'),
                                type: "image/jpeg",

                            });
                        }
                    }, {
                        text: 'Save as PNG',
                        onclick: function() {
                            this.exportChart({
                                filename: $(this.container).closest('article')
                                    .attr('data-filename'),
                                type: "image/png"
                            });
                        }
                    }]
                }
            }
        },
    });
}

/* This function returns the title, subtitle, sources, and notes for a given figure,
pulling them from the <caption> tags of the data table, where they are stored after
having been read in from the markdown files. */
function getFigureText(chart) {

    // Use jQuery to select the data table with the ID matching that of the chart's closest slide-figure element
    var $datatable = $("#" +
        $(chart.container).closest('.slide-figure, .figure-tab-pane').first().attr('id') +
        "-data");

    // Once we've selected the right table, pull out the relevant text
    var title = $datatable.find('caption .figure-title');
    var subtitle = $datatable.find('caption .figure-subtitle');
    var sources = $datatable.find('caption .figure-sources');
    var notes = $datatable.find('caption .figure-notes');

    // Create new elements to use as the figure title and footnote
    /* To get around a limitation of Highcharts, we use the "title" to contain both
    the title and the subtitle, using HTML to allow for styling */
    var figureTitle = "<div class='figure-title-container'>" +
        (title.text().length > 0 ?
            "<h4 class='figure-figure-title figure-title figure-text'>" +
            title.html().trim() +
            "</h4>" : "") +
        (subtitle.text().length > 0 ?
            "<h6 class='figure-figure-subtitle figure-subtitle figure-text'>" +
            subtitle.html().trim() +
            "</h6>" : "") + "</div>";
    var figureFootnote = "<div class='figure-footnote-container'>" +
        (sources.text().length > 0 ?
            "<p class='figure-figure-sources figure-sources figure-footnote figure-text'>" +
            sources.html().trim() +
            "</p>" : "") +
        (notes.text().length > 0 ?
            "<p class='figure-figure-notes figure-notes figure-footnote figure-text'>" +
            notes.html().trim() +
            "</p></div>" : "");

    // console.log("Figure title:", figureTitle, "Footnote", figureFootnote);
    return {
        title: figureTitle,
        footnote: figureFootnote
    };
}





/*
Define group Columns function

This function takes two columns and converts them into the format required by
grouped-categories.js:

[{
    name: "Parent category name",
    categories: ["child", "category", "values"]
}]

parent_cat is an array representing the column of values for the parent category
(aka supercategory).

child_cat is an array representing the column of values for the child category.

This function assumes the columns are laid out as they would be to make a stacked
bar graph in Excel, namely:

"Parent Category Name"    "Child Category Name"
"Parent value 1"            "Child value 1"
null                        "Child value 2"
"parent Value 2"            "Child value 1"
null                        "Child value 2"

So, the parent category is null whenever that row's child value is part of the
same parent category; in this case, we need to turn this into:

[{
    name: "Parent value 1",
    categories: ["Child value 1", "Child value 2"]
}, {
    name: "Parent value 2",
    categories: ["Child value 1", "Child value 2"]
}]

So, we go through each element of the parent category array and, if that element
is not null,
*/
/* This function takes two columns that have blank cells in the first column
for repeated super-categories, like we use for grouped column charts in Excel,
and makes groups that will work with the grouped_categories extension to Highcharts */
function group2Cols(parent_cat, child_cat) {
    // Create empty array, all_categories, to contain all the category objects
    var all_categories = [];
    var working_category = {}; // start off with working category as empty object

    for (i = 1; i < parent_cat.length; i++) { // Start at one because first row is header
        // If parent category is blank, get from previous row
        if (!parent_cat[i]) {
            parent_cat[i] = parent_cat[i - 1];
        }

        // If string, convert pipes to newlines; otherwise, convert to string
        if ($.type(parent_cat[i]) === "string") {
            parent_cat[i] = parent_cat[i].split("|").join("<br>");
        } else {
            parent_cat[i] = parent_cat[i].toString();
        }

        /* If working_category has a name element (i.e. is not empty, as when we start)
                and that name is the same as the current parent category value, i.e.
                    we're continuing the same parent category
                and the child category value on the same row is not already in the categories
                    array for that parent (do we actually want this condition?)
            Then, we add the child category to the working category object

            If NOT, then we add the working category to the all_categories array
            and create a NEW working category object
        */
        if (working_category.name && working_category.name == parent_cat[i]) {
            // Same super-category
            var child_value = child_cat[i];

            if (working_category.categories.indexOf(child_cat[i]) < 0) {
                working_category.categories.push(child_value.toString());
            }
        } else {
            // New category; add complete category to array, make new empty object
            if (working_category.name) { // working category object exists, so add to all_categories
                all_categories.push(working_category);
            }
            // Initialize new working category object
            working_category = {
                name: parent_cat[i],
                categories: [child_cat[i].toString()]
            };
        }
    }
    // Push the final working category to all_categories
    all_categories.push(working_category);
    return all_categories;
}


/* Function to take column array and create a grouped categories array */
function groupColumns(columns, groupedIndices) {
    //console.log("Grouping columns", JSON.stringify(columns, null, 2), groupedIndices);
    var groupCols = $.map(groupedIndices, function(i, c) {
        //console.log(i, c, JSON.stringify(columns[c], null, 2));
        return [columns[c]];
    });
    /*
    var categories = groupCols[groupCols.length-1];
    console.log(categories);
    for (i = groupCols.length-2; i > 0; i--) {
        categories = group2Cols(groupCols[i-1], categories);
    }
    return categories;*/
    //console.log("GROUP COLS", JSON.stringify(groupCols.slice(0), null, 2));
    var categories = groupCols.pop(); // get last category; child category
    //console.log("Categories before group", JSON.stringify(groupCols.slice(0), null, 2));
    while (supercategory = groupCols.pop()) {
        categories = group2Cols(supercategory, categories);
        //console.log("Categories after group", JSON.stringify(categories, null, 2), supercategory);
    }
    return categories;


}

/* This function resizes all the figures to be the height of their parent.

This allows the actual size of the slides to be set at runtime, while the
figures will be expanded to fit them.

Note that right now it assumes a full-screen layout; we assume for example
that .slide-figure-right is actually on the right, rather than having wrapped
around to be on the bottom, as happens if the screen is not wide enough. */
function resizeAll() {
    // TODO: Need to do the resizing differently for small screens
    $(
        '.slide-figure-container.slide-figure-left, ' +
        '.slide-figure-container.slide-figure-right').each(function() {
        var h = $(this).parent().height();
        $(this).height(h);
    });
    $('.slide-figure-container.slide-figure-bottom, ' +
        '.slide-figure-container.slide-figure-bottom-wide').each(function() {
        var h = $(this).parent().height() - $(this).parent().find('.slide-text-container').height();
        $(this).height(h);
    });
    $('.slide-figure-container.slide-title-over-text-and-figure').each(function() {
        var h = $(this).parent().height() -
            $(this).parent().find('.slide-title-container').height() -
            $(this).parent().find('.slide-text-container').height();
        $(this).height(h);
    });


    $.each(Highcharts.charts, function() {
        // console.log("Resizing this: ", this, typeof this);
        if ("redraw" in this) {
            //console.log("redrawing");
            this.redraw();
            this.reflow();
        }
    });
}
