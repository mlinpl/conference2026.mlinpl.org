---
layout: page
title: Frequently Asked Questions
permalink: /faq
---

Here are answers to the questions we get asked most often. 
Can't find what you're looking for? [Get in touch]({{ "/#contact" | relative_url }}).

<div class="faq-list">
    {% for item in site.data.faq %}
    <div class="faq-item">
        <a href="#faq-{{ forloop.index }}" class="faq-question collapsed" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="faq-{{ forloop.index }}">
            <span class="faq-question-text">{{ item.question }}</span>
            <span class="faq-icon"><i class="fa-solid fa-chevron-down"></i></span>
        </a>
        <div id="faq-{{ forloop.index }}" class="faq-panel collapse">
            <div class="faq-answer">{{ item.answer }}</div>
        </div>
    </div>
    {% endfor %}
</div>
