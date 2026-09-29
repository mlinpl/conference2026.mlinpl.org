// Add to calendar: .ics download and dropdown handling
(function () {
    var VTIMEZONE = [
        'BEGIN:VTIMEZONE',
        'TZID:Europe/Warsaw',
        'BEGIN:DAYLIGHT',
        'TZOFFSETFROM:+0100',
        'TZOFFSETTO:+0200',
        'TZNAME:CEST',
        'DTSTART:19700329T020000',
        'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=-1SU',
        'END:DAYLIGHT',
        'BEGIN:STANDARD',
        'TZOFFSETFROM:+0200',
        'TZOFFSETTO:+0100',
        'TZNAME:CET',
        'DTSTART:19701025T030000',
        'RRULE:FREQ=YEARLY;BYMONTH=10;BYDAY=-1SU',
        'END:STANDARD',
        'END:VTIMEZONE'
    ];

    function escapeText(text) {
        return (text || '')
            .replace(/\\/g, '\\\\')
            .replace(/;/g, '\;')
            .replace(/,/g, '\\,')
            .replace(/\r?\n/g, '\\n');
    }

    function buildIcs(d) {
        var stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d+/, '');
        return [
            'BEGIN:VCALENDAR',
            'VERSION:2.0',
            'PRODID:-//ML in PL//Conference Agenda//EN',
            'CALSCALE:GREGORIAN',
            'METHOD:PUBLISH'
        ].concat(VTIMEZONE, [
            'BEGIN:VEVENT',
            'UID:' + d.calUid,
            'DTSTAMP:' + stamp,
            'DTSTART;TZID=Europe/Warsaw:' + d.calDate + 'T' + d.calStart,
            'DTEND;TZID=Europe/Warsaw:' + d.calDate + 'T' + d.calEnd,
            'SUMMARY:' + escapeText(d.calTitle),
            'LOCATION:' + escapeText(d.calLocation),
            'DESCRIPTION:' + escapeText(d.calDetails),
            'END:VEVENT',
            'END:VCALENDAR'
        ]).join('\r\n');
    }

    document.addEventListener('click', function (e) {
        var button = e.target.closest && e.target.closest('.cal-ics');
        if (button) {
            var data = button.closest('.cal-add').dataset;
            var blob = new Blob([buildIcs(data)], { type: 'text/calendar;charset=utf-8' });
            var link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = data.calTitle.replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-').slice(0, 60) + '.ics';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            setTimeout(function () { URL.revokeObjectURL(link.href); }, 1000);
        }

        // Close open menus when clicking elsewhere or picking an option
        var current = e.target.closest && e.target.closest('.cal-menu');
        var picked = e.target.closest && e.target.closest('.cal-menu-list');
        document.querySelectorAll('.cal-menu[open]').forEach(function (menu) {
            if (menu !== current || picked) {
                menu.removeAttribute('open');
            }
        });
    });
})();
