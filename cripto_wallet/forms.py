from flask_wtf  import FlaskForm
from wtforms import SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired, ValidationError

coins = [("option","Select an option"),
         ("EUR","EUR"),
         ("BTC","BTC"), 
         ("BNB","BNB"),
         ("ETH","ETH"),
         ("USTD","USTD"),
         ("XRP","XRP"),
         ("ADA","ADA"),
         ("SOL","SOL"),
         ("DOT","DOT"),
         ("MATIC","MATIC")]



class SelectCoins(FlaskForm):
    amount = FloatField("Amount", description="Amount you want to invest", validators = [DataRequired("Must be a number")])
    coinFrom = SelectField("From", validators = [DataRequired("Select an option")], choices=coins, description="Coin you want to sell")
    coinTo = SelectField("To", validators = [DataRequired("Select an option")], choices=coins, description="Coin you want to buy")
    submit = SubmitField("Calculate")

    def validate_amount(self,field):
        if field.data<=0:
            raise ValidationError("Must be positive number")
        
    def validate_coinFrom(self, field):
        if field.data == "option":
            raise ValidationError("Select an option")
        
    def validate_coinTo(self, field):
        if field.data == "option":
            raise ValidationError("Select an option")
        if field.data == self.coinFrom.data:
            raise ValidationError("Select a different coin in To than in From")