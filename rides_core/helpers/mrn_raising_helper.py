from django.db.models import Q, Sum

from apps.sales.models import MRNLogDetail, MRNMaster
from apps.stock.models import StockMaster




class StockChecker():
    
    def __init__(self,order_instance=None, product_batch= None):
        self.order_instance  = order_instance
        self.product_batch   = product_batch
        self.quantity_needed = 0
    
    def mrn_raise(self):

        instance = MRNMaster.objects.filter(Q(product=self.product_batch)&Q(is_approved=False))

        if instance is not None and len(instance)>0:
            instance          = instance.last()
            quantity_needed   = instance.quantity_needed
        else:
            instance          = MRNMaster()
            quantity_needed   = 0

        quantity_needed = quantity_needed + self.quantity_needed if quantity_needed not in ['',None] else self.quantity_needed


        instance.order              = self.order_instance.order
        instance.product            = self.product_batch
        instance.quantity_needed    = quantity_needed
        instance.save()

        log_instance                    = MRNLogDetail()
        log_instance.order              = self.order_instance.order
        log_instance.product            = self.product_batch
        log_instance.quantity_needed    = self.quantity_needed
        log_instance.save()



        return 
    
    def stockchecker(self):

        if self.product_batch is None  or self.order_instance is None:
            return None
        
        order_quantity = self.order_instance.quantity

        stock_master = StockMaster.objects.filter(product_batch=self.product_batch)

        if stock_master is not None:
            stock_master = stock_master.last()

            current_stock = stock_master.current_stock

            if current_stock < order_quantity :
                self.quantity_needed = int(order_quantity) - int(current_stock)

                self.mrn_raise()

        return
    

        
