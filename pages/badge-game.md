---
layout: page
title: Conference Badge Game
html-title: Conference Badge Game
permalink: /badge-game
---

Welcome to our conference badge game! 
This year each participant's badge contains **one of three symbols**, which are based on their first and last names, and roles:

<div class="row" style="margin-bottom: 30px;">
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px; border: 0;" src="{{ "./images/optimized/badge-game-800x800/decoder.webp" | relative_url }}" alt="decoder symbol">
        <p class="text-center"><strong>decoder</strong></p>
    </div>
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px; border: 0;" src="{{ "./images/optimized/badge-game-800x800/autoencoder.webp" | relative_url }}" alt="autoencoder symbol">
        <p class="text-center"><strong>autoencoder</strong></p>
    </div>
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px; border: 0;" src="{{ "./images/optimized/badge-game-800x800/encoder.webp" | relative_url }}" alt="encoder symbol">
        <p class="text-center"><strong>encoder</strong></p>
    </div>
</div>

<span style="font-size: 1.25em; text-align: center; display: block;">
    <span style="letter-spacing: 5px; font-style: italic;">f</span>(first_name, last_name, role) ∈ {decoder, autoencoder, encoder}
</span>

As in classic machine learning problems, your task is to **collect data** and **discover the unknown mapping function**.
The **first five participants** who correctly predict all the labels for the test set and give a short description of the function will receive special prizes. 

Curious what the game looked like before? See [last year's badge game](https://conference2025.mlinpl.org/badge-game){:target="_blank"} together with its solution.

## / Rules

The rules are simple -- collect as much data as possible and discover the mapping function to accurately predict the labels of the test set. 
Participants who will succeed with their predictions have a chance to win prizes. 
If none of the participants solve the puzzle by the end of the conference, the prizes will be drawn among all participants who get the highest number of correct predictions on the test set.
You can **network with other participants** to collect their names and associated labels and **visit sponsor booths to collect extra data points** that will help you discover the mapping function.

The assigned labels are printed on the back of the badges, so you can ask other participants to show them.

<!-- <div class="row" style="margin-bottom: 30px;">
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px;" src="{{ "./images/optimized/badge-game-800x800/badge-decoder.webp" | relative_url }}">
    </div>
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px;" src="{{ "./images/optimized/badge-game-800x800/badge-autoencoder.webp" | relative_url }}">
    </div>
    <div class="col-xs-4">
        <img class="img-responsive center-block photo" style="margin-bottom: 5px;" src="{{ "./images/optimized/badge-game-800x800/badge-encoder.webp" | relative_url }}">
    </div>
</div> -->

## / Hints

Don't worry if you can't find the pattern right away -- we will provide hints to guide you in solving the mapping function. 
But remember, the faster you solve the puzzle, the higher are your chances of winning.

{% if site.data.badge-game.hints.size > 0 %}
{% for hint in site.data.badge-game.hints %}
- **Hint {{ forloop.index }}:** {{ hint }}
{%- endfor %}
{% endif %}

## / Submit results

Submit your predictions for the test set names by filling out the form -- you can make multiple submissions (under a reasonable limit).
Along with your predictions, include a short description of the function you discovered.

<div align="center" style="margin-bottom: 30px;">
    {% if site.data.badge-game.status == "open" %}
    <a href="{{ site.data.badge-game.form-url }}" class="btn btn-default btn-lg" target="_blank"><i class="fa-solid fa-list"></i> Submit your predictions</a>
    {% else %}
    <a class="btn btn-default btn-lg btn-nonactive" disabled><i class="fa-solid fa-list"></i> Submit your predictions</a>
    <p style="margin-top: 10px;">Submissions are closed.</p>
    {% endif %}
</div>

{% if site.data.badge-game.winners.size > 0 %}
## / Winners

Congratulations to the winners of this year's badge game!
{% for winner in site.data.badge-game.winners %}
{{ forloop.index }}. {{ winner }}
{%- endfor %}
{% endif %}

{% if site.data.badge-game.solution %}
## / Solution

{{ site.data.badge-game.solution }}
{% endif %}
