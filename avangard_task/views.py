from flask import jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource

from . import api, app, db
from .error_handlers import InvalidAPIUsage
from .models import DataModel, User

bcrypt = Bcrypt()


class DataResource(Resource):
    @jwt_required()
    def post(self):
        """Этот эндпоинт позволяет пользователю создавать
        новые записи с конфиденциальными данными."""
        try:
            data = request.get_json()
            new_data = DataModel(name=data['name'], value=data['value'])
            db.session.add(new_data)
            db.session.commit()
            data = {
                'id': new_data.id
            }
            return data, 201

        except KeyError as e:
            return {'Ошибка': f'Отсутствует обязательное поле: {e}'}, 400
        except Exception as e:
            return {'Ошибка': str(e)}, 500

    @jwt_required()
    def get(self, id=None):
        """Этот эндпоинт возвращает список всех конфиденциальных данных.
        А если пользователь ввел ID в запросе, то возвращаются
        конфиденциальные данные по ID.
        """
        if id is None:
            page = request.args.get('page', default=1, type=int)
            per_page = request.args.get('per_page', default=10, type=int)
            data = DataModel.query.paginate(
                page=page, per_page=per_page, error_out=False
            )

            result = {
                'data': [item.serialize() for item in data.items],
                'total_pages': data.pages,
                'total_items': data.total
            }

            return jsonify(result)
        else:
            data = DataModel.query.get_or_404(id)
            return jsonify(data.serialize())

    @jwt_required()
    def put(self, id):
        """Этот эндпоинт позволяет пользователю обновлять существующие
        конфиденциальные данные."""
        try:
            data = request.get_json()
            db.session.query(DataModel).filter_by(id=id).update(data)
            db.session.commit()
            return jsonify(success=True)

        except KeyError as e:
            return {'Ошибка': f'Отсутствует обязательное поле: {e}'}, 400
        except Exception as e:
            return {'Ошибка': str(e)}, 500

    @jwt_required()
    def delete(self, id):
        """Этот эндпоинт позволяет пользователю удалять существующие
        конфиденциальные данные."""
        data = DataModel.query.get_or_404(id)
        db.session.delete(data)
        db.session.commit()
        return jsonify(success=True)


api.add_resource(DataResource, '/data', '/data/<int:id>')


@app.route('/register', methods=['POST'])
def register_user():
    """Этот эндпоинт позволяет зарегистрироваться в системе."""
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'username' not in data:
        raise InvalidAPIUsage('<username> является обязательным полем!')
    if 'password' not in data:
        raise InvalidAPIUsage('<password> является обязательным полем!')

    username = data['username']
    password = data['password']

    if User.query.filter_by(username=username).first():
        return InvalidAPIUsage('Пользователь уже зарегистрирован!')
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return {'Сообщение': 'Пользователь успешно создан'}, 201


@app.route('/login', methods=['POST'])
def login():
    """Этот эндпоинт позволяет войти в систему."""
    data = request.get_json()

    if data is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'username' not in data:
        raise InvalidAPIUsage('<username> является обязательным полем!')
    if 'password' not in data:
        raise InvalidAPIUsage('<password> является обязательным полем!')

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        raise InvalidAPIUsage('Неправильное имя пользователя или пароль', 401)

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


if __name__ == '__main__':
    app.run(debug=True)
