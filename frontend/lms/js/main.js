// const calendar = new VanillaCalendar('#calendar', {
//     date: new Date('2023-02-13'),
//     settings: {
//         iso8601: false,
//         lang: 'define',
//         locale: {
//             months: ['Қаңтар', 'Ақпан', 'Наурыз', 'Сәуір', 'Мамыр', 'Маусым', 'Шілде', 'Тамыз', 'Қыркүйек', 'Қазан', 'Қараша', 'Желтоқсан'],
//             weekday: ['Се', 'Же', 'Ду', 'Сй', 'Ср', 'Бе', 'Жұ'],
//         },
//     },
// });
// calendar.init();

const calendarKZLang = new VanillaCalendar('#calendar-kz-lang', {
    settings: {
        lang: 'define',
        iso8601: true,
    },
    locale: {
        months: ['Қаңтар', 'Ақпан', 'Наурыз', 'Сәуір', 'Мамыр', 'Маусым', 'Шілде', 'Тамыз', 'Қыркүйек', 'Қазан', 'Қараша', 'Желтоқсан'],
        weekday: [ 'Же', 'Дү', 'Сй', 'Сә', 'Бе', 'Жұ','Се'],
        // Example:
        // months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
        // weekday: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
        // Note that the weeks array must start with Sunday, this does not affect ISO 8601.
    },
});
calendarKZLang.init();