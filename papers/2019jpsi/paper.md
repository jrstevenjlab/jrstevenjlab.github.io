---
layout: default
---

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript">
</script>

{% for paper_hash in site.data.papers %}
{% assign papers = paper_hash[1] %}
{% for item in papers %}
{% if item.name == "2019jpsi" %}
# {{ item.title }}  
### Abstract:  
{{ item.abstract }}
### Journal: [{{ item.citation }}](https://doi.org/{{ item.doi }})  
### arXiv: [arXiv:{{ page.arXiv }}](https://arxiv.org/abs/{{ item.arXiv }})  
### HEPdata: [link](https://www.hepdata.net/record/{{ item.hepdata }})   
{% endif %}
{% endfor %}
{% endfor %}

<table>
    <tbody>
    {% for paper_hash in site.data.papers %}
    {% assign papers = paper_hash[1] %}
    {% for item in papers %}
    {%- if item.figure -%}
        <tr>
            <td class="figure" id="Figure_{{item.figure}}">
                    <a href="fig{{item.figure}}.png">
                    <img src="fig{{item.figure}}.png"></a>
                    <br>
                    <a href="fig{{item.figure}}.png">png</a>
                    <a href="fig{{item.figure}}.pdf">pdf</a>
            </td>
            <td class="legend">
                <a href="{{ page.url }}#Figure_00{{item.figure}}"><i>Figure {{item.figure}}</i>
                </a>
                <br> {{item.caption}}
            </td>
        </tr>
    {%- endif -%}
    {% endfor %}
    {% endfor %}
    </tbody>
</table>
