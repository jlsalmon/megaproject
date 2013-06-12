function initCalendar() {
    console.log('initCalendar()');

    var date = new Date();
    var d = date.getDate();
    var m = date.getMonth();
    var y = date.getFullYear();

    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },

        eventSources: [
            {
                url: '/events',
                type: 'POST',
                async: false,
                data: {
                    custom_param1: 'something',
                    custom_param2: 'somethingelse'
                },
                beforeSend: function (data) {
                    console.log('eventSources beforeSend()');

                    if (typeof data === "undefined") {
                        console.log('it was undefined')
                        return false;
                    }
                    console.log(data);
                },
                error: function (data) {
                    console.log('eventSources error() ' + data);
                    //alert('there was an error while fetching events! ' + data);
                    //console.log(e + ' ' + s + ' ' + t);
                },
                success: function (data) {
                    console.log('eventSources success()');
                    //console.log('data: ' + data)
                }
                //className: 'popover'
                //color: '#eee',     // a non-ajax option
                //textColor: 'black' // a non-ajax option
            }
            // any other sources...

            //'http://www.google.com/calendar/feeds/mccrustin%40gmail.com/public/basic'
        ],

        eventClick: function (event, element) {
            // opens events in a popup window
            console.log('eventClick()');
            console.log(event);
            console.log(element);
            $.ajax({
                url: '/task-overview',
                type: "POST",
                async: false,
                data: { task: event },
                beforeSend: function (data) {
                    console.log('eventClick beforeSend()');
                },
                success: function (data) {
                    console.log('eventClick success()');
                    $('#task-overview').html(data);

                    $('.popover').popover({
                        html: true,
                        trigger: 'hover',
                        content: function () {
                            return $('#popover_content_wrapper').html();
                        }
                    });

                },
                error: function (data) {
                    console.log('eventClick error()');
                }
            });
            return false;
        },

        editable: true,
        selectable: true,
        selectHelper: true,

        select: function (start, end, allDay) {
            var title = prompt('Event Title:');
            if (title) {
                calendar.fullCalendar('renderEvent',
                    {
                        title: title,
                        start: start,
                        end: end,
                        allDay: allDay
                    },
                    true // make the event "stick"
                );
            }
            calendar.fullCalendar('unselect');
        },

        loading: function (bool) {
            if (bool) {
                $('#loading').show();
            } else {
                $('#loading').hide();
            }
        }
    });

}
