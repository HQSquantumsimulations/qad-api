{{ fullname | escape | underline}}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

   {% if methods or attributes %}

   .. rubric:: Member Overview

   {% block class_toc %}

   {% if methods %}
   {% block methods %}

   *Methods:*

   .. autosummary::
   {% for item in methods %}
      ~{{ name }}.{{ item }}
   {%- endfor %}

   {% endblock %}
   {% endif %}

   {% if attributes %}
   {% block attributes %}

   *Attributes:*

   .. autosummary::
   {% for item in attributes %}
      ~{{ name }}.{{ item }}
   {%- endfor %}

   {% endblock %}
   {% endif %}

   {% endblock %}
   {% endif %}

   .. rubric:: Member's Documentation

