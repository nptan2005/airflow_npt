from flask import Blueprint, request, jsonify
from sqlalchemy.orm import sessionmaker
from airflow.utils.db import provide_session
from custom_config_plugin.models import AppSetting
from airflow.models import Base
from sqlalchemy import create_engine

# Lấy kết nối từ Airflow config
from airflow.settings import SQL_ALCHEMY_CONN

custom_config_api = Blueprint(
    "custom_config_api",
    __name__,
    url_prefix="/api/custom_config"
)

# Tạo engine và session
engine = create_engine(SQL_ALCHEMY_CONN)
Session = sessionmaker(bind=engine)

# GET all
@custom_config_api.route("/settings", methods=["GET"])
def get_settings():
    session = Session()
    settings = session.query(AppSetting).all()
    result = [
        {
            "id": s.id,
            "environment": s.environment,
            "key": s.key,
            "value": s.value,
            "description": s.description,
            "created_at": str(s.created_at),
            "updated_at": str(s.updated_at),
        }
        for s in settings
    ]
    session.close()
    return jsonify(result)

# INSERT
@custom_config_api.route("/settings", methods=["POST"])
def insert_setting():
    data = request.json
    session = Session()
    setting = AppSetting(
        environment=data.get("environment", "default"),
        key=data["key"],
        value=data.get("value"),
        description=data.get("description"),
    )
    session.add(setting)
    session.commit()
    result = {
        "id": setting.id,
        "environment": setting.environment,
        "key": setting.key,
        "value": setting.value,
        "description": setting.description,
        "created_at": str(setting.created_at),
        "updated_at": str(setting.updated_at),
    }
    session.close()
    return jsonify(result), 201

# UPDATE
@custom_config_api.route("/settings/<int:setting_id>", methods=["PUT"])
def update_setting(setting_id):
    data = request.json
    session = Session()
    setting = session.query(AppSetting).get(setting_id)
    if not setting:
        session.close()
        return jsonify({"error": "Not found"}), 404
    setting.environment = data.get("environment", setting.environment)
    setting.key = data.get("key", setting.key)
    setting.value = data.get("value", setting.value)
    setting.description = data.get("description", setting.description)
    session.commit()
    result = {
        "id": setting.id,
        "environment": setting.environment,
        "key": setting.key,
        "value": setting.value,
        "description": setting.description,
        "created_at": str(setting.created_at),
        "updated_at": str(setting.updated_at),
    }
    session.close()
    return jsonify(result)

# DELETE
@custom_config_api.route("/settings/<int:setting_id>", methods=["DELETE"])
def delete_setting(setting_id):
    session = Session()
    setting = session.query(AppSetting).get(setting_id)
    if not setting:
        session.close()
        return jsonify({"error": "Not found"}), 404
    session.delete(setting)
    session.commit()
    session.close()
    return jsonify({"status": "deleted", "id": setting_id})