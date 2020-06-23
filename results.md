---
layout: default
title: Results
---

# Publications 

<a href="http://inspirehep.net/search?p=find+collaboration+gluex"> List of GlueX publications on INSPIRE-HEP </a>

<!-- loop over paper files in _data directory -->
{% for paper_hash in site.data.papers %}
{% assign papers = paper_hash[1] %}
{% for item in papers %}
{%- if item.link -%}
<a href="{{ item.link }}"> {{ item.title }} </a> {{ item.citation }}, arXiv:{{ item.arXiv }} 
{%- endif -%}
{% endfor %}
{% endfor %}

# Recent Plenary Talks

<a href="https://halldweb.jlab.org/wiki/index.php/GlueX_Talks"> List of GlueX talks </a>

<!-- loop over talks in _data directory -->
{% for item in site.data.talks %}
<a href="{{ item.link }}"> {{ item.title }} </a>, {{item.conference}} ({{ item.name }})
{% endfor %}


