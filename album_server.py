from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    """
    Принимаем исполнителя и выводим список его альбомов
    """
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов исполнителя '{}' не найдено!".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Количество альбомов исполнителя '{}' = {} <br>".format(artist, len(album_names))
        result += "Список альбомов исполнителя - {} :<br><b>".format(artist)
        result += "<b><br>".join(album_names)
    return result

@route("/albums", method="POST")
def add_albums():
    # Формируем словарь для значений
    new_album={
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year":int(request.forms.get("year"))
    }
    # Выполняем проверку на год между 1900 и 2020 (Врядли старше 1900 альбомы выпускали)
    if ((new_album["year"]<1900) and (new_album["year"]>2020)):
        message = "Ошибка при вводе года выпуска альбома!"
        result = HTTPError(409, message)
        return result
    
    # Делаем запрос на наличие в базе такого альбома у этого исполнителя
    albums_res = album.find_new(new_album["artist"],new_album["album"])
    # Если результат не ноль, выдаем сообщение и не добавляем запись в базу
    if (albums_res != 0):
        message = "Альбом '{}' исполнителя '{}' имеется в базе!".format(new_album["album"],new_album["artist"])
        result = HTTPError(409, message)
    # Иначе вызываем функции записи в базу и передаем ей наш словарь
    else:
        result = album.safe_album(new_album)
    # Выводим результат
    return result
    

if __name__=="__main__":
    run(host="localhost", port=8080, debug=True)
    
    
