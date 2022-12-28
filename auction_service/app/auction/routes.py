from datetime import datetime
from flask import Blueprint, request, jsonify
import json
from app.auction.models import Auction
from bson import ObjectId

auction = Blueprint('auctions', __name__, url_prefix='/auctions')


@auction.route('/', methods=['GET'])
def auctions():
    if request.environ.get('is_admin'):
        auction_objects = Auction.objects()
    else:
        raw_query = {'start_time': {'$lt': datetime.utcnow()}, 'end_time': {'$gt': datetime.utcnow()}}
        auction_objects = Auction.objects(__raw__=raw_query)

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
def create_auction():
    if request.environ.get('is_admin'):
        data = json.loads(request.data)
        item_name = data.get('item_name')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        start_price = data.get('start_price')
        highest_bid = data.get('start_price')
        currency_string = data.get('currency_string')

        if not (item_name and start_price and start_time and end_time and highest_bid and currency_string):
            return jsonify({
                "message": "item_name, start_price, start_time, end_time, highest_bid, currency_string are required"
            }), 400

        try:
            start_time = datetime.strptime(start_time, '%d/%m/%Y %H:%M')
            end_time = datetime.strptime(end_time, '%d/%m/%Y %H:%M')
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

        if start_time >= end_time:
            return jsonify({"message": "start time must be less than end time"}), 400

        auction_obj = Auction(
            item_name=item_name,
            start_time=start_time,
            end_time=end_time,
            start_price=start_price,
            highest_bid=highest_bid,
            currency_string=currency_string,
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
def update_auction(auction_id: str):
    if request.environ.get('is_admin'):
        auction_obj = Auction.objects(id=ObjectId(auction_id)).first()
        if not auction_obj:
            return jsonify({"message": "Auction not found"}), 404

        data = json.loads(request.data)
        data['start_time'] = datetime.strptime(data['start_time'], '%m/%d/%Y %H:%M')
        data['end_time'] = datetime.strptime(data['end_time'], '%m/%d/%Y %H:%M')

        auction_obj.update(**data)
        new_start_price = data.get('start_price', 0)
        if new_start_price > auction_obj.highest_bid:
            auction_obj.update(highest_bid=new_start_price, user_id=None)

        auction_obj = Auction.objects(id=auction_id)
        return jsonify(auction_obj),200
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
