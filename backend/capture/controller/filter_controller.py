from flask import Blueprint, jsonify, request
import service.filter_service as filter_service

filter_blueprint = Blueprint('filter_blueprint', __name__)

@filter_blueprint.route('',  methods = ['POST'])
def change_filter():
    filter_service.change_filter(request.json["filter"])
    print(f"Current filter: {filter_service.current_filter}")
    return jsonify({"success": True})

@filter_blueprint.route('',  methods = ['GET'])
def get_filter():
    return jsonify({"current_filter": filter_service.current_filter})