python manage.py collectstatic

    {% load static %}

        @font-face {
        font-family: "Alice-Regular";
        src: local('Alice-Regular') url('{% static '/fonts/Alice-Regular.ttf' %} format("truetype")') ;
        }

        body {
        font-family: "Alice-Regular";
        }