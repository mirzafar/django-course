{% extends 'api/base.html' %}


{% block content %}
    <?php
    includes 'upload.php';

    ?>
    <form action="/api/courses/add/" method="POST">
    {% csrf_token %}
        <table border="1">
            <tr>
                <td>Название</td>
                <td><input type="text" value="" name="title"></td>
            </tr>
            <tr>
                <td> Категория </td>
                <td>
                    <select name="category_id">
                        <option value="0">Выберите</option>
                        {% for cat in categories %}
                            <option value="{{ cat.id }}">{{ cat.title }}</option>
                        {% endfor %}
                    </select>
                </td>
            </tr>
            <tr>
                <td>Количество уроков</td>
                <td><input name="lessons_count" value="0" type="number"></td>
            </tr>
            <tr>
                <td>Описание</td>
                <td><textarea name="description" rows="4" cols="50"></textarea></td>
            </tr>
            <tr>
                <td>инфо1</td>
                <td><input name="info1" type="text"></td>
            </tr>
            <tr>
                <td>инфо1_текст</td>
                <td><textarea name="info1_text" rows="4" cols="50"></textarea></td>
            </tr>
            <tr>
                <td>ЛОГО</td>
                <td>
                    <img style="width: 300px;" src="/media/{{ item.logo }}" alt="">
                    <input type="hidden" name="logo" value="{{ item.logo }}">
                    <input type="file" id="category_logo" data-name="logo">
                </td>
            </tr>
            <tr>
                <td>New logo</td>
                <td>
                    <div class="container" align="center">
                        <div class="row">
                            <div>&nbsp;</div>
                            <div class="col-md-4">
                                <div class="image_area">
                                    <form method="post">
                                        <label for="upload_image">
                                            <img src="upload/user.png" id="uploaded_image" class="img-responsive img-circle" />
                                            <div class="overlay">
                                                <div class="text">Click to Change Profile Image</div>
                                            </div>
                                            <input type="file" name="image" class="image" id="upload_image" style="display:none" />
                                        </label>
                                    </form>
                                </div>
                            </div>
                        <div class="modal fade" id="modal" tabindex="-1" role="dialog" aria-labelledby="modalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-lg" role="document">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Crop Image Before Upload</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                            <span aria-hidden="true">×</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        <div class="img-container">
                                            <div class="row">
                                                <div class="col-md-8">
                                                    <img src="" id="sample_image" />
                                                </div>
                                                <div class="col-md-4">
                                                    <div class="preview"></div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" id="crop" class="btn btn-primary">Crop</button>
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </td>
            </tr>
            <tr>
                <td>Статус</td>
                <td><input type="number" value="0" name="status"></td>
            </tr>
            <tr>
                <td></td>
                <td><input type="checkbox" id="subscribeNews" name="is_free"><label for="subscribeNews">Is free</label></td>
            </tr>
            <tr>
                <tr>
                    <td><input type="hidden" name="action" value="add"></td>
                    <td><button>Сохранить</button></td>
                </tr>
            </tr>
        </table>
    </form>
{% endblock %}


