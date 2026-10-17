---
layout: page
title: Contributed Talk and Poster Awards
permalink: /cfc-awards
---

We are thrilled to announce the winners of the Best Contributed Talk and Best Poster Awards at {{ site.inline-logo }}. The awards were decided by the community voting, and this year the competition was very close!

{% comment %} Look up the winners by id, keeping the order from cfc-awards.yml {% endcomment %}
{% assign award_talks = "" | split: "" %}
{% for id in site.data.cfc-awards.talks %}
{% assign talk = site.data.contributed-talks | where: "id", id | first %}
{% assign award_talks = award_talks | push: talk %}
{% endfor %}
{% assign award_posters = "" | split: "" %}
{% for id in site.data.cfc-awards.posters %}
{% assign poster = site.data.posters | where: "id", id | first %}
{% assign award_posters = award_posters | push: poster %}
{% endfor %}

{% include talks.html talks-title="/ Best Contributed Talk Award" talks-data=award_talks talk-title-prefix="Contributed Talk" %}

{% include talks.html talks-title="/ Best Poster Award" talks-data=award_posters talk-title-prefix="Poster" %}

Congratulations to the winners, and thank you to all who made {{ site.inline-logo }} a memorable experience! 