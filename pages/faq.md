---
layout: page
title: Frequently Asked Questions
permalink: /faq
---

Here are answers to the questions we get asked most often. 
Can't find what you're looking for? [Get in touch]({{ "/#contact" | relative_url }}).

<div class="row">
    <div class="col-xs-12 col-sm-8 col-sm-offset-2">
        <div class="faq-list">
            {% for item in site.data.faq %}
            <div class="faq-item">
                <a href="#faq-{{ forloop.index }}" class="faq-question collapsed" data-toggle="collapse" role="button" aria-expanded="false" aria-controls="faq-{{ forloop.index }}">
                    <p class="faq-question-text">{{ item.question }}</p>
                    <span class="faq-icon"><i class="fa-solid fa-chevron-down"></i></span>
                </a>
                <div id="faq-{{ forloop.index }}" class="faq-panel collapse">
                    <p>{{ item.answer }}</p>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>
