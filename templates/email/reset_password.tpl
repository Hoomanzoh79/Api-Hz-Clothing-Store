{% extends "mail_templated/base.tpl" %}

{% block subject %}
Hello {{ user }}
{% endblock %}

{% block body %}
You can reset your password with the given link:

127.0.0.1:8000/accounts/api/v1/password/reset/confirm/{{token}}/

{% endblock %}