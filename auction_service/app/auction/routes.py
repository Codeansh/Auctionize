from datetime import datetime
from flask import Blueprint, request, jsonify
import json
from app.auction.models import Auction
from app.auction.schema import AuctionModel
from app.auction.utils import convert_datetime
from bson import ObjectId
from flask_pydantic import validate

auction = Blueprint('auctions', __name__, url_prefix='/auctions')


@auction.route('/', methods=['GET'])
def auctions():
    limit = int(request.args.get('offset', 10))
    offset = int(request.args.get('offset', 0))

    if request.environ.get('is_admin'):
        auction_objects = Auction.objects().skip(offset).limit(limit)
    else:
        raw_query = {'start_time': {'$lt': datetime.utcnow()}, 'end_time': {'$gt': datetime.utcnow()}}
        auction_objects = Auction.objects(__raw__=raw_query).skip(offset).limit(limit)

    if not auction_objects:
        return jsonify({"message": "No auction available"}), 404

    return jsonify(auction_objects), 200


@auction.route('/<auction_id>', methods=['POST'])
def bidding(auction_id: str):
    user_id = request.environ.get('user_id')
    auction_obj = Auction.objects(id=ObjectId(auction_id)).first()

    if not auction_obj:
        return jsonify({"message": "auction not found"}), 404

    if auction_obj.start_time > datetime.utcnow() or auction_obj.end_time < datetime.utcnow():
        return jsonify({"message": "not allowed"}), 403

    bidding_amount = json.loads(request.data).get('bidding_amount')
    if not bidding_amount:
        return jsonify({"message": "bidding_amount is a required field"}), 400

    bidding_amount = float(bidding_amount)

    if bidding_amount > auction_obj.highest_bid:
        auction_obj.update(highest_bid=bidding_amount, user_id=user_id)
        auction_obj = Auction.objects(id=auction_id).first()
        return jsonify(auction_obj), 200

    return jsonify({"message": "invalid bidding amount"}), 400


@auction.route('/create', methods=['POST'])
@validate()
def create_auction(body: AuctionModel):
    if request.environ.get('is_admin'):

        start_time, error = convert_datetime(body.start_time, '%d/%m/%Y %H:%M')
        if error:
            return jsonify({"message": str(error)}), 400

        end_time, error = convert_datetime(body.end_time, '%d/%m/%Y %H:%M')
        if error:
            return jsonify({"message": str(error)}), 400

        auction_obj = Auction(
            item_name=body.item_name,
            start_time=start_time,
            end_time=end_time,
            start_price=body.start_price,
            highest_bid=body.start_price,
            currency_string=body.currency_string,
        )

        auction_obj.save()

        return jsonify(auction_obj), 201

    return jsonify({"message": "Forbidden"}), 403


@auction.route('/<auction_id>', methods=['GET'])
def view_auction(auction_id: str):
    if request.environ.get('is_admin'):
        auction_obj = Auction.objects(id=ObjectId(auction_id)).first()
        if not auction_obj:
            return jsonify({"message": "Auction not found"}), 404
        return jsonify(auction_obj), 200
    return jsonify({"message": "unauthorized"}), 403


@auction.route('/update/<auction_id>', methods=['PUT'])
@validate()
def update_auction(auction_id: str, body: AuctionModel):
    if request.environ.get('is_admin'):
        auction_obj = Auction.objects(id=ObjectId(auction_id)).first()
        if not auction_obj:
            return jsonify({"message": "Auction not found"}), 404

        start_time, error = convert_datetime(body.start_time, '%d/%m/%Y %H:%M')
        if error:
            return jsonify({"message": str(error)}), 400

        end_time, error = convert_datetime(body.end_time, '%d/%m/%Y %H:%M')
        if error:
            return jsonify({"message": str(error)}), 400

        if start_time >= end_time:
            return jsonify({"message": "start time must be less than end time"}), 400

        auction_obj.update(
            item_name=body.item_name,
            start_time=start_time,
            end_time=end_time,
            start_price=body.start_price,
            currency_string=body.currency_string,
            highest_bid=body.start_price,
            user_id=None
        )

        auction_obj = Auction.objects(id=auction_id)
        return jsonify(auction_obj), 200
    return jsonify({"message": "unauthorized"}), 403


@auction.route('/delete/<auction_id>', methods=['DELETE'])
def delete_auction(auction_id: str):
    if request.environ.get('is_admin'):
        auction_obj = Auction.objects(id=ObjectId(auction_id)).first()
        if not auction_obj:
            return jsonify({"message": "Auction not found"}), 404

        auction_obj.delete()
        return jsonify({'success': 'Deleted successfully'}), 204

    return jsonify({"message": "unauthorized"}), 403
