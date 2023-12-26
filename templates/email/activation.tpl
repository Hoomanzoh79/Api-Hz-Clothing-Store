{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
You can verify your account with the given link:

127.0.0.1:8000/accounts/api/v1/activation/confirm/{{token}}/

{% endblock %}