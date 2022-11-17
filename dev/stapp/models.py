from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
 
class DataEntry(Model):
    brand_name = columns.Text(partition_key=True,max_length=1000,required=True)
    shop_id = columns.Integer(primary_key=True,required=True)
    item_id = columns.Integer(partition_key=True,required=True)
    date = columns.Date(primary_key=True,required=True)
    shop_name = columns.Text(max_length=1000,required=False)
    item_name = columns.Text(max_length=1000,required=False)
    item_price = columns.Float(required=False)
    item_cnt_day = columns.Integer(required=False)

    def to_dict(self):
        return {
            'brand_name': self.brand_name,
            'shop_id': self.shop_id,
            'item_id': self.item_id,
            'date': self.date,
            'shop_name': self.shop_name,
            'item_name': self.item_name,
            'item_price': self.item_price,
            'item_cnt_day': self.item_cnt_day,
        }
    def to_tuple(self):
        return (self.brand_name,self.shop_id,self.item_id,self.date,self.shop_name,self.item_name,self.item_price,self.item_cnt_day)
        
