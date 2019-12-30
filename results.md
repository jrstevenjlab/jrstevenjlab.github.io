---
layout: default
title: Results
---
<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript">
</script>

# Papers 

<!-- loop over paper files in _data directory -->
{% for paper_hash in site.data.papers %}
{% assign papers = paper_hash[1] %}
{% for item in papers %}
{%- if item.link -%}
[{{ item.title }}]({{ item.link }}) {{ item.citation }}, arXiv:{{ item.arXiv }} 
{%- endif -%}
{% endfor %}
{% endfor %}
