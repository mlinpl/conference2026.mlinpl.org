/*!
 * ML in PL Jekyll Theme - FAQ accordion
 * Toggles a FAQ answer panel and flips the +/x icon on click.
 */
$(function() {
    $('.faq-question').on('click', function(event) {
        event.preventDefault();

        var $question = $(this);
        var $panel = $($question.attr('href'));

        $panel.stop().slideToggle(250);
        $question.toggleClass('faq-question-active');
        $question.attr('aria-expanded', $question.hasClass('faq-question-active'));
    });
});
