{% extends 'base.html' %}

{% block content %}
    <div class="line course-item-header">
        <div class="middle">

            <h2>{{ course.title }}</h2>
            <p>
                {{ course_lesson_count }} уроков

            </p>

        </div>
    </div>
    <div class="middle">
        <div class="course-item-mini">
            <div class="course-item-mini-left">
                <img src="/media/{{ course.logo }}" alt="">
            </div>
            <div class="course-item-mini-right">
                <div class="course-item-mini-right-title">
                    {{ course.title}} / {{ first_course_item.title }}
                </div>
                <div class="course-item-mini-right-cat">
                    <a href="#" class="btn btn-outline-dark"> {{ course.category.title }} </a>
                    {% if active_user %}
                        {% if user_have_course %}
                            <a href="#" class="btn btn-outline-success"> Вы начали курс </a>
                            {% else %}
                                <br><br>
                                <form action="/course/{{ course.id }}/" method="POST">
                                 {% csrf_token %}
                                    <input type="hidden" name="action" value="start_course">
                                    <button class="btn btn-outline-success"> Начать курс </button>
                                </form>
                        {% endif %}
                    {% endif %}
                </div>
                <div class="course-item-mini-right-desc">
                   {{ course.description }}
                </div>


            </div>
        </div>
    </div>
    <div class="middle">
        <div class="course-item-info">
            <p>{{ first_course_item.title}}
            </p>
            <div class="course-item-info-item">
                {{ first_course_item.description }}<br><br>

                {% if first_course_item.logo %}
                    <p>
                        <img src="/media/{{first_course_item.logo}}" alt="">
                    </p>
                {% endif %}
             {% if first_course_item.video_link %}
                    <iframe width="560" height="315" src="https://www.youtube.com/embed/{{ first_course_item.video_link }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                {% endif %}
            </div>
        </div>


        {% for p in paragraphs %}
        <div class="course-item-info">
            <p>{{ p.title }}
            </p>
            <div class="course-item-info-item">
                {{ p.description1 }}
                {{ p.description2 }}<br>
                {% if p.logo %}
                    <p style="text-align: center">
                    <img src="/media/{{ p.logo}}" alt="" class="center">
                    </p>
                {% endif %}

                {% if p.video_link %}
                    <iframe width="560" height="315" src="https://youtu.be/{{ p.video_link }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                {% endif %}

                {{ p.description3 }}
            </div>
        </div>
        {% endfor %}
        <div class="course-item-pager">
            {% for i in lesson_counts %}
                <a href="/course/{{ course.id }}/?lesson={{ i }}"{% if active_lesson_number == i %} class="active" {% endif %}>{{ i }}</a>
            {% endfor %}


        </div>

     </div>








{% endblock %}