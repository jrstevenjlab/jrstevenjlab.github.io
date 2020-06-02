---
layout: default
title: Results
---
 
 <a href="http://inspirehep.net/search?p=find+collaboration+gluex"> List of GlueX publications on INSPIRE-HEP </a>

# Physics Publications 

<!-- loop over paper files in _data directory -->
{% for paper_hash in site.data.papers %}
{% assign papers = paper_hash[1] %}
{% for item in papers %}
{%- if item.link -%}
<a href="{{ item.link }}"> {{ item.title }} </a> {{ item.citation }}, arXiv:{{ item.arXiv }} 
{%- endif -%}
{% endfor %}
{% endfor %}
