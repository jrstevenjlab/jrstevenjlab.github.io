---
layout: default
title: Results
---

# Publications 

<a href="http://inspirehep.net/search?p=find+collaboration+gluex"> List of GlueX publications on INSPIRE-HEP </a>

<!-- specific order for papers from YAML-->
{% for i in ( 1..site.data.papers.size ) %}
{% assign j = site.data.papers.size | minus: i %}
{% assign j = j | plus: 1 %}

<!-- loop over paper files in _data directory -->
{% for paper_hash in site.data.papers %}
{% assign papers = paper_hash[1] %}
{% for item in papers %}
{%- if item.order == j -%}
<a href="{{ item.link }}"> {{ item.title }} </a> {{ item.citation }}, arXiv:{{ item.arXiv }}
{% assign i = i | plus:1 %}
{%- endif -%}
{% endfor %}
{% endfor %}
{% endfor %}

# Recent Plenary Talks

<a href="https://halldweb.jlab.org/wiki/index.php/GlueX_Talks"> List of GlueX talks </a>

<!-- loop over talks in _data directory -->
{% for item in site.data.talks %}
<a href="{{ item.link }}"> {{ item.title }} </a>, {{item.conference}} ({{ item.name }})
{% endfor %}


